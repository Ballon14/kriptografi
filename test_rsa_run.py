from rsa_key import RSAKeyManager



manager = RSAKeyManager()



result = manager.generate_key_pair()



print(
    "Generate:",
    result
)



private_key = (
    manager.load_private_key()
)


public_key = (
    manager.load_public_key()
)



print(
    manager.get_key_information(
        private_key
    )
)


print(
    manager.get_key_information(
        public_key
    )
)
