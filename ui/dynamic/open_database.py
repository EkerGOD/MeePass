# 打开数据库页面
import os
import re

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

from auth import authenticate_otp, authenticate_master_password
from ui.static.open_database import Ui_Form as OpenDatabaseUI
from utils.file import verify_dir_path


class OpenDatabaseWindow(QtWidgets.QWidget):

    # 创建信号
    switch_to_operate_database_window = QtCore.pyqtSignal(str)


    def __init__(self):
        super(OpenDatabaseWindow, self).__init__()
        self.ui = OpenDatabaseUI()
        self.ui.setupUi(self)
        # 初始化数据
        self.database_path = ""

        # 点击连接函数
        # ok按钮
        self.ui.OK_pushButton.clicked.connect(self.check_input)
        # cancel按钮
        self.ui.cancel_pushButton.clicked.connect(self.go_operate)

        # 选择文件路径按钮
        self.ui.databasePath_toolButton.clicked.connect(self.select_database)

    def check_input(self):

        self.database_path = self.ui.databasePath_lineEdit.text()
        master_password = self.ui.masterPassword_lineEdit.text()
        otp = self.ui.OTP_lineEdit.text()

        # 检验路径是否正确
        if not verify_dir_path(self.database_path):
            QMessageBox.critical(self, "非法数据库路径", "传入数据库路径非法，请重新输入后重试！", QMessageBox.Yes, QMessageBox.Yes)
            return

        if not master_password or not otp:
            QMessageBox.warning(self, "验证失败", "主密码和OTP不能为空！", QMessageBox.Yes, QMessageBox.Yes)
            return

        if not bool(re.match(r'^\d{6}$', otp)):
            QMessageBox.warning(self, "验证失败", "OTP必须为6位数字！", QMessageBox.Yes, QMessageBox.Yes)
            return

        response = authenticate_otp(otp)
        if not authenticate_master_password(self.database_path, master_password) or not response['data']['is_otp_correct']:
            QMessageBox.warning(self, "验证失败", "请检查主密码和OTP是否正确", QMessageBox.Yes, QMessageBox.Yes)
            return
        else:
            print("验证通过")

        self.go_operate()


    def select_database(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取数据库", os.getcwd(),
                                                                   "DB Files (*.db)")
        self.ui.databasePath_lineEdit.setText(fileName)

        print(fileName)

    def go_operate(self):
        # 函数发出信号
        self.switch_to_operate_database_window.emit(self.database_path)