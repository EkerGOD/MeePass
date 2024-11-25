# 操作数据库页面
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTreeWidgetItem
from PyQt5 import QtCore

from db import select_groups
from ui.static.operate_database import Ui_MainWindow as OperateDatabaseUI


class OperateDatabaseWindow(QtWidgets.QMainWindow):
    open_create_master_key_window = QtCore.pyqtSignal(str)


    def __init__(self, db_path):
        super(OperateDatabaseWindow, self).__init__()
        self.ui = OperateDatabaseUI()
        self.ui.setupUi(self)

        # 初始化数据
        self.db_path = db_path
        # 验证是否有db_path
        if db_path:
            print(db_path)
            rows = select_groups(db_path)
            self.update_groups_tree(rows)
        else:
            print("fail to load database")
            print(db_path)

        '''
        绑定事件
        '''
        # 菜单按钮
        self.ui.actionNew.triggered.connect(self.click_new)

        self.ui.group_treeWidget.itemClicked.connect(self.click_groups_tree)

    # 点击新建数据库
    def click_new(self):
        # 创建数据库提示
        reply = QMessageBox.information(self, "MeePass", """Your data will be stored in a KeePass database filewhich is a regular file. After clicking , you will beprompted to specify the location where KeePassshould save this file.
It is important that you remember where thedatabase file is stored.
You should regularly create a backup of the databasefile (onto an independent data storage device).""", QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)
        # 获取文件路径
        # 取消创建
        if reply != QMessageBox.Ok:
            return
        filepath, type = QFileDialog.getSaveFileName(self, "文件保存", "/database.db",
                                                         'db(*.db)')  # 前面是地址，后面是文件类型,得到输入地址的文件名和地址txt(*.txt*.xls);;image(*.png)不同类别
        print(f"create database path: {filepath}")

        self.open_create_master_key(filepath)


    # 打开创建主密码页面 发送信号
    def open_create_master_key(self, filepath):
        print("emit signal to open create master key window")
        self.open_create_master_key_window.emit(filepath)

    # 更新组树
    def update_groups_tree(self, rows):
        items = []
        root_row = rows[0]
        root = QTreeWidgetItem(self.ui.group_treeWidget)
        root.setText(0, root_row[1])
        items.append(root)
        for row in rows[1:]:
            item = QTreeWidgetItem(items[row[2]])
            item.setText(0, row[1])
            item.setIcon(0, QIcon('../icon/ic_fluent_book_add_24_filled.png'))
            items.append(row)

    def click_groups_tree(self, item, column):
        print(item, column)