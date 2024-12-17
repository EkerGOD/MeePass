from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from zxcvbn import zxcvbn

from db.password import add_password
from global_state import global_state
from ui.static.add_entry import Ui_Form as AddEntryUI
from utils.password import calculate_entropy_from_zxcvbn


class AddEntryWindow(QtWidgets.QWidget):
    def __init__(self, db_path):
        super(AddEntryWindow, self).__init__()
        self.ui = AddEntryUI()
        self.ui.setupUi(self)

        # 数值
        self.db_path = db_path

        self.ui.password_lineEdit.textChanged.connect(self.password_line_edit_change)

        self.ui.OK_pushButton.clicked.connect(self.ok_button_click)

        self.ui.cancel_pushButton.clicked.connect(self.close)

    def ok_button_click(self):
        title = self.ui.title_lineEdit.text()
        username = self.ui.username_lineEdit.text()
        password = self.ui.password_lineEdit.text()
        repeat_password = self.ui.repeat_lineEdit.text()
        url = self.ui.url_lineEdit.text()
        notes = self.ui.notes_textEdit.toPlainText()

        # 校验必填选项是否为空 password
        if not password:
            QMessageBox.critical(self, "密码不能为空", "密码不能为空，请重新输入后重试！", QMessageBox.Yes, QMessageBox.Yes)
            return

        # 校验两次密码是否正确
        if password != repeat_password:
            QMessageBox.critical(self, "密码错误", "输入密码不相同，请重新输入！", QMessageBox.Yes, QMessageBox.Yes)
            return

        add_password(
            db_path=self.db_path,
            master_password=global_state.get_temp('master_password'),
            cryption_code=global_state.get_temp('cryption_code'),
            title=title,
            username=username,
            password=password,
            url=url,
            notes=notes,
            group_id=global_state.get_temp('group_id'),
        )

        # 关闭自己
        self.close()


    def password_line_edit_change(self):
        # 获取 UI 控件
        progressbar = self.ui.quality_progressBar
        master_password = self.ui.password_lineEdit.text()
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
        value = self.ui.quality_progressBar.value() / self.ui.quality_progressBar.maximum()  # 转换为0到1的比例
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
        self.ui.quality_progressBar.setStyleSheet(gradient_css)