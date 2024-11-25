# 创建主密码页面
from PyQt5 import QtWidgets
from zxcvbn import zxcvbn

from ui.static.create_master_key import Ui_Form as CreateMasterKeyUI
from utils.password import calculate_entropy_from_zxcvbn


class CreateMasterKeyWindow(QtWidgets.QWidget):
    def __init__(self, db_path):
        super(CreateMasterKeyWindow, self).__init__()
        self.ui = CreateMasterKeyUI()
        self.ui.setupUi(self)

        # 参数
        self.db_path = db_path

        # 设置内容
        self.ui.databasePath_label.setText(self.db_path)

        self.ui.OTP_widget.setVisible(False)

        # 初始化文本显示密码形式
        self.ui.masterPassword_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.repeadPassword_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)


        # 初始化密码强度条
        # self.ui.estimatedQuality_progressBar.setRange(0, 128)
        # self.ui.estimatedQuality_progressBar.setValue(0)

        # 绑定事件
        # cancel按钮
        self.ui.cancel_pushButton.clicked.connect(self.close)

        self.ui.showExpertOptions_checkBox.stateChanged.connect(self.show_expert_options_checkbox_state_change)

        self.ui.masterPassword_lineEdit.textChanged.connect(self.master_password_line_edit_change)

        self.ui.masterPassword_toolButton.clicked.connect(self.master_password_tool_button_click)

    def master_password_tool_button_click(self):
        if self.ui.masterPassword_lineEdit.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            self.ui.masterPassword_lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.ui.repeadPassword_lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.ui.masterPassword_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ui.repeadPassword_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

    # 展示专业选项复选框状态改变
    def show_expert_options_checkbox_state_change(self):
        if self.ui.showExpertOptions_checkBox.isChecked():
            self.ui.OTP_widget.setVisible(True)
        else:
            self.ui.OTP_widget.setVisible(False)

    def master_password_line_edit_change(self):
        # 获取 UI 控件
        progressbar = self.ui.estimatedQuality_progressBar
        master_password = self.ui.masterPassword_lineEdit.text()
        if master_password:
            # 计算密码熵
            result = zxcvbn(master_password)
            bits = calculate_entropy_from_zxcvbn(result)
        else:
            bits = 0

        # 设置进度条值（限制范围）
        limited_bits = max(0, min(bits, progressbar.maximum()))  # 限制进度条最大值

        progressbar.setValue(limited_bits)

        # 更新显示文本（允许超过进度条最大值）
        progressbar.setFormat(f"{bits} bits")  # bits 可以超过 progressbar.maximum()

        # 更新字符计数显示
        self.ui.char_label.setText(f"  {len(master_password)} ch.")

        self.update_gradient()

    def update_gradient(self):
        """根据当前进度更新渐变颜色"""
        value = self.ui.estimatedQuality_progressBar.value() / self.ui.estimatedQuality_progressBar.maximum()  # 转换为0到1的比例
        gradient_css = f"""
        QProgressBar::chunk {{
            background: qlineargradient(
                spread: pad,
                x1: 0, y1: 0.5, x2: 1, y2: 0.5,
                stop: 0 red,
                {f"stop: {0.5 / value} yellow" if value > 0.5 else f"stop: 1 rgba(255, {value / 0.5 * 255}, 0)" }
                {f"stop: 1 rgba({255 - (value - 0.5) / 0.5 * 255}, 255, 0)" if value > 0.5 else ""}
            );
        }}
        """
        self.ui.estimatedQuality_progressBar.setStyleSheet(gradient_css)