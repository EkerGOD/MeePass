# AES 加密
import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# 生成加密密钥
def derive_key(value, salt, length=32, iterations=100000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive((value).encode())


# AES 加密
def aes_encryption(value ,key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    print(value)
    padded_data = padder.update(value.encode()) + padder.finalize()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_data = base64.b64encode(iv + encrypted).decode()
    return encrypted_data

# AES 解密
def aes_decryption(value, key):
    # 解密密文
    encrypted_data = base64.b64decode(value)
    print("encrypted_data", encrypted_data)

    # 提取iv和密文
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    print("IV:", iv)
    print("Ciphertext:", ciphertext)

    # 解密
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted = decryptor.update(ciphertext) + decryptor.finalize()

    print("Decrypted data:", decrypted)

    # 去除填充并返回原始密码
    unpadder = padding.PKCS7(128).unpadder()
    unpadded = unpadder.update(decrypted) + unpadder.finalize()
    return unpadded.decode()