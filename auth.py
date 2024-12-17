"""
验证代码
"""
import base64
import sqlite3

import pyotp
import requests

import config
from crypt import derive_key
from db.password import get_master_password


# 验证OTP
def authenticate_otp(otp:str):
    url = config.OTP_AUTH_URL + '/auth_otp/' + str(otp)
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# 验证主密码
def authenticate_master_password(db_path, master_password):
    stored_key = get_master_password(db_path)
    print("get master password")
    salt , stored_hashed_password = stored_key.split(':')
    key = derive_key(master_password, base64.b64decode(salt))
    derived_hashed_password = base64.b64encode(key).decode()
    if derived_hashed_password == stored_hashed_password:
        return True
    else:
        return False
