# 添加主密码
import base64
import os
import sqlite3

import sql
from crypt import derive_key, aes_decryption, aes_encryption
from db import get_session
from models.passwords import Passwords


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
def add_password(db_path, master_password, cryption_code, title, username, password,url,notes ,group_id):
    salt = os.urandom(16)
    # 生成加密密钥
    key = derive_key(master_password + cryption_code, salt)
    print('key', key)
    # 加密密码
    encryption_password = aes_encryption(password, key)
    encryption_password = base64.b64encode(salt).decode() + ':' + encryption_password

    insert_password(db_path, title, username, encryption_password, url, notes, group_id)

# 获取密码
def get_password(db_path, master_password, cryption_code, username=None, encrypted_password=None):
    if username:
        row = select_password(db_path, username)
        if row:
            row = row[0]
    else:
        row = encrypted_password

    # print('row', row)
    salt, encrypted_password = row.split(":")
    # print(salt, encrypted_password)
    key = derive_key(master_password + cryption_code, base64.b64decode(salt))
    return aes_decryption(encrypted_password, key)

# 插入密码
def insert_password(db_path,title , username, password, url,  notes, group_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql.INSERT_PASSWORDS, (title, username, password, url, notes, group_id))
    conn.commit()
    conn.close()

# 查询密码
def select_password(db_name, username):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql.SELECT_PASSWORDS, (username,))
    row = cursor.fetchone()
    conn.close()
    return row

def select_passwords_by_group(group_id):
    session = get_session()
    rows = session.query(Passwords).filter(Passwords.group_id == group_id).all()
    return rows