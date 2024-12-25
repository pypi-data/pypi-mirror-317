import codecs

import gostcrypto


class Kuznechik:
    def __init__(self, key: str):
        self.key = bytearray.fromhex(key)

    def encrypt(self, text: str) -> str:
        heximal = text.encode().hex()
        return self.kuznechik_encryptor(bytes.fromhex(heximal)).hex()

    def kuznechik_encryptor(self, input_array: bytes) -> bytes:
        cipher_obj = gostcrypto.gostcipher.new(
            "kuznechik", self.key, gostcrypto.gostcipher.MODE_ECB, pad_mode=gostcrypto.gostcipher.PAD_MODE_1
        )
        return cipher_obj.encrypt(bytearray(input_array))  # pyright: ignore[reportAttributeAccessIssue, reportReturnType]

    def decrypt(self, text: str) -> str:
        result = self.kuznechik_decryptor(bytes.fromhex(text))
        return codecs.decode(result.hex(), "hex").decode()

    def kuznechik_decryptor(self, input_array: bytes) -> bytes:
        cipher_obj = gostcrypto.gostcipher.new(
            "kuznechik", self.key, gostcrypto.gostcipher.MODE_ECB, pad_mode=gostcrypto.gostcipher.PAD_MODE_1
        )
        result = cipher_obj.decrypt(bytearray(input_array))  # pyright: ignore[reportAttributeAccessIssue]
        return self.remove_fillers(result)  # pyright: ignore[reportArgumentType]

    def remove_fillers(self, byte_array: bytes) -> bytes:
        return byte_array.replace(b"\x00", b"")


class Streebog:
    def __init__(self, key: str):
        self.key = bytearray.fromhex(key)

    def encrypt(self, text: str) -> str:
        heximal = text.encode().hex()
        return self.streebog_encryptor(bytes.fromhex(heximal)).hex()

    def streebog_encryptor(self, input_array: bytes) -> bytearray:
        cipher_obj = gostcrypto.gosthash.new("streebog512", data=input_array)
        return cipher_obj.digest()
