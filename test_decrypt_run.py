from pathlib import Path

import pytest

from decrypt import FileDecryptor


target_file = Path("encrypted/sample.txt.filevault")
if not target_file.exists():
    pytest.skip("sample encrypted file is not present", allow_module_level=True)

decryptor = FileDecryptor()
result = decryptor.decrypt_file(target_file)
print(result)
