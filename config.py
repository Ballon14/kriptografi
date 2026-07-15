"""
Application configuration module.
"""

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


APP_NAME = "Secure File Vault"

APP_VERSION = "1.0.0"


RSA_KEY_SIZE = 2048

AES_KEY_SIZE = 32


PUBLIC_KEY_FILE = (
    BASE_DIR /
    "keys" /
    "public_key.pem"
)


PRIVATE_KEY_FILE = (
    BASE_DIR /
    "keys" /
    "private_key.pem"
)


FILE_EXTENSION = ".filevault"



ASSET_DIR = BASE_DIR / "assets"

KEY_DIR = BASE_DIR / "keys"

ENCRYPTED_DIR = BASE_DIR / "encrypted"

DECRYPTED_DIR = BASE_DIR / "decrypted"

LOG_DIR = BASE_DIR / "logs"



def initialize_directories() -> None:
    """
    Create application directories.
    """

    directories = [

        ASSET_DIR,

        KEY_DIR,

        ENCRYPTED_DIR,

        DECRYPTED_DIR,

        LOG_DIR

    ]


    for directory in directories:

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

VAULT_HEADER = "SECURE_FILE_VAULT"

HASH_ALGORITHM = "SHA-256"
