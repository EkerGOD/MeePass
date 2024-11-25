
import sys
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet

from ui.controller import Controller

#448aff

def main():
    app = QtWidgets.QApplication(sys.argv)

    # apply_stylesheet(app, theme='dark_blue.xml')

    # 启动中控
    controller = Controller()
    # 启动初始页面
    controller.show_open_database_window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()