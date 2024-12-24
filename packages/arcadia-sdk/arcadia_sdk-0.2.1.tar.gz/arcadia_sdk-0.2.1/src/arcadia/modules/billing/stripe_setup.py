import os
from typing import Dict, Optional

import stripe
from supabase import Client, create_client

from arcadia.modules.logger.factory import LoggerFactory
from arcadia.utils.settings import Settings


class StripeSetup:
    def __init__(self):
        self.settings = Settings()
        self.logger = LoggerFactory()
        self.supabase: Client = create_client(
            self.settings.supabase_url, self.settings.supabase_key
        )
        stripe.api_key = self.settings.stripe_secret_key

    def setup_stripe_columns(self):
        """Add stripe_account_id column and migrate data"""
        try:
            # Add new column if it doesn't exist
            self.supabase.table("users").update({"stripe_account_id": None}).eq(
                "id", "dummy"
            ).execute()

            # Get all users with existing stripe_customer_id that starts with 'acct_'
            users = self.supabase.table("users").select("*").execute()

            for user in users.data:
                if user.get("stripe_customer_id", "").startswith("acct_"):
                    # Move acct_ ID to new column and clear customer_id
                    self.supabase.table("users").update(
                        {
                            "stripe_account_id": user["stripe_customer_id"],
                            "stripe_customer_id": None,
                        }
                    ).eq("id", user["id"]).execute()

            self.logger.info("Successfully set up Stripe columns")

        except Exception as e:
            self.logger.error(f"Error setting up Stripe columns: {str(e)}")

    def create_stripe_customer(self, user: Dict) -> Optional[str]:
        """Create a Stripe customer for a user"""
        try:
            # Create new customer
            customer = stripe.Customer.create(
                email=user.get(
                    "email", f"user_{user['id']}@arcadia.ai"
                ),  # Fallback email if none exists
                name=user.get(
                    "name", f"User {user['id']}"
                ),  # Fallback name if none exists
                metadata={"user_id": user["id"], "arcadia_user": "true"},
            )

            self.logger.info(
                f"Created Stripe customer for user {user['id']}: {customer.id}"
            )
            return customer.id

        except Exception as e:
            self.logger.error(
                f"Error creating Stripe customer for user {user['id']}: {str(e)}"
            )
            return None

    def setup_all_customers(self):
        """Set up Stripe customers for all users"""
        try:
            # First set up columns
            self.setup_stripe_columns()

            # Get all users without stripe_customer_id
            users = (
                self.supabase.table("users")
                .select("*")
                .is_("stripe_customer_id", "null")
                .execute()
            )

            for user in users.data:
                # Create customer and update user
                customer_id = self.create_stripe_customer(user)
                if customer_id:
                    self.supabase.table("users").update(
                        {"stripe_customer_id": customer_id}
                    ).eq("id", user["id"]).execute()

            self.logger.info("Completed Stripe customer setup for all users")

        except Exception as e:
            self.logger.error(f"Error in setup_all_customers: {str(e)}")


def run_stripe_setup():
    setup = StripeSetup()
    setup.setup_all_customers()


if __name__ == "__main__":
    run_stripe_setup()
