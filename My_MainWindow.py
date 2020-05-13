# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'index.ui'
#!/usr/bin/env python3"
# File Name: My_MainWindow.py
# Author: wkangk
# Mail: wangkangchn@163.com
# Created Time: 2020-05-12 20:22:41 中国标准时间
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All slot_switch_keyboards made in this file will be lost!
#
import cv2 as cv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtCore import QCoreApplication

from LoginWindow import LoginWindow
from SoftKeyBoard import SoftKeyBoard

from utils import logger

global log
log = logger.setup_logger('logging.log')

class My_MainWindow:

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.config_window()
        self.set_slot_func()

        # 设置配置文件
        self.soft_keybord.set_log(log)
        self.login_window.set_log(log)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hello World (*^▽^*)"))

    def config_window(self):
        # 垂直布局
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # 分隔主窗口 上按钮, 下图片
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        # 外层竖向弹簧
        self.verticalLayout.addWidget(self.splitter)

        self.login_window = LoginWindow()
        self.soft_keybord = SoftKeyBoard()
        self.splitter.addWidget(self.login_window)         # 弹簧上面

    def set_slot_func(self):
        """ 配置槽函数 """
        # 登录窗口与键盘联动
        self.login_window.btn_keyboard.clicked.connect(self.slot_switch_keyboard)
        self.soft_keybord.signal_send_text.connect(self.slot_recive_key)

        self.switch_keybord = False     # 控制键盘的开启

    def slot_switch_keyboard(self):
        """ 显示关闭软键盘 """
        self.switch_keybord = not self.switch_keybord
        if not self.switch_keybord:
            self.splitter.widget(1).setParent(None)
        else:
            self.splitter.insertWidget(1, self.soft_keybord)

        # 显示光标
        self.login_window.now_editline.setFocus()

    def processing_func_key(self, text):
        """ 处理功能键 """
        if text == 'up':
            self.login_window.focusPreviousChild()

        elif text == 'down':
            self.login_window.focusNextChild()

        elif text == 'left':
            self.login_window.now_editline.cursorBackward(False, 1)

        elif text == 'right':
            self.login_window.now_editline.cursorForward(False, 1)

        elif text == 'backspace':
            self.login_window.now_editline.backspace()

        elif text == 'enter':
            if self.login_window.btn_keyboard.hasFocus():   # 隐藏键盘
                # ~ self.slot_switch_keyboard()
                pass

            elif self.login_window.btn_login.hasFocus():    # 登录
                self.login_window.slot_btn_login_clicked()

            elif self.login_window.btn_regist.hasFocus():   # 注册
                self.login_window.slot_btn_regist_clicked()

            elif self.login_window.le_user.hasFocus():      # 在用户框时进入密码框
                self.login_window.focusNextChild()

            elif self.login_window.le_passwd.hasFocus():    # 在密码框时登录
                self.login_window.focusNextChild()
                self.login_window.slot_btn_login_clicked()

        elif text == 'clear':
            self.login_window.now_editline.clear()

    def slot_recive_key(self, text):
        """ 接收键盘发来的信息, 并发送到相应输入框 """
        if len(text) == 1:  # 非功能键
            self.login_window.now_editline.insert(text)
        else:
            self.processing_func_key(text)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = My_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())


