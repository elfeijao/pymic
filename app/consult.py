# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/consult.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_consult(object):
    def setupUi(self, consult):
        consult.setObjectName("consult")
        consult.resize(575, 467)
        self.centralwidget = QtWidgets.QWidget(consult)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 100, 551, 311))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_search = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_search.setText("")
        self.label_search.setObjectName("label_search")
        self.gridLayout.addWidget(self.label_search, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.btn_consult = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_consult.setMinimumSize(QtCore.QSize(80, 28))
        self.btn_consult.setMaximumSize(QtCore.QSize(80, 28))
        self.btn_consult.setObjectName("btn_consult")
        self.gridLayout.addWidget(self.btn_consult, 0, 1, 1, 1)
        self.edit_cpf = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_cpf.setMinimumSize(QtCore.QSize(194, 28))
        self.edit_cpf.setMaximumSize(QtCore.QSize(194, 28))
        self.edit_cpf.setObjectName("edit_cpf")
        self.gridLayout.addWidget(self.edit_cpf, 0, 0, 1, 1)
        self.table_consult = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.table_consult.setAutoFillBackground(False)
        self.table_consult.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_consult.setDragDropOverwriteMode(False)
        self.table_consult.setGridStyle(QtCore.Qt.DashLine)
        self.table_consult.setObjectName("table_consult")
        self.table_consult.setColumnCount(2)
        self.table_consult.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_consult.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_consult.setHorizontalHeaderItem(1, item)
        self.table_consult.horizontalHeader().setCascadingSectionResizes(True)
        self.table_consult.horizontalHeader().setDefaultSectionSize(250)
        self.table_consult.horizontalHeader().setMinimumSectionSize(150)
        self.table_consult.horizontalHeader().setSortIndicatorShown(True)
        self.table_consult.horizontalHeader().setStretchLastSection(True)
        self.table_consult.verticalHeader().setVisible(True)
        self.table_consult.verticalHeader().setDefaultSectionSize(30)
        self.table_consult.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.table_consult, 1, 0, 1, 4)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 581, 80))
        self.widget.setStyleSheet("background-color: #6a9b4a;")
        self.widget.setObjectName("widget")
        consult.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(consult)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 575, 28))
        self.menubar.setObjectName("menubar")
        consult.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(consult)
        self.statusbar.setObjectName("statusbar")
        consult.setStatusBar(self.statusbar)

        self.retranslateUi(consult)
        self.btn_consult.clicked.connect(consult.on_btnSearch_clicked)
        self.table_consult.cellDoubleClicked['int','int'].connect(consult.on_modelIndex_clicked)
        QtCore.QMetaObject.connectSlotsByName(consult)

    def retranslateUi(self, consult):
        _translate = QtCore.QCoreApplication.translate
        consult.setWindowTitle(_translate("consult", "Consultar Exame"))
        self.btn_consult.setText(_translate("consult", "Pesquisar"))
        self.edit_cpf.setPlaceholderText(_translate("consult", "Insira o CPF do Cliente"))
        item = self.table_consult.horizontalHeaderItem(0)
        item.setText(_translate("consult", "Nome Paciente"))
        item = self.table_consult.horizontalHeaderItem(1)
        item.setText(_translate("consult", "Data do Exame"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    consult = QtWidgets.QMainWindow()
    ui = Ui_consult()
    ui.setupUi(consult)
    consult.show()
    sys.exit(app.exec_())

