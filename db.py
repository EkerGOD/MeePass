"""
数据库
"""
import base64
import os
import sqlite3

import config
import sql
from crypt import derive_key, aes_encryption, aes_decryption


# 添加密码
def add_password(db_path, master_password, cryption_code, account, password, group_id, notes):
    salt = os.urandom(16)
    # 生成加密密钥
    key = derive_key(master_password, cryption_code, salt)

    # 加密密码
    encryption_password = aes_encryption(password, key)
    encryption_password = base64.b64encode(salt).decode() + encryption_password

    insert_password(db_name, account, encryption_password, group_id, notes)


# 查看密码
def get_password(db_path, master_password, cryption_code, account):
    row = select_password(db_path, account, master_password)
    if row:
        salt, encrypted_password = row[0].split(":")
        key = derive_key(master_password, cryption_code, base64.b64decode(salt))
        return aes_decryption(encrypted_password, key)
    else:
        return None

def init_db(db_name, db_folder_path=config.DB_FOLDER_PATH):
    dbs_name = get_db(db_folder_path)
    if db_name not in dbs_name:
        db_path = os.path.join(db_folder_path, db_name)
        # print('DB_PATH:', db_path)
        create_db(db_path)

def get_db(folder_path):
    dbs = [file for file in os.listdir(folder_path) if file.endswith('.db')]
    return dbs

def create_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql.CREATE_PASSWORDS)
    cursor.execute(sql.CREATE_GROUPS)
    conn.commit()
    conn.close()

def insert_password(db_name, account, password, group_id, notes):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql.INSERT_PASSWORDS, (account, password, group_id, notes))
    conn.commit()
    conn.close()

def select_password(db_name, account, password):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql.SELECT_PASSWORDS, (account,))
    row = cursor.fetchone()
    conn.close()
    return row