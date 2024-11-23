# AES 加密
import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# 生成加密密钥
def derive_key(master_password, cryption_code, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive((master_password + cryption_code).encode())


# AES 加密
def aes_encryption(value ,key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = padding.PKCS7(128).padder().update(value.encode()) + padding.PKCS7(128).padder().finalize()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_data = base64.b64encode(iv + encrypted).decode()
    return encrypted_data

# AES 解密
def aes_decryption(value, key):
    # 解密密文
    encrypted_data = base64.b64decode(value)

    # 提取iv和密文
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    # 解密
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted = decryptor.update(ciphertext) + decryptor.finalize()

    # 去除填充并返回原始密码
    unpadded = padding.PKCS7(128).unpadder().update(decrypted) + padding.PKCS7(128).unpadder().finalize()
    return unpadded.decode()