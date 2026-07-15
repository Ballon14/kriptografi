"""
AES-256-GCM Encryption Module.

Used for encrypting file content.
"""


from typing import Tuple


from Crypto.Cipher import AES

from Crypto.Random import get_random_bytes



from config import AES_KEY_SIZE



class AESGCMManager:
    """
    Manage AES-256-GCM operations.
    """


    def generate_key(self) -> bytes:
        """
        Generate secure AES-256 key.

        Returns:
            32 bytes key
        """

        return get_random_bytes(
            AES_KEY_SIZE
        )



    def encrypt(
        self,
        plaintext: bytes,
        key: bytes
    ) -> Tuple[bytes, bytes, bytes]:
        """
        Encrypt data using AES-GCM.

        Returns:

        ciphertext,
        nonce,
        authentication tag

        """

        cipher = AES.new(
            key,
            AES.MODE_GCM
        )


        ciphertext, tag = (
            cipher.encrypt_and_digest(
                plaintext
            )
        )


        return (
            ciphertext,
            cipher.nonce,
            tag
        )



    def decrypt(
        self,
        ciphertext: bytes,
        key: bytes,
        nonce: bytes,
        tag: bytes
    ) -> bytes:
        """
        Decrypt AES-GCM data.

        Raises:
            ValueError:
            If integrity check fails.
        """


        cipher = AES.new(
            key,
            AES.MODE_GCM,
            nonce=nonce
        )


        plaintext = (
            cipher.decrypt_and_verify(
                ciphertext,
                tag
            )
        )


        return plaintext
