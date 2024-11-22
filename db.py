"""
数据库
"""
import os
import sqlite3

import config


def init_db(db_name):
    conn = sqlite3.connect('MeePass.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            ID INTEGER PRIMARY KEY,
            master_password TEXT NOT NULL,
            otp_secret TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db(folder_path):
    dbs = [file for file in os.listdir(folder_path) if file.endswith('.db')]
    return dbs

dbs = get_db(config.DB_FOLDER_PATH)
for db in dbs:
    print(db)

