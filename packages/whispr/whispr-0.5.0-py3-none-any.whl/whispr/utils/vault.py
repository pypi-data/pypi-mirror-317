import json

from dotenv import dotenv_values

from whispr.factory import VaultFactory
from whispr.logging import logger
from whispr.enums import VaultType


def fetch_secrets(config: dict) -> dict:
    """Fetch secret from relevant vault"""
    kwargs = config
    kwargs["logger"] = logger

    vault = config.get("vault")
    secret_name = config.get("secret_name")

    if not vault or not secret_name:
        logger.error(
            "Vault type or secret name not specified in the configuration file."
        )
        return {}

    try:
        vault_instance = VaultFactory.get_vault(**kwargs)
    except ValueError as e:
        logger.error(f"Error creating vault instance: {str(e)}")
        return {}

    secret_string = vault_instance.fetch_secrets(secret_name)
    if not secret_string:
        return {}

    return json.loads(secret_string)


def get_filled_secrets(env_file: str, vault_secrets: dict) -> dict:
    """Inject vault secret values into local empty secrets"""

    filled_secrets = {}
    env_vars = dotenv_values(dotenv_path=env_file)

    # Iterate over .env variables and check if they exist in the fetched secrets
    for key in env_vars:
        if key in vault_secrets:
            filled_secrets[key] = vault_secrets[key]  # Collect the matching secrets
        else:
            logger.warning(
                f"The given key: '{key}' is not found in vault. So ignoring it."
            )

    # Return the dictionary of matched secrets for further use if needed
    return filled_secrets


def prepare_vault_config(vault_type: str) -> dict:
    """Prepares in-memory configuration for a given vault"""
    config = {
        "env_file": ".env",
        "secret_name": "<your_secret_name>",
        "vault": VaultType.AWS.value,
    }

    # Add more configuration fields as needed for other secret managers.
    if vault_type == VaultType.GCP.value:
        config["project_id"] = "<gcp_project_id>"
        config["vault"] = VaultType.GCP.value
    elif vault_type == VaultType.AZURE.value:
        config["vault_url"] = "<azure_vault_url>"
        config["vault"] = VaultType.AZURE.value

    return config
