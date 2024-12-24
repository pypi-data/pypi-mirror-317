import os
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional

import stripe
from supabase import Client, create_client

from arcadia.modules.logger.factory import LoggerFactory
from arcadia.utils.settings import Settings


class InvoiceStatus(Enum):
    PENDING = "pending"  # For users without payment methods
    PAID = "paid"
    FAILED = "failed"


class BillingProcessor:
    def __init__(self):
        self.settings = Settings()
        self.logger = LoggerFactory()
        self.supabase: Client = create_client(
            self.settings.supabase_url, self.settings.supabase_key
        )
        stripe.api_key = self.settings.stripe_secret_key
        self.PLATFORM_FEE = 0.10
        self.MODEL_OWNER_SHARE = 1 - self.PLATFORM_FEE

    def get_default_payment_method(self, customer_id: str) -> Optional[str]:
        """Get customer's default payment method if exists"""
        try:
            customer = stripe.Customer.retrieve(customer_id)
            if customer.invoice_settings.default_payment_method:
                return customer.invoice_settings.default_payment_method

            # If no default set, get their first payment method
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id, type="card"
            )
            if payment_methods.data:
                return payment_methods.data[0].id

            return None
        except Exception as e:
            self.logger.error(
                f"Error getting payment method for customer {customer_id}: {str(e)}"
            )
            return None

    def charge_pending_invoices(self, user_id: str):
        """Charge any pending invoices when user adds payment method"""
        try:
            # Get all pending invoices for user
            pending_invoices = (
                self.supabase.table("invoices")
                .select("*")
                .eq("user_id", user_id)
                .eq("status", InvoiceStatus.PENDING.value)
                .execute()
            )

            for invoice in pending_invoices.data:
                payment_intent_id = self.charge_customer(
                    user_id, invoice["total_revenue"]
                )
                if payment_intent_id:
                    # Update invoice to paid status
                    self.supabase.table("invoices").update(
                        {
                            "status": InvoiceStatus.PAID.value,
                            "payment_id": payment_intent_id,
                        }
                    ).eq("id", invoice["id"]).execute()

                    self.logger.info(
                        f"Successfully charged pending invoice {invoice['id']} for user {user_id}"
                    )
                else:
                    self.logger.error(
                        f"Failed to charge pending invoice {invoice['id']} for user {user_id}"
                    )

        except Exception as e:
            self.logger.error(
                f"Error charging pending invoices for user {user_id}: {str(e)}"
            )

    def handle_payment_method_added(self, user_id: str):
        """Called when user connects their payment method"""
        # First charge any pending invoices
        self.charge_pending_invoices(user_id)

        # Setup automatic billing flag in database
        self.supabase.table("users").update({"automatic_billing_enabled": True}).eq(
            "id", user_id
        ).execute()
        try:
            user = (
                self.supabase.table("users")
                .select("*")
                .eq("id", user_id)
                .single()
                .execute()
            )
            if not user.data or not user.data.get("stripe_customer_id"):
                self.logger.info(f"User {user_id} not set up with Stripe yet")
                return None

            customer_id = user.data["stripe_customer_id"]
            payment_method_id = self.get_default_payment_method(customer_id)

            if not payment_method_id:
                self.logger.info(f"No payment method found for user {user_id}")
                return None

            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency="usd",
                customer=customer_id,
                payment_method=payment_method_id,
                off_session=True,
                confirm=True,
            )

            if payment_intent.status == "succeeded":
                self.logger.info(
                    f"Successfully charged customer {user_id} ${amount:.2f}"
                )
                return payment_intent.id
            else:
                self.logger.error(
                    f"Payment failed for customer {user_id}: {payment_intent.status}"
                )
                return None

        except stripe.error.CardError as e:
            self.logger.error(f"Card declined for user {user_id}: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Error charging customer {user_id}: {str(e)}")
            return None

    def calculate_monthly_usage(
        self, model_id: str, user_id: str, month: datetime
    ) -> Dict:
        """Calculate usage and earnings for a model"""
        try:
            model_details = (
                self.supabase.table("models")
                .select("*")
                .eq("id", model_id)
                .single()
                .execute()
            )

            if not model_details.data:
                return {}

            cost_per_call = model_details.data.get("cost_per_call", 0)
            start_of_month = month.replace(day=1)
            end_of_month = (start_of_month + timedelta(days=32)).replace(
                day=1
            ) - timedelta(days=1)

            usage_query = (
                self.supabase.table("model_usage")
                .select("model_id, count")
                .eq("model_id", model_id)
                .eq("user_id", user_id)
                .gte("timestamp", start_of_month.isoformat())
                .lte("timestamp", end_of_month.isoformat())
                .execute()
            )

            total_calls = sum(row.get("count", 0) for row in usage_query.data)
            total_revenue = total_calls * cost_per_call

            return {
                "model_id": model_id,
                "user_id": user_id,
                "total_calls": total_calls,
                "cost_per_call": cost_per_call,
                "total_revenue": total_revenue,
                "arcadia_share": total_revenue * self.PLATFORM_FEE,
                "model_owner_share": total_revenue * self.MODEL_OWNER_SHARE,
            }
        except Exception as e:
            self.logger.error(f"Error calculating usage: {str(e)}")
            return {}

    def create_invoice(
        self, usage_details: Dict, payment_intent_id: Optional[str] = None
    ) -> Optional[str]:
        """Create invoice record"""
        try:
            if not usage_details or usage_details.get("total_revenue", 0) <= 0:
                return None

            status = (
                InvoiceStatus.PAID.value
                if payment_intent_id
                else InvoiceStatus.PENDING.value
            )

            invoice_data = {
                "model_id": usage_details["model_id"],
                "user_id": usage_details["user_id"],
                "month": datetime.now().strftime("%Y-%m"),
                "total_calls": usage_details["total_calls"],
                "total_revenue": usage_details["total_revenue"],
                "arcadia_share": usage_details["arcadia_share"],
                "model_owner_share": usage_details["model_owner_share"],
                "status": status,
            }

            if payment_intent_id:
                invoice_data["payment_id"] = payment_intent_id

            invoice = self.supabase.table("invoices").insert(invoice_data).execute()
            return invoice.data[0]["id"] if invoice.data else None

        except Exception as e:
            self.logger.error(f"Error creating invoice: {str(e)}")
            return None

    def monthly_billing_cycle(self):
        """Process monthly billing"""
        billing_month = datetime.now().replace(day=1) - timedelta(days=1)

        usage_data = (
            self.supabase.table("model_usage")
            .select("user_id, model_id")
            .gte("timestamp", billing_month.replace(day=1).isoformat())
            .lte("timestamp", billing_month.isoformat())
            .execute()
        )

        unique_combinations = {
            (usage["user_id"], usage["model_id"]) for usage in usage_data.data
        }

        platform_total_amount = 0
        platform_total_calls = 0
        successful_charges = 0
        pending_charges = 0

        for user_id, model_id in unique_combinations:
            try:
                usage_details = self.calculate_monthly_usage(
                    model_id, user_id, billing_month
                )

                if not usage_details or usage_details["total_revenue"] <= 0:
                    continue

                platform_total_amount += usage_details["total_revenue"]
                platform_total_calls += usage_details["total_calls"]

                # Try to charge if they have payment set up
                payment_intent_id = self.charge_customer(
                    user_id, usage_details["total_revenue"]
                )

                if payment_intent_id:
                    successful_charges += 1
                else:
                    pending_charges += 1

                # Create invoice regardless of payment status
                self.create_invoice(usage_details, payment_intent_id)

            except Exception as e:
                self.logger.error(
                    f"Billing cycle error for user {user_id} "
                    f"and model {model_id}: {str(e)}"
                )

        self.logger.info(
            f"Monthly billing cycle completed for {billing_month.strftime('%B %Y')}:\n"
            f"Total Platform Revenue: ${platform_total_amount:,.2f}\n"
            f"Total Inference Calls: {platform_total_calls:,}\n"
            f"Successful Charges: {successful_charges}\n"
            f"Pending Charges: {pending_charges}"
        )


if __name__ == "__main__":
    processor = BillingProcessor()
    processor.monthly_billing_cycle()
