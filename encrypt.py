"""
Hybrid File Encryption Engine.

AES encrypts file content.
RSA encrypts AES session key.
"""


import json

import base64


from pathlib import Path


from Crypto.Cipher import PKCS1_OAEP



from aes import AESGCMManager


from rsa_key import RSAKeyManager


from config import (
    FILE_EXTENSION,
    ENCRYPTED_DIR
)


from logger import setup_logger




class FileEncryptor:
    """
    Encrypt files using RSA + AES hybrid cryptography.
    """



    def __init__(self):

        self.aes = AESGCMManager()

        self.rsa = RSAKeyManager()

        self.logger = setup_logger()



    def encrypt_file(
        self,
        file_path: Path
    ) -> Path:
        """
        Encrypt a file.

        Output:
            .filevault file
        """


        if not file_path.exists():

            raise FileNotFoundError(
                "File does not exist"
            )



        public_key = (
            self.rsa.load_public_key()
        )


        if public_key is None:

            raise ValueError(
                "Public key unavailable"
            )



        plaintext = (
            file_path.read_bytes()
        )



        aes_key = (
            self.aes.generate_key()
        )



        ciphertext, nonce, tag = (
            self.aes.encrypt(
                plaintext,
                aes_key
            )
        )



        rsa_cipher = (
            self.rsa.create_cipher(
                public_key
            )
        )



        encrypted_key = (
            rsa_cipher.encrypt(
                aes_key
            )
        )



        package = {

            "filename":
            file_path.name,


            "encrypted_key":
            base64.b64encode(
                encrypted_key
            ).decode(),


            "nonce":
            base64.b64encode(
                nonce
            ).decode(),


            "tag":
            base64.b64encode(
                tag
            ).decode(),


            "ciphertext":
            base64.b64encode(
                ciphertext
            ).decode()

        }



        output_file = (
            ENCRYPTED_DIR /
            (
                file_path.name
                +
                FILE_EXTENSION
            )
        )



        output_file.write_text(
            json.dumps(package),
            encoding="utf-8"
        )



        self.logger.info(
            f"Encrypted: {file_path.name}"
        )



        return output_file
