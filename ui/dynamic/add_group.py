import logging

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

from db.group import insert_groups
from global_state import global_state
from ui.static.add_group import Ui_Form as AddGroupUI

logger = logging.getLogger(__name__)

class AddGroupWindow(QtWidgets.QWidget):
    # 关闭页面信号
    on_close_add_group_window = QtCore.pyqtSignal()

    def __init__(self):
        super(AddGroupWindow, self).__init__()
        self.ui = AddGroupUI()
        self.ui.setupUi(self)

        self.ui.OK_pushButton.clicked.connect(self.on_ok_button_clicked)

    def on_ok_button_clicked(self):
        logger.info("正在创建组...")
        name = self.ui.name_lineEdit.text()
        notes = self.ui.notes_textEdit.toPlainText()
        logger.info(f"创建组参数name: {name}, group_id: {global_state.get_temp('group_id')}, notes: {notes}")

        if not name:
            QMessageBox.critical(self, "组名称不能为空", "组名称不能为空，请重新输入后重试！", QMessageBox.Yes, QMessageBox.Yes)
            return

        if global_state.get_temp('group_id') is None:
            QMessageBox.critical(self, "请选择组父节点", "组父节点不存在，请选择父节点后重试！", QMessageBox.Yes,
                                 QMessageBox.Yes)
            return

        logger.info("验证组字段完毕")
        insert_groups(
            name=name,
            parent_id=global_state.get_temp('group_id'),
            notes=notes
        )

        # 发送关闭页面信号
        # 用于在主页面刷新页面
        self.on_close_add_group_window.emit()

        self.close()
        logger.info("创建组完毕")


