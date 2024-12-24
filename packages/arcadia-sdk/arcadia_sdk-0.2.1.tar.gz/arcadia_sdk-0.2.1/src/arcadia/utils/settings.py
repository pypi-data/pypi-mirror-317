from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings class for managing environment variables and configuration.

    This class uses pydantic-settings to handle environment variables
    with enhanced configuration and type validation.

    Attributes:
        stripe_secret_key: Stripe API secret key
        supabase_url: Supabase project URL
        supabase_service_role_key: Supabase service role key
        slack_webhook: Slack webhook URL for notifications
        replicate_api_token: Replicate API authentication token
    """

    # Directly map environment variables
    stripe_secret_key: Optional[str] = None
    supabase_url: Optional[str] = None
    supabase_service_role_key: Optional[str] = None
    slack_webhook: Optional[str] = None
    replicate_api_token: Optional[str] = None

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",  # Path to .env file
        env_file_encoding="utf-8",
        extra="allow",  # Allow extra environment variables
        case_sensitive=False,  # Ignore case when matching env vars
    )

    def get_settings_dict(self) -> Dict[str, Any]:
        """
        Convert settings to a dictionary, excluding None values.

        Returns:
            Dict[str, Any]: A dictionary of non-None settings
        """
        return {k: v for k, v in self.__dict__.items() if v is not None}


@lru_cache()
def get_settings() -> Settings:
    """
    Get a cached Settings instance.

    Returns:
        Settings: Cached Settings instance with environment variables
    """
    return Settings()


# Optional: Quick validation method
def validate_settings():
    """
    Validate that critical environment variables are set.
    Raises a ValueError if any critical setting is missing.
    """
    settings = get_settings()
    critical_settings = [
        "stripe_secret_key",
        "supabase_url",
        "supabase_service_role_key",
    ]

    for setting in critical_settings:
        if not getattr(settings, setting):
            raise ValueError(f"Critical setting {setting} is not set")
