from PyQt5.QtCore import Qt

from ui.dynamic.add_group import AddGroupWindow
from ui.dynamic.create_master_key import CreateMasterKeyWindow
from ui.dynamic.open_database import OpenDatabaseWindow
from ui.dynamic.operate_database import OperateDatabaseWindow
from ui.dynamic.add_entry import AddEntryWindow


class Controller:
    def __init__(self):
        pass

    def show_open_database_window(self):
        # 创建打开页面
        self.open_database_window = OpenDatabaseWindow()
        # 信号连接函数
        self.open_database_window.switch_to_operate_database_window.connect(self.show_operate_database_window)
        self.open_database_window.show()

    def show_operate_database_window(self, db_path):
        # 创建操作页面
        self.operate_database_window = OperateDatabaseWindow(db_path)
        # 会传出一个参数db_path
        self.operate_database_window.open_create_master_key_window.connect(self.show_create_master_key_window)
        self.operate_database_window.open_add_entry_window.connect(self.show_add_entry_window)
        self.operate_database_window.open_add_group_window.connect(self.show_add_group_window)

        self.open_database_window.close()
        self.operate_database_window.show()

    def show_create_master_key_window(self, db_path):
        print("controller get signal")
        self.create_master_key_window = CreateMasterKeyWindow(db_path)
        self.create_master_key_window.setWindowModality(Qt.ApplicationModal)
        self.create_master_key_window.show()

    def show_add_entry_window(self, db_path):
        self.add_entry_window = AddEntryWindow(db_path)
        self.add_entry_window.setWindowModality(Qt.ApplicationModal)
        self.add_entry_window.show()

    def show_add_group_window(self):
        self.add_group_window = AddGroupWindow()

        # 关闭页面的时候刷新页面
        self.add_group_window.on_close_add_group_window.connect(self.operate_database_window.update_groups_tree)

        self.add_group_window.setWindowModality(Qt.ApplicationModal)
        self.add_group_window.show()