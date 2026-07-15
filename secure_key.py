"""
Secure RSA Key Storage Module

Features:
- RSA 2048 generation
- Password protected private key
- Public key export
- Private key loading
- Key validation
"""


from pathlib import Path

from typing import Optional


from Crypto.PublicKey import RSA

from Crypto.Random import get_random_bytes


from logger import setup_logger

from config import (
    RSA_KEY_SIZE,
    KEY_DIR
)



PUBLIC_KEY_PATH = (
    KEY_DIR /
    "public_key.pem"
)


PRIVATE_KEY_PATH = (
    KEY_DIR /
    "private_key.pem"
)



class SecureRSAKeyManager:
    """
    Secure RSA key management.
    """


    def __init__(self):

        self.logger = setup_logger()



    def generate_key_pair(
        self,
        password: str
    ) -> bool:
        """
        Generate RSA key pair.

        Private key is protected
        using password.
        """

        try:

            if len(password) < 8:

                raise ValueError(
                    "Password minimum 8 characters"
                )


            rsa_key = RSA.generate(
                RSA_KEY_SIZE
            )


            private_key = rsa_key.export_key(

                format="PEM",

                passphrase=password,

                protection=
                "PBKDF2WithHMAC-SHA512AndAES256-CBC"

            )


            public_key = (

                rsa_key.publickey()
                .export_key()

            )



            PRIVATE_KEY_PATH.write_bytes(

                private_key

            )


            PUBLIC_KEY_PATH.write_bytes(

                public_key

            )


            self.logger.info(

                "Protected RSA key generated"

            )


            return True



        except Exception as error:


            self.logger.error(

                f"RSA generation error: {error}"

            )


            return False



    def load_private_key(
        self,
        password: str
    ) -> Optional[RSA.RsaKey]:
        """
        Load password protected private key.
        """


        try:


            if not PRIVATE_KEY_PATH.exists():

                raise FileNotFoundError(

                    "Private key missing"

                )



            key = RSA.import_key(

                PRIVATE_KEY_PATH.read_bytes(),

                passphrase=password

            )



            if not key.has_private():

                raise ValueError(

                    "Invalid private key"

                )



            self.logger.info(

                "Private key loaded"

            )


            return key



        except ValueError:


            self.logger.error(

                "Wrong private key password"

            )


            return None



        except Exception as error:


            self.logger.error(

                f"Load private key failed: {error}"

            )


            return None



    def load_public_key(
        self
    ) -> Optional[RSA.RsaKey]:
        """
        Load public key.
        """


        try:


            if not PUBLIC_KEY_PATH.exists():

                raise FileNotFoundError(

                    "Public key missing"

                )



            key = RSA.import_key(

                PUBLIC_KEY_PATH.read_bytes()

            )


            return key



        except Exception as error:


            self.logger.error(

                f"Load public key failed: {error}"

            )


            return None



    def key_information(
        self,
        key: RSA.RsaKey
    ) -> dict:
        """
        Return key information.
        """


        return {


            "algorithm":
            "RSA",


            "size":
            key.size_in_bits(),


            "private":
            key.has_private()

        }
