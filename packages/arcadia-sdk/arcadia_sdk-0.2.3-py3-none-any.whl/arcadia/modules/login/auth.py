import json
import os

from supabase import Client, create_client

from arcadia.utils.settings import Settings

from .config import CONFIG_DIR, CONFIG_FILE


def save_credentials(username: str, api_key: str):
    """Save credentials to config file"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"username": username, "api_key": api_key}, f)


def load_credentials():
    """Load credentials from config file"""
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("Not logged in. Please run 'arcadia login' first.")


def validate_credentials(username: str, api_key: str) -> bool:
    """Validate credentials against Supabase"""
    try:
        settings = Settings()
        supabase: Client = create_client(settings.supabase_url, settings.supabase_key)
        response = (
            supabase.table("users")
            .select("*")
            .eq("username", username)
            .eq("api_key", api_key)
            .execute()
        )
        return len(response.data) > 0
    except Exception as e:
        print(f"Error validating credentials: {e}")
        return False
