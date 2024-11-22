"""
主入口
"""
import sqlite3
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

from auth import authenticate_otp


# 初始化数据库
def init_db():
    conn = sqlite3.connect('meepass.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            account TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            encrypted_salt TEXT NOT NULL,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()


# 生成加密密钥
def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(master_password.encode())

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

# 添加密码
def add_password(master_password, salt, account, password, notes=""):
    # 生成加密密钥
    key = derive_key(master_password, salt)

    # 使用加密的盐
    encrypted_salt = aes_encryption(salt.encode(), key)

    # 加密密码
    encrypted_password = aes_encryption(password, key)

    conn = sqlite3.connect('meepass.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO passwords (account, encrypted_password, encryption_salt, notes) 
        VALUES (?, ?, ?, ?)
    ''', (account, encrypted_password, encrypted_salt, notes))
    conn.commit()
    conn.close()


# 查看密码
def get_password(master_password, account):
    conn = sqlite3.connect('meepass.db')
    cursor = conn.cursor()
    cursor.execute('SELECT encrypted_password, encrypted_salt FROM passwords WHERE account = ?', (account,))
    row = cursor.fetchone()
    conn.close()
    if row:
        salt, encrypted_password = row[0].split(":")
        key = derive_key(master_password, base64.b64decode(salt))
        return aes_decryption(encrypted_password, key)
    else:
        return None


# 示例操作
if __name__ == '__main__':
    # 初始化数据库
    init_db()


    print("Welcome to your password manager!")
    otp = input("Please enter your OTP: ")
    master_password = input("Enter your master password: ")

    encryption_code = authenticate_otp(otp)
    while True:
        print("\n1. Add Password\n2. Get Password\n3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            account = input("Enter account name: ")
            password = input("Enter password: ")
            notes = input("Enter notes (optional): ")
            add_password(master_password, encryption_code, account, password, notes)
            print(f"Password for {account} added successfully.")

        elif choice == "2":
            account = input("Enter account name to retrieve: ")
            password = get_password(master_password, account)
            if password:
                print(f"Password for {account}: {password}")
            else:
                print("Account not found.")

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
