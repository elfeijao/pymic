# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/ui/DataCollect.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dataCollect(object):
    def setupUi(self, dataCollect):
        dataCollect.setObjectName("dataCollect")
        dataCollect.resize(991, 639)
        dataCollect.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(dataCollect)
        self.centralwidget.setObjectName("centralwidget")
        self.mpl_widget = QtWidgets.QWidget(self.centralwidget)
        self.mpl_widget.setGeometry(QtCore.QRect(0, 80, 991, 540))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mpl_widget.sizePolicy().hasHeightForWidth())
        self.mpl_widget.setSizePolicy(sizePolicy)
        self.mpl_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.mpl_widget.setMaximumSize(QtCore.QSize(991, 540))
        self.mpl_widget.setStyleSheet("background-color: #000;")
        self.mpl_widget.setObjectName("mpl_widget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 981, 80))
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 961, 41))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_stop = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_stop.setStyleSheet("")
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout.addWidget(self.btn_stop, 0, 4, 1, 1)
        self.edit_cpf = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_cpf.setMaximumSize(QtCore.QSize(200, 16777215))
        self.edit_cpf.setStyleSheet("")
        self.edit_cpf.setObjectName("edit_cpf")
        self.gridLayout.addWidget(self.edit_cpf, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.btn_start = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_start.setStyleSheet("")
        self.btn_start.setObjectName("btn_start")
        self.gridLayout.addWidget(self.btn_start, 0, 3, 1, 1)
        self.btn_save = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_save.setStyleSheet("")
        self.btn_save.setObjectName("btn_save")
        self.gridLayout.addWidget(self.btn_save, 0, 1, 1, 1)
        dataCollect.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(dataCollect)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 991, 24))
        self.menubar.setObjectName("menubar")
        dataCollect.setMenuBar(self.menubar)

        self.retranslateUi(dataCollect)
        self.btn_save.clicked.connect(dataCollect.on_btn_save)
        self.btn_start.clicked.connect(dataCollect.on_btn_start)
        self.btn_stop.clicked.connect(dataCollect.on_btn_stop)
        QtCore.QMetaObject.connectSlotsByName(dataCollect)

    def retranslateUi(self, dataCollect):
        _translate = QtCore.QCoreApplication.translate
        dataCollect.setWindowTitle(_translate("dataCollect", "Analisador"))
        self.btn_stop.setText(_translate("dataCollect", "Parar"))
        self.edit_cpf.setPlaceholderText(_translate("dataCollect", "Insira o CPF do usuário"))
        self.btn_start.setText(_translate("dataCollect", "Iniciar"))
        self.btn_save.setText(_translate("dataCollect", "Salvar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dataCollect = QtWidgets.QMainWindow()
    ui = Ui_dataCollect()
    ui.setupUi(dataCollect)
    dataCollect.show()
    sys.exit(app.exec_())

