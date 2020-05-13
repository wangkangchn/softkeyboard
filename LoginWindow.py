from PyQt5 import QtGui
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMainWindow, QApplication

from UI.Ui_LoginWindow import Ui_LoginWindow

if __name__ == '__main__':
    from utils import logger
    global log
    log = logger.setup_logger('logging.log')
else:
    log = None

class LoginWindow(QMainWindow, Ui_LoginWindow):

    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('吼吼吼哈哈哈 ... ')
        #LoginWindow.setStyleSheet("background-color: rgb(0, 67, 98);")
        # ~ window_pale = QtGui.QPalette()
        # ~ window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(r"pic\background.jpg")))
        # ~ self.setPalette(window_pale)

        # 将点击事件与槽函数进行连接
        self.btn_login.clicked.connect(self.slot_btn_login_clicked)
        self.btn_regist.clicked.connect(self.slot_btn_regist_clicked)

        self.le_user.installEventFilter(self)
        self.le_passwd.installEventFilter(self)

        # 最后一次点击的输入框
        self.now_editline = self.le_user

        self.set_log(log)

    def set_log(self, logger):
        """ 设置日志文件 """
        self.log = logger

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            self.log.debug('焦点进入: {}'.format(obj.objectName()))
            self.now_editline = obj

        elif event.type()== QEvent.FocusOut:
            pass
        return False

    def slot_btn_login_clicked(self):
        self.log.debug("点击登录按钮.")
        if self.le_user.text() == '':
            QMessageBox.warning(self, "警告！", "用户名不能为空！", QMessageBox.Yes)
            return

        if self.le_passwd.text().strip() == '':
            QMessageBox.warning(self, "警告！", "密码不能为空！", QMessageBox.Yes)
            return

        # 正确密码
        if (self.le_passwd.text().strip() == "1" and self.le_user.text() == "1"):
            QMessageBox.information(self, "登录", "密码正确, 确认登录.", QMessageBox.Yes)
            self.le_user.clear()
            self.le_passwd.clear()
            self.le_user.setFocus()
            return

        else:
            QMessageBox.warning(self, "警告！", "用户名或者密码错误！", QMessageBox.Yes)
            self.le_user.clear()
            self.le_passwd.clear()
            self.le_user.setFocus()
            return

    def slot_btn_regist_clicked(self):
        self.log.debug("点击注册按钮.")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = LoginWindow()
    mainWindow.show()
    sys.exit(app.exec_())
