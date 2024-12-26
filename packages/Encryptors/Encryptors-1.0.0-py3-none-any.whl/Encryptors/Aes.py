import os
from base64 import b64decode, b64encode
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from src.Exceptions.CustomExceptions import AESEncryptError

class AES:
    def __init__(self):
        self.IV_LENGTH = 32
        self.TAG_LENGTH = 16

    @staticmethod
    def generate_key() -> str:
        key = os.urandom(32)
        return b64encode(key).decode('utf-8')
    
    def encrypt(self, aes_key: str, data: dict | str | list) -> str:
        if not isinstance(data, (dict, str, list)):
            raise ValueError('Input data must be a dictionary, string, or list.')

        try:
            key = b64decode(aes_key)
            iv = os.urandom(self.IV_LENGTH)

            if isinstance(data, (dict, list)):
                json_data = json.dumps(data)
            else:
                json_data = data

            cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(json_data.encode('utf-8')) + encryptor.finalize()
            tag = encryptor.tag
            encrypted_data = iv + ciphertext + tag

            return b64encode(encrypted_data).decode('utf-8')

        except Exception as ex:
            raise AESEncryptError(message='Encryption AES operation failed', error=str(ex), status_code=500) from ex
   

    def decrypt(self, aes_key: str, encrypted_data: str):
        try:
            key = b64decode(aes_key)
            encrypted_data = b64decode(encrypted_data)
            iv = encrypted_data[:self.IV_LENGTH]
            tag = encrypted_data[-self.TAG_LENGTH:]
            ciphertext = encrypted_data[self.IV_LENGTH:-self.TAG_LENGTH]
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            try:
                decrypted_data = json.loads(plaintext.decode('utf-8'))
                return decrypted_data
            except json.JSONDecodeError:
                return plaintext.decode('utf-8')

        except Exception as ex:
            raise AESEncryptError(message='Decryption AES operation failed', error=str(ex), status_code=500) from ex