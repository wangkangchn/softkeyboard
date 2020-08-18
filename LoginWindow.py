from PyQt5 import QtGui
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget

from signal import *
from UI.Ui_LoginWindow import Ui_LoginWindow

if __name__ == '__main__':
    from utils import logger
    global log
    log = logger.setup_logger('logging.log')
else:
    log = None

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()  
        self.initUI()
               
    def initUI(self):               
        
        self.statusBar().showMessage('Ready')
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Statusbar')    


class LoginWindow(QWidget, Ui_LoginWindow):

    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('轮胎磨损检测程序')

        # 将点击事件与槽函数进行连接
        self.btn_login.clicked.connect(self.slot_btn_login_clicked)
        self.btn_regist.clicked.connect(self.slot_btn_regist_clicked)

        self.le_user.installEventFilter(self)
        self.le_passwd.installEventFilter(self)

        # 最后一次点击的输入框
        self.now_editline = self.le_user

        self.set_log(log)

        self.e = Example()

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
        # 发送信号
             
        if self.le_user.text() == '':
            QMessageBox.warning(self, "警告！", "用户名不能为空！", QMessageBox.Yes)
            return

        if self.le_passwd.text().strip() == '':
            QMessageBox.warning(self, "警告！", "密码不能为空！", QMessageBox.Yes)
            return

        # 正确密码
        if (self.le_passwd.text().strip() == "123456" and self.le_user.text() == "admin"):
            QMessageBox.information(self, "登录", "密码正确, 确认登录.", QMessageBox.Yes)
            self.le_user.clear()
            self.le_passwd.clear()
            self.le_user.setFocus()
            #############################################
            # TODO：
            #   在此处打开子窗口
            #############################################
            c.close_login.emit()
            self.e.show()

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
