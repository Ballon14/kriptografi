"""
Hybrid File Decryption Engine.

RSA:
- Decrypt AES session key

AES:
- Decrypt file content
"""


import json

import base64


from pathlib import Path


from Crypto.Cipher import PKCS1_OAEP


from aes import AESGCMManager

from rsa_key import RSAKeyManager


from config import (
    DECRYPTED_DIR
)


from logger import setup_logger




class FileDecryptor:
    """
    Handle .filevault decryption.
    """



    def __init__(self):

        self.aes = AESGCMManager()

        self.rsa = RSAKeyManager()

        self.logger = setup_logger()



    def decrypt_file(
        self,
        encrypted_file: Path
    ) -> Path:
        """
        Decrypt encrypted vault file.

        Returns:
            Restored original file path.
        """

        try:


            if not encrypted_file.exists():

                raise FileNotFoundError(
                    "Encrypted file not found"
                )



            private_key = (
                self.rsa.load_private_key()
            )


            if private_key is None:

                raise ValueError(
                    "Private key unavailable"
                )



            package = json.loads(

                encrypted_file.read_text(
                    encoding="utf-8"
                )

            )



            encrypted_key = (
                base64.b64decode(
                    package["encrypted_key"]
                )
            )


            nonce = (
                base64.b64decode(
                    package["nonce"]
                )
            )


            tag = (
                base64.b64decode(
                    package["tag"]
                )
            )


            ciphertext = (
                base64.b64decode(
                    package["ciphertext"]
                )
            )



            rsa_cipher = (
                self.rsa.create_cipher(
                    private_key
                )
            )



            aes_key = (
                rsa_cipher.decrypt(
                    encrypted_key
                )
            )



            plaintext = (
                self.aes.decrypt(
                    ciphertext,
                    aes_key,
                    nonce,
                    tag
                )
            )



            original_name = (
                package["filename"]
            )



            output_file = (
                DECRYPTED_DIR /
                original_name
            )



            output_file.write_bytes(
                plaintext
            )



            self.logger.info(
                f"Decrypted: {original_name}"
            )



            return output_file



        except FileNotFoundError as error:


            self.logger.error(
                f"File error: {error}"
            )

            raise



        except ValueError as error:


            self.logger.error(
                f"Validation error: {error}"
            )

            raise



        except Exception as error:


            self.logger.error(
                f"Decryption failed: {error}"
            )

            raise
