from pathlib import Path
from decrypt import FileDecryptor

decryptor = FileDecryptor()

result = decryptor.decrypt_file(

    Path(
        "encrypted/sample.txt.filevault"
    )

)


print(
    result
)
