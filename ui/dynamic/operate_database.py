# 操作数据库页面
import logging

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTreeWidgetItem, QTableWidgetItem, QTableWidget, QApplication
from PyQt5 import QtCore

from db.password import select_passwords_by_group, get_password
from db.group import select_groups, delete_groups
from global_state import global_state
from ui.static.operate_database import Ui_MainWindow as OperateDatabaseUI

logger = logging.getLogger(__name__)

class OperateDatabaseWindow(QtWidgets.QMainWindow):
    open_create_master_key_window = QtCore.pyqtSignal(str)
    open_add_entry_window = QtCore.pyqtSignal(str)
    open_add_group_window = QtCore.pyqtSignal()

    def __init__(self, db_path):
        super(OperateDatabaseWindow, self).__init__()
        logger.info("OperateDatabaseWindow 开始初始化")
        self.ui = OperateDatabaseUI()
        self.ui.setupUi(self)

        # 初始化数据
        self.db_path = db_path
        # 验证是否有db_path
        logger.info(f"验证db_path: {self.db_path}")
        if db_path:
            self.update_groups_tree()
        else:
            print("fail to load database")
            print(db_path)

        # 初始化数据
        global_state.set_temp('db_path', db_path)
        # 初始化界面
        self._init_ui()
        #初始化事件
        self._init_event()
        logger.info("初始化OperateDatabaseWindow 初始化完毕")

    def _init_ui(self):
        # 初始化界面
        # 禁止编辑
        self.ui.password_tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        # 选择整行
        self.ui.password_tableWidget.setSelectionBehavior(QTableWidget.SelectRows)

        self.ui.password_tableWidget.setStyleSheet("""
        QTreeWidget::item:selected {
            background-color: lightblue;  /* 设置选中背景色 */
            color: black;  /* 设置选中文字颜色 */
        }
        """)

    def _init_event(self):
        # 菜单按钮
        self.ui.actionNew.triggered.connect(self.click_new)

        # 点击树事件
        self.ui.group_treeWidget.itemClicked.connect(self.click_groups_tree)

        # 点击创建新密码按钮
        self.ui.actionAdd_Entry.triggered.connect(self.add_entry)

        self.ui.actionAdd_Group.triggered.connect(self.add_group)

        self.ui.password_tableWidget.cellDoubleClicked.connect(self.on_double_click_table_cell)

        self.ui.actionDelete_Group.triggered.connect(self.delete_group)

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

    def add_entry(self):
        self.open_add_entry_window.emit(self.db_path)

    def add_group(self):
        self.open_add_group_window.emit()
        self.update_groups_tree()

    def delete_group(self):
        if global_state.get_temp('group_id') is None:
            QMessageBox.critical(self, "未选择删除组", "未选择删除组，请选择后重试！", QMessageBox.Yes,
                                 QMessageBox.Yes)
            return

        delete_groups(global_state.get_temp('group_id'))
        self.update_groups_tree()

    # 更新组树
    def update_groups_tree(self):
        logger.info("更新组树")
        # 清空组树
        self.ui.group_treeWidget.clear()
        # 获取组数据
        rows = select_groups()
        self.rows = rows
        global_state.set_temp('tree_rows', rows)
        items = []
        root_row = rows[0]
        root = QTreeWidgetItem(self.ui.group_treeWidget)
        root.setText(0, root_row.name)
        items.append(root)
        for row in rows[1:]:
            logger.info(f"正在加载第 {row.id} 组 {row.name}, 父节点为 {row.parent_id}")
            # print(items)
            item = QTreeWidgetItem(items[row.parent_id])
            item.setText(0, row.name)
            # item.setIcon(0, QIcon('../icon/ic_fluent_book_add_24_filled.png'))
            items.append(item)

        # 设置默认选择
        self.ui.group_treeWidget.setCurrentItem(root)
        logger.info("更新组树完毕")

    def click_groups_tree(self, item, column):
        name = item.text(column)
        for row in self.rows:
            if row.name == name:
                global_state.set_temp('group_id', row.id)
                # 更新table
                self.password_rows = select_passwords_by_group(row.id)
                self.refresh_table(self.password_rows)

    # 刷新table
    def refresh_table(self, rows):
        # 清空表格
        self.ui.password_tableWidget.setRowCount(0)

        # 填充新数据
        for row_idx, row_data in enumerate(rows):
            self.ui.password_tableWidget.insertRow(row_idx)  # 插入一行
            self.ui.password_tableWidget.setItem(row_idx, 0, QTableWidgetItem(row_data.title))
            self.ui.password_tableWidget.setItem(row_idx, 1, QTableWidgetItem(row_data.username))
            self.ui.password_tableWidget.setItem(row_idx, 2, QTableWidgetItem("******"))
            self.ui.password_tableWidget.setItem(row_idx, 3, QTableWidgetItem(row_data.url))
            self.ui.password_tableWidget.setItem(row_idx, 4, QTableWidgetItem(row_data.notes))

    def on_double_click_table_cell(self, row, column):
        encrypted_password = self.password_rows[row].password
        print(encrypted_password)
        password = get_password(
            db_path=self.db_path,
            master_password=global_state.get_temp('master_password'),
            cryption_code=global_state.get_temp('cryption_code'),
            encrypted_password=encrypted_password
        )
        print(password)
        clipboard = QApplication.clipboard()
        clipboard.setText(password)
        # print(row, column)
        print(password)