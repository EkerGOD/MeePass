"""
主入口
"""
import os
import base64
import config
from auth import authenticate_otp
from db import init_db, add_password, get_password

# 示例操作
if __name__ == '__main__':
    group_id = 1
    db_name = input('Enter database name: ')
    db_path = os.path.join(config.DB_FOLDER_PATH, db_name)
    # 初始化数据库
    init_db(db_name)


    print("Welcome to your password manager!")
    master_password = input("Enter your master password: ")
    otp = input("Please enter your OTP: ")

    cryption_code = authenticate_otp(otp)
    while True:
        print("\n1. Add Password\n2. Get Password\n3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            account = input("Enter account name: ")
            password = input("Enter password: ")
            notes = input("Enter notes (optional): ")
            add_password(db_path, master_password, cryption_code, account, password, group_id, notes)
            print(f"Password for {account} added successfully.")

        elif choice == "2":
            account = input("Enter account name to retrieve: ")
            password = get_password(db_path, master_password, cryption_code, account)
            if password:
                print(f"Password for {account}: {password}")
            else:
                print("Account not found.")

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
