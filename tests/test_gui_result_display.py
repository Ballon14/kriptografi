from pathlib import Path

from gui import SecureFileVaultGUI


def test_format_result_message_includes_operation_details(tmp_path):
    gui = object.__new__(SecureFileVaultGUI)

    source_file = tmp_path / "plain.txt"
    source_file.write_text("hello world", encoding="utf-8")

    output_file = tmp_path / "plain.txt.filevault"
    output_file.write_text("{\"status\": \"encrypted\"}", encoding="utf-8")

    message = gui.format_result_message("Encryption", source_file, output_file)

    assert "Encryption complete" in message
    assert "plain.txt" in message
    assert "plain.txt.filevault" in message
    assert "encrypted" in message


def test_format_result_message_for_decryption(tmp_path):
    gui = object.__new__(SecureFileVaultGUI)

    encrypted_file = tmp_path / "secret.filevault"
    encrypted_file.write_text("{\"status\": \"decrypted\"}", encoding="utf-8")

    restored_file = tmp_path / "secret.txt"
    restored_file.write_text("restored", encoding="utf-8")

    message = gui.format_result_message("Decryption", encrypted_file, restored_file)

    assert "Decryption complete" in message
    assert "secret.filevault" in message
    assert "secret.txt" in message
    assert "restored" in message
