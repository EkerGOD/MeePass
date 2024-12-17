"""
主入口
"""
import logging

# def main():
#     group_id = 1
#     db_name = input('Enter database name: ')
#     db_path = os.path.join(config.DB_FOLDER_PATH, db_name)
#     # 初始化数据库
#     # 没有该数据库
#     if not init_db(db_name):
#         print(f"Create {db_name} Successfully!")
#         master_password = input("Please create master password:")
#         repeat_master_password = input("Please repeat the master password:")
#         if master_password != repeat_master_password:
#             return
#         add_master_password(db_path, master_password)
#
#     print("Welcome to your password manager!")
#
#
#
#     # 验证master password
#     master_password = input("Enter your master password: ")
#     if not authenticate_master_password(db_path, master_password):
#         print("Wrong master password!")
#         return
#     print("Authentication master password Successful!")
#
#
#
#     # 验证OTP
#     otp = input("Please enter your OTP: ")
#     response = authenticate_otp(otp)
#     if not response:
#         return
#     if not response['data']['is_otp_correct']:
#         print("Wrong OTP!")
#         return
#     print("Authentication OTP Successful!")
#     # 获取cryption_code
#     cryption_code = response['data']['cryption_code']
#
#     while True:
#         print("\n1. Add Password\n2. Get Password\n3. Exit")
#         choice = input("Choose an option: ")
#
#         if choice == "1":
#             account = input("Enter account name: ")
#             password = input("Enter password: ")
#             notes = input("Enter notes (optional): ")
#             add_password(db_path, master_password, cryption_code, account, password, group_id, notes)
#             print(f"Password for {account} added successfully.")
#
#         elif choice == "2":
#             account = input("Enter account name to retrieve: ")
#             password = get_password(db_path, master_password, cryption_code, account)
#             if password:
#                 print(f"Password for {account}: {password}")
#             else:
#                 print("Account not found.")
#
#         elif choice == "3":
#             print("Goodbye!")
#             break
#         else:
#             print("Invalid option.")

from ui import main_ui
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main_ui.main()
