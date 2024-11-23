"""
验证代码
"""
import sqlite3

import pyotp
import requests

import config


def authenticate_master_password(master_password, stored_password, otp_secret):
    # 验证主密码
    if master_password != stored_password:
        print("Invalid master password")
        return False

    otp = input("Enter your OTP: ")
    totp = pyotp.TOTP(otp_secret)
    if not totp.verify(otp):
        print("Invalid OTP")
        return False

    print("Authentication successful!")
    return True

# 设置主密码和OTP
def setup_master_password():
    master_password = input("Set your master password:")

    conn = sqlite3.connect('mee_pass.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO settings (master_password, otp_secret) VALUES (?, ?)',
                   (master_password))
    conn.commit()
    conn.close()

# 获取主密码和OTP密钥
def get_master_settings(master_password, otp_secret):
    conn = sqlite3.connect('mee_pass.db')
    cursor = conn.cursor()
    cursor.execute('SELECT master_password, otp_secret FROM settings VALUES (?, ?) LIMIT 1',
                   (master_password, otp_secret))
    row = cursor.fetchone()
    conn.close()
    return row

# 验证OTP
def authenticate_otp(otp:str):
    url = config.OTP_AUTH_URL + '/auth_otp/' + str(otp)
    response = requests.get(url)

    if response.status_code == 200:
        print("Authentication successful!")
        return response.json()
    else:
        print("Invalid OTP")
        return None

# # 验证主密码
# def authenticate_master_password():
#
