"""
数据库
"""
import base64
import os
import sqlite3

import config
import sql
from crypt import derive_key, aes_encryption, aes_decryption

# 添加主密码
def add_master_password(db_path, master_password):
    salt = os.urandom(16)
    key = derive_key(master_password, salt)
    key = base64.b64encode(salt).decode() + ':' + base64.b64encode(key).decode()
    insert_password(db_path, 'master_password', key, 0, '')

# 获取主密码
def get_master_password(db_path):
    row = select_password(db_path, 'master_password')
    if row:
        return row[0]
    return None

# 添加密码
def add_password(db_path, master_password, cryption_code, account, password, group_id, notes):
    salt = os.urandom(16)
    # 生成加密密钥
    key = derive_key(master_password + cryption_code, salt)
    print('key', key)
    # 加密密码
    encryption_password = aes_encryption(password, key)
    encryption_password = base64.b64encode(salt).decode() + ':' + encryption_password

    insert_password(db_path, account, encryption_password, group_id, notes)

# 获取密码
def get_password(db_path, master_password, cryption_code, account):
    row = select_password(db_path, account)
    if row:
        salt, encrypted_password = row[0].split(":")
        key = derive_key(master_password + cryption_code, base64.b64decode(salt))
        return aes_decryption(encrypted_password, key)
    else:
        return None

# 初始化数据库
def init_db(db_name, db_folder_path=config.DB_FOLDER_PATH):
    dbs_name = get_db(db_folder_path)
    if db_name not in dbs_name:
        db_path = os.path.join(db_folder_path, db_name)
        # print('DB_PATH:', db_path)
        create_db(db_path)
        return False
    return True

# 获取已知数据库
def get_db(folder_path):
    dbs = [file for file in os.listdir(folder_path) if file.endswith('.db')]
    return dbs

# 创建数据库
def create_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql.CREATE_PASSWORDS)
    cursor.execute(sql.CREATE_GROUPS)
    conn.commit()
    conn.close()

# 插入密码
def insert_password(db_path, account, password, group_id, notes):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql.INSERT_PASSWORDS, (account, password, group_id, notes))
    conn.commit()
    conn.close()

# 查询密码
def select_password(db_name, account):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql.SELECT_PASSWORDS, (account,))
    row = cursor.fetchone()
    conn.close()
    return row