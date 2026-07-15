from pathlib import Path

from config import DECRYPTED_DIR, ENCRYPTED_DIR, initialize_directories
from decrypt import FileDecryptor
from encrypt import FileEncryptor
from rsa_key import RSAKeyManager


def test_encrypt_and_decrypt_round_trip(tmp_path):
    initialize_directories()

    manager = RSAKeyManager()
    assert manager.generate_key_pair() is True

    source_file = tmp_path / "sample.txt"
    source_file.write_bytes(b"secret payload for round trip test" * 5)

    encryptor = FileEncryptor()
    encrypted_file = encryptor.encrypt_file(source_file)

    assert encrypted_file.exists()
    assert encrypted_file.suffix == ".filevault"

    decryptor = FileDecryptor()
    restored_file = decryptor.decrypt_file(encrypted_file)

    assert restored_file.exists()
    assert restored_file.read_bytes() == source_file.read_bytes()

    restored_file.unlink(missing_ok=True)
    encrypted_file.unlink(missing_ok=True)
    for path in DECRYPTED_DIR.glob("*"):
        if path.is_file():
            path.unlink(missing_ok=True)
    for path in ENCRYPTED_DIR.glob("*"):
        if path.is_file():
            path.unlink(missing_ok=True)
