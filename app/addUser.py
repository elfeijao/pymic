# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/addUser.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_addUser(object):
    def setupUi(self, addUser):
        addUser.setObjectName("addUser")
        addUser.resize(400, 350)
        addUser.setMinimumSize(QtCore.QSize(400, 350))
        addUser.setMaximumSize(QtCore.QSize(400, 350))
        self.centralwidget = QtWidgets.QWidget(addUser)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 100, 341, 201))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.entry_cpf = QtWidgets.QLineEdit(self.layoutWidget)
        self.entry_cpf.setMinimumSize(QtCore.QSize(0, 25))
        self.entry_cpf.setObjectName("entry_cpf")
        self.gridLayout.addWidget(self.entry_cpf, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        self.comboBox_genre = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_genre.setMinimumSize(QtCore.QSize(0, 25))
        self.comboBox_genre.setObjectName("comboBox_genre")
        self.comboBox_genre.addItem("")
        self.comboBox_genre.addItem("")
        self.comboBox_genre.addItem("")
        self.gridLayout.addWidget(self.comboBox_genre, 1, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.entry_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.entry_name.setMinimumSize(QtCore.QSize(0, 25))
        self.entry_name.setObjectName("entry_name")
        self.gridLayout.addWidget(self.entry_name, 1, 0, 1, 2)
        self.date_birthDay = QtWidgets.QDateEdit(self.layoutWidget)
        self.date_birthDay.setMinimumSize(QtCore.QSize(0, 25))
        self.date_birthDay.setDate(QtCore.QDate(2018, 1, 1))
        self.date_birthDay.setCalendarPopup(True)
        self.date_birthDay.setObjectName("date_birthDay")
        self.gridLayout.addWidget(self.date_birthDay, 3, 1, 1, 2)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 401, 80))
        self.frame.setStyleSheet("background-color: #6a9b4a;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        addUser.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(addUser)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 28))
        self.menubar.setObjectName("menubar")
        addUser.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(addUser)
        self.statusbar.setObjectName("statusbar")
        addUser.setStatusBar(self.statusbar)

        self.retranslateUi(addUser)
        self.buttonBox.accepted.connect(addUser.register)
        self.buttonBox.rejected.connect(addUser.destroy)
        QtCore.QMetaObject.connectSlotsByName(addUser)

    def retranslateUi(self, addUser):
        _translate = QtCore.QCoreApplication.translate
        addUser.setWindowTitle(_translate("addUser", "Cadastro de Usuário"))
        self.label.setText(_translate("addUser", "Nome:"))
        self.entry_cpf.setPlaceholderText(_translate("addUser", "Insira o CPF"))
        self.label_4.setText(_translate("addUser", "Nascimento:"))
        self.comboBox_genre.setItemText(0, _translate("addUser", "Feminino"))
        self.comboBox_genre.setItemText(1, _translate("addUser", "Masculino"))
        self.comboBox_genre.setItemText(2, _translate("addUser", "Outro"))
        self.label_2.setText(_translate("addUser", "CPF:"))
        self.label_3.setText(_translate("addUser", "Gênero"))
        self.entry_name.setPlaceholderText(_translate("addUser", "Insira o nome do paciente"))
        self.date_birthDay.setDisplayFormat(_translate("addUser", "dd/MM/yyyy"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addUser = QtWidgets.QMainWindow()
    ui = Ui_addUser()
    ui.setupUi(addUser)
    addUser.show()
    sys.exit(app.exec_())

