import os
import random
from io import BytesIO

import pyotp
import qrcode

from flask import Flask, send_file
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'

@app.route('/auth_otp/<string:otp>')
def auth_otp(otp):
    if have_otp():
        secret = get_secret()
        totp = pyotp.TOTP(secret)
        if not totp.verify(otp):
            print("Invalid OTP")
            # 返回错误加密代码
            return generate_encryption_code()
        # 返回正确加密代码
        return get_code()
    else:
        print("OTP doesn't exist")
        return generate_otp_and_code()

def get_secret():
    with open("totp_secret.txt", "r") as f:
        return f.read()

def get_code():
    with open("encryption_code.txt", "r") as f:
        return f.read()

def have_otp():
    if os.path.exists("totp_secret.txt"):
        return True
    return False

# 初始化全局 OTP 密钥
def generate_otp_secret():
    return pyotp.random_base32()

def generate_encryption_code():
    return str(random.randint(100000,999999))

# 根据secret制作qrcode
def make_qrcode(secret):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(secret)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def generate_otp_and_code():
    try:
        secret = generate_otp_secret()
        encryption_code = generate_encryption_code()

        # 写入文件
        with open("totp_secret.txt", "w") as f:
            f.write(secret)
        with open("encryption_code.txt", "w") as f:
            f.write(encryption_code)
        print("文件已创建")

    except Exception as e:
        print(f"创建或写入文件时发生错误：{e}")

    try:
        # 创建qrcode
        qr_img = make_qrcode(secret)
        buffer = BytesIO()
        qr_img.save(buffer, 'PNG')
        buffer.seek(0)

        # 将二维码保存到内存
        return send_file(
            buffer,
            mimetype='image/png',
            as_attachment=False,
            download_name='totp_secret.png'
        )
    except Exception as e:
        return f"生成二维码时发生错误：{e}", 500
