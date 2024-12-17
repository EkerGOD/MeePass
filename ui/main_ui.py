
import sys
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet

from global_state import global_state
from ui.controller import Controller

#448aff

def main():
    app = QtWidgets.QApplication(sys.argv)

    # apply_stylesheet(app, theme='dark_blue.xml')
    app.aboutToQuit.connect(on_exit)
    # 启动中控
    controller = Controller()
    # 启动初始页面
    controller.show_open_database_window()
    sys.exit(app.exec_())

# 退出程序执行
def on_exit():
    # global_state.save()
    pass

if __name__ == '__main__':
    main()