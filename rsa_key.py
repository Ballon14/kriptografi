"""
RSA Key Management Module.

Responsible for:
- RSA key generation
- Saving keys
- Loading keys
- Key validation
"""


from pathlib import Path

from typing import Optional


from Crypto.PublicKey import RSA


from Crypto.Cipher import PKCS1_OAEP


from Crypto.Hash import SHA256


from config import (
    RSA_KEY_SIZE,
    PUBLIC_KEY_FILE,
    PRIVATE_KEY_FILE
)


from logger import setup_logger



class RSAKeyManager:
    """
    Manage RSA public and private keys.
    """


    def __init__(self):

        self.logger = setup_logger()



    def generate_key_pair(self) -> bool:
        """
        Generate RSA-2048 key pair.

        Returns:
            bool:
            True if generation success.
        """

        try:

            key = RSA.generate(
                RSA_KEY_SIZE
            )


            private_key = (
                key.export_key()
            )


            public_key = (
                key.publickey()
                .export_key()
            )


            PRIVATE_KEY_FILE.write_bytes(
                private_key
            )


            PUBLIC_KEY_FILE.write_bytes(
                public_key
            )


            self.logger.info(
                "RSA key pair generated"
            )


            return True


        except Exception as error:


            self.logger.error(
                f"RSA generation failed: {error}"
            )


            return False



    def save_private_key(
        self,
        key_data: bytes,
        path: Path = PRIVATE_KEY_FILE
    ) -> bool:
        """
        Save private key.
        """

        try:

            path.write_bytes(
                key_data
            )


            self.logger.info(
                "Private key saved"
            )


            return True


        except PermissionError:


            self.logger.error(
                "Permission denied saving private key"
            )


            return False



    def save_public_key(
        self,
        key_data: bytes,
        path: Path = PUBLIC_KEY_FILE
    ) -> bool:
        """
        Save public key.
        """

        try:

            path.write_bytes(
                key_data
            )


            self.logger.info(
                "Public key saved"
            )


            return True


        except PermissionError:


            self.logger.error(
                "Permission denied saving public key"
            )


            return False



    def load_private_key(
        self,
        path: Path = PRIVATE_KEY_FILE
    ) -> Optional[RSA.RsaKey]:
        """
        Load private RSA key.
        """

        try:

            if not path.exists():

                raise FileNotFoundError(
                    "Private key not found"
                )


            key = RSA.import_key(
                path.read_bytes()
            )


            if not key.has_private():

                raise ValueError(
                    "Key is not private"
                )


            self.logger.info(
                "Private key loaded"
            )


            return key



        except Exception as error:


            self.logger.error(
                f"Private key loading failed: {error}"
            )


            return None



    def load_public_key(
        self,
        path: Path = PUBLIC_KEY_FILE
    ) -> Optional[RSA.RsaKey]:
        """
        Load public RSA key.
        """

        try:

            if not path.exists():

                raise FileNotFoundError(
                    "Public key not found"
                )


            key = RSA.import_key(
                path.read_bytes()
            )


            self.logger.info(
                "Public key loaded"
            )


            return key



        except Exception as error:


            self.logger.error(
                f"Public key loading failed: {error}"
            )


            return None



    def get_key_information(
        self,
        key: RSA.RsaKey
    ) -> dict:
        """
        Return RSA key information.
        """

        return {

            "bits":
            key.size_in_bits(),


            "has_private":
            key.has_private(),


            "type":
            "RSA"

        }



    def create_cipher(
        self,
        public_key: RSA.RsaKey
    ) -> PKCS1_OAEP:
        """
        Create RSA OAEP cipher.

        SHA-256 is used as OAEP hash.
        """

        return PKCS1_OAEP.new(
            public_key,
            hashAlgo=SHA256
        )
