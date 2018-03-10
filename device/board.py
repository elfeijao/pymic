from PyQt5.QtSerialPort import QSerialPort
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTextEdit

# Detect port Arduino
from PyQt5.QtSerialPort import QSerialPortInfo

class Board:
    def __init__( self, parent = None ):
        self.board = QSerialPort();
        port = QSerialPortInfo.availablePorts()[0].portName();
        print( "Connected port: ", port );
        self.board.setPortName(port);

    def board_destroy( self ):
        self.board.close();

    def on_board_read( self ):
        self.process_bytes( bytes(self.board.readAll()) );

    def process_bytes( self, bs ):
        print(bs);

    def board_connect( self ):
        if self.board.open(QtCore.QIODevice.ReadWrite):
            self.board.setBaudRate( 115200 );
            self.board.readyRead.connect(self.on_board_read);
            self.board.clear();
        else:
            raise IOError("Cannot connect to device on port {}".format(port));
