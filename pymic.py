# -*- coding: utf-8 -*-

# Logger
import logging
from app import logger

import scipy.signal
import numpy as np
np.set_printoptions(threshold=1000000000);

# Matplotlib QT5
import matplotlib
import matplotlib.animation as animation
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
plt.style.use('dark_background');

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Splash Screen
from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtGui import QPixmap

# Local
from app.default import *
from app.addUser import *
from app.dataCollect import *
from app.consult import *
from app.examDetail import *
from model.db import *
from device.board import *

class SerialDebug( QtWidgets.QWidget, Board ):
    ''' This work like serial monitor from Arduino. 
        You can read the serial port to analise the datas '''
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent);
        self.setup();
        try:
            Board.__init__(self);
            self.board_connect();
        except:
            QtWidgets.QMessageBox.warning(self, 'Erro ao detectar o Hardware', 'Dispositivo desconectado!', QtWidgets.QMessageBox.Yes);

    def setup(self):
        # Configure Window
        self.resize(255, 190)
        self.move(550, 300)

        # Configure TextEdit
        self.te = QtWidgets.QTextEdit(self);
        self.te.setAcceptRichText(False)
        self.te.setReadOnly(False)
        self.te.setObjectName('serialMonitor')

    #overwrite QWidget
    def closeEvent(self, event):
        self.board_destroy();
        event.accept();

    # overwrite Board
    def process_bytes(self, bs):
        tc = self.te.textCursor()

        while tc.movePosition(QtGui.QTextCursor.Down):
            pass

        for b in bs:
            if b == 8:  # \b
                tc.movePosition(QtGui.QTextCursor.Left);
                self.te.setTextCursor(tc);
            elif b == 13:  # \r
                pass
            else:
                tc.deleteChar();
                self.te.setTextCursor(tc);
                self.te.insertPlainText(chr(b));
        self.te.ensureCursorVisible()

class Exam( QtWidgets.QMainWindow, Ui_dataCollect, Board ):
    ''' Plot datas from serial port '''
    def __init__( self, parent=None, data="" ):
        QtWidgets.QMainWindow.__init__( self, parent );
        self.setupUi( self );
        Board.__init__( self );

        self.initialize_vars();
        self.configureWidgetDraw( self.mpl_widget );

        self.ani = animation.FuncAnimation( self.fig, self.refreshPlot, interval=100 );
        try:
            self.db = DB();
        except Exception as e:
            logging.critical( "Houve um erro com a conexao de banco de dados: " + str(e) );
            raise e

    def initialize_vars(self):
        self.keep_data = "";

        self.xpressure_volume = np.array([0]);
        self.ypressure_volume = np.array([0]);

        self.xpressure_flow = np.array([0]);
        self.ypressure_flow = np.array([0]);

        self.xdata = np.array([0]);
        self.ydata = np.array([0]);
        self.flow = np.array([0]);

        self.pressure_xdata = np.array([0]);
        self.pressure_ydata = np.array([0]);

        self.xmax_fsr402 = 0;
        self.ymax_fsr402 = 0;
        self.xmax_yfs201 = 0;
        self.ymax_yfs201 = 0;


    def configureWidgetDraw( self, parent ):
        self.fig = Figure(figsize=(10,5.5));
        self.fig.subplots_adjust(bottom=0.1, top=0.95, left=0.07, right=0.97)

        self.axes = self.fig.add_subplot( 211 );
        self.axes.grid(linewidth=0.1);
        self.axes.set_ylim( [0,400] );
        self.axes.set_ylabel('ml');
        self.axes.set_xlabel('s');

        self.axes2 = self.fig.add_subplot( 212 );
        self.axes2.grid(linewidth=0.1);
        self.axes2.set_xlim( [0,1200] );
        self.axes2.set_ylim( [0,100] );
        self.axes2.set_ylabel('ml/s');
        self.axes2.set_xlabel('s');

        self.line, = self.axes.plot( [],[], animated=True );
        self.line2, = self.axes2.plot( [],[], animated=True );

        self.canvas = FigureCanvas( self.fig );
        self.canvas.setParent( parent );

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding);
        FigureCanvas.updateGeometry(self);

    def closeEvent(self, event):
        self.board_destroy();
        event.accept();

    def refreshPlot(self, i):
        self.axes.legend( ["Volume YFS-201", "Volume FSR-402"] );
        self.axes2.legend( ["Fluxo YFS-201", "Fluxo FSR-402"] );

        self.axes.grid(linewidth=0.1);
        self.axes.set_ylim( [0,400] );
        self.axes.set_xlim( [0,30] );
        self.axes.set_ylabel('ml');
        self.axes.set_xlabel('s');
        self.axes.plot( self.xpressure_volume, self.ypressure_volume, '#00FFFF', linewidth=0.15 );
        self.axes.plot( self.xdata, self.ydata, '#00FF00', linewidth=0.15 );

        self.axes2.grid(linewidth=0.1);
        self.axes2.set_ylim( [0,100] );
        self.axes2.set_xlim( [0,30] );
        self.axes2.set_ylabel('ml/s');
        self.axes2.set_xlabel('s');
        self.axes2.plot( self.xpressure_flow, self.ypressure_flow, '#00FFFF', linewidth=0.15 );
        self.axes2.plot( self.xdata, self.flow, '#00FF00', linewidth=0.15 );

        return self.line, self.line2;

    def validData(self, data):
        try:
            self.keep_data += data.decode().replace('\n', '').replace('\r', '');
            aux = self.keep_data;

            data_serial_splited = aux.split(";");
            size_data = len(data_serial_splited);        
            if( size_data > 1 ):
                data_serial_splited = aux.split(';')[0:size_data-1];
                self.keep_data = str(aux.split(';')[size_data-1]);
                return data_serial_splited;
            else:
                self.keep_data = str(data_serial_splited);
                return "";
        except Exception as e:
                logging.critical( "Houve um erro na leitura: " + str(e) );
                return "";

            

    #override Board
    # Sempre que tem um dado na porta serial esse funcao eh chamada. 
    # Tem que existir um comp rapido o suficiente para fazer a leitura
    def process_bytes(self, bs):
        data_serial_collected = self.validData( bs );	

        for data_serial in data_serial_collected:
            if data_serial:
                if( data_serial[0] == "f" ):
                    data = data_serial.replace( "f ", "" );
                    try: 
                        xdata,ydata = data.split(",");

                        self.flow = np.append( self.flow, (float( ydata )-self.ydata[-1])/0.25  );
                        self.ydata = np.append(self.ydata, float(ydata));
                        self.xdata = np.append(self.xdata, float(xdata));

                        if float(ydata) > self.ymax_yfs201:
                            self.ymax_yfs201 = float(ydata);
                            self.xmax_yfs201 = float(xdata)

                    except Exception as e:
                        logging.critical( "Houve um erro na plotagem: " + str(e) );

                if( data_serial[0] == "p" ):
                    data = data_serial.replace("p ", "");
                    try:
                        xdata, ydata = data.split(",");

                        self.xpressure_flow = np.append( self.xpressure_flow, float(xdata) );
                        self.ypressure_flow = np.append( self.ypressure_flow, (float(ydata) - self.ypressure_volume[-1])/0.02 );


                        self.xpressure_volume = np.append( self.xpressure_volume, float(xdata) );
                        self.ypressure_volume = np.append( self.ypressure_volume, float(ydata) );

                        if float(ydata) > self.ymax_fsr402:
                            self.ymax_fsr402 = float(ydata);
                            self.xmax_fsr402 = float(xdata)

                    except Exception as e:
                        logging.critical( "Houve um erro na plotagem: " + str(e) );

    def on_btn_start( self ):
        self.board_connect();

    def on_btn_stop( self ):
        self.board_destroy();

    def on_btn_save( self ):
        cpf = self.edit_cpf.text();

        yfs201_xflow = np.array2string( self.xdata );
        yfs201_yflow = np.array2string( self.flow );

        yfs201_xvolume = np.array2string( self.xdata );
        yfs201_yvolume = np.array2string( self.ydata );

        fsr402_xflow = np.array2string( self.xpressure_flow );
        fsr402_yflow = np.array2string( self.ypressure_flow );

        fsr402_xvolume = np.array2string( self.xpressure_volume );
        fsr402_yvolume = np.array2string( self.ypressure_volume );

        pressure_xdata = np.array2string( self.xpressure_volume );
        pressure_ydata = np.array2string( self.ypressure_volume );

        exam_data = yfs201_xvolume + ";" + yfs201_yvolume + "_" + fsr402_xvolume  + ";" + fsr402_yvolume + "_";
        exam_data+= yfs201_xflow + ";" + yfs201_yflow + "_" + fsr402_xflow + ";" + fsr402_yflow; 

        #print(exam_data);

        try:
            self.db.insertExam( cpf, exam_data );
            QtWidgets.QMessageBox.information(self, 'Exame Salvo', 'Exame salvo com sucesso!', QtWidgets.QMessageBox.Yes);
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'Erro em salvar o exame do usuario', QtWidgets.QMessageBox.Yes);
            loggin.critical( "Houve um erro ao salvar o exame do usuario. " );

class ExamDetail( QtWidgets.QMainWindow, Ui_examDetail ):
    ''' Plot datas from serial port '''
    def __init__( self, parent=None, data=None ):
        QtWidgets.QMainWindow.__init__( self, parent );
        self.setupUi( self );

        if data != None:
            yfs201_volume = str( data[5] ).split("_")[0];
            fsr402_volume = str( data[5] ).split("_")[1];
            yfs201_flow = str( data[5] ).split("_")[2];
            fsr402_flow = str( data[5] ).split("_")[3];

            str_yfs201_xvolume, str_yfs201_yvolume = yfs201_volume.split(';');
            str_fsr402_xvolume, str_fsr402_yvolume = fsr402_volume.split(';');
            str_yfs201_xflow, str_yfs201_yflow = yfs201_flow.split(';');
            str_fsr402_xflow, str_fsr402_yflow = fsr402_flow.split(';');

            str_yfs201_xvolume = str_yfs201_xvolume.replace(']','');
            str_yfs201_xvolume = str_yfs201_xvolume.replace('[','');
            str_yfs201_yvolume = str_yfs201_yvolume.replace(']','');
            str_yfs201_yvolume = str_yfs201_yvolume.replace('[','');

            str_fsr402_xvolume = str_fsr402_xvolume.replace('[','');
            str_fsr402_xvolume = str_fsr402_xvolume.replace(']','');
            str_fsr402_yvolume = str_fsr402_yvolume.replace('[','');
            str_fsr402_yvolume = str_fsr402_yvolume.replace(']','');

            str_yfs201_xflow = str_yfs201_xflow.replace('[', '');
            str_yfs201_xflow = str_yfs201_xflow.replace(']', '');
            str_yfs201_yflow = str_yfs201_yflow.replace('[', '');
            str_yfs201_yflow = str_yfs201_yflow.replace(']', '');

            str_fsr402_xflow = str_fsr402_xflow.replace('[', '');
            str_fsr402_xflow = str_fsr402_xflow.replace(']', '');
            str_fsr402_yflow = str_fsr402_yflow.replace('[', '');
            str_fsr402_yflow = str_fsr402_yflow.replace(']', '');

            self.yfs201_xvolume = np.fromstring( str_yfs201_xvolume, dtype=float, sep=' '); 
            self.yfs201_yvolume = np.fromstring( str_yfs201_yvolume, dtype=float, sep=' '); 
            self.fsr402_xvolume = np.fromstring( str_fsr402_xvolume, dtype=float, sep=' ');
            self.fsr402_yvolume = np.fromstring( str_fsr402_yvolume, dtype=float, sep=' ');

            self.yfs201_xflow = np.fromstring( str_yfs201_xflow, dtype=float, sep=' '); 
            self.yfs201_yflow = np.fromstring( str_yfs201_yflow, dtype=float, sep=' '); 
            self.fsr402_xflow = np.fromstring( str_fsr402_xflow, dtype=float, sep=' ');
            self.fsr402_yflow = np.fromstring( str_fsr402_yflow, dtype=float, sep=' ');

            self.label_name.setText( data[0] );
            self.label_genr.setText( data[1] );
            self.label_cpf.setText( str(data[2]) );
            self.label_date.setText( data[6] );

            self.yfs201_ymax = max( self.yfs201_yflow );
            index = self.yfs201_yflow.argmax()
            self.yfs201_xmax = self.yfs201_xflow[index];

            self.fsr402_ymax = max( self.fsr402_yflow );
            index = self.fsr402_yflow.argmax()
            self.fsr402_xmax = self.fsr402_xflow[index];

            qmean = 0;
            cont = 0;
            for i in self.fsr402_yflow:
                if i > 10:
                    cont += 1;
                    qmean += i;

            #qmean /= len( self.fsr402_yflow );
            qmean /= cont;

            self.label_data_qmax.setText( str( self.fsr402_ymax ) );
            self.label_data_tqmax.setText( str( self.fsr402_xmax ) );
            self.label_data_qmean.setText( str(round(qmean,2)) );

        else:
            self.xdata = [];
            self.ydata = [];
            
        self.setupMpl( self.mpl_widget );

    def setupMpl( self, parent ):
        self.fig = Figure(figsize=(10,5.5));
        self.fig.subplots_adjust(bottom=0.1, top=0.95, left=0.07, right=0.97)

        self.axes = self.fig.add_subplot( 211 );
        self.axes.grid(linewidth=0.1);
        self.axes2 = self.fig.add_subplot( 212 );
        self.axes2.grid(linewidth=0.1);
        #self.axes.set_xlim( [0,1200] );
        self.axes.set_ylim( [0,400] );
        self.axes2.set_ylim( [0,100] );

        self.compute_initial_figure();

        self.canvas = FigureCanvas( self.fig );
        self.canvas.setParent( parent );

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding);
        FigureCanvas.updateGeometry(self);

    def compute_initial_figure( self ):
        self.axes.set_ylabel('ml');
        self.axes.set_xlabel('s');

        self.axes2.set_ylabel('ml/s');
        self.axes2.set_xlabel('s');

        self.axes.plot( self.yfs201_xvolume, self.yfs201_yvolume, "#00FFFF", linewidth=0.5 );
        self.axes.plot( self.fsr402_xvolume, self.fsr402_yvolume, "#00FF00", linewidth=0.5 );

        self.axes2.plot( self.yfs201_xflow, self.yfs201_yflow, "#00FFFF", linewidth=0.5 );
        self.axes2.plot( self.fsr402_xflow, self.fsr402_yflow, "#00FF00", linewidth=0.5 );

        self.axes.legend( ["Volume YFS-201", "Volume FSR-402"] );
        self.axes2.legend( ["Fluxo YFS-201", "Fluxo FSR-402"] );
        
        self.axes2.plot( self.yfs201_xmax, self.yfs201_ymax, 'or')
        self.axes2.plot( self.fsr402_xmax, self.fsr402_ymax, 'or')
        self.axes2.annotate('QMax = '+str(self.yfs201_ymax), xy=(self.yfs201_xmax, self.yfs201_ymax), xytext=(self.yfs201_xmax-10, self.yfs201_ymax-1), arrowprops=dict(facecolor='black', shrink=0.05));

        self.axes2.annotate('QMax = '+str(self.fsr402_ymax), xy=(self.fsr402_xmax, self.fsr402_ymax), xytext=(self.fsr402_xmax-10, self.fsr402_ymax-1), arrowprops=dict(facecolor='black', shrink=0.05));

        self.axes.annotate('YF-S201 Volume Máx = '+str(max(self.yfs201_yvolume)), xy=(0.5, 400-200));
        self.axes.annotate('FSR-402 Volume Máx = '+str(max(self.fsr402_yvolume)), xy=(0.5, 400-250));

class ConsultWindow( QtWidgets.QMainWindow, Ui_consult ):
    def __init__( self, parent=None ):
        super(ConsultWindow, self).__init__(parent);
        self.setupUi(self);
        try:
            self.db = DB();
        except Exception as e:
            logging.critical( "Houve um erro com a conexao de banco de dados: " + str(e) );
            raise e

    def on_btnSearch_clicked( self ):
        cpf = self.edit_cpf.text();

        if self.db.checkUser( cpf ):
            rows = self.db.consult( cpf );

            for row in rows:
                rowPosition = self.table_consult.rowCount()
                self.table_consult.insertRow(rowPosition)
                self.table_consult.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem( row[0] ))
                self.table_consult.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem( row[1] ))
                #self.listConsult.addItem( row[0] );'''
            self.label_search.setText( "Sucesso!" );
        else:
            self.label_search.setText( "Usuário não encontrado!" );

    def on_modelIndex_clicked( self, index ):
        cpf = self.edit_cpf.text();
        try:
            for row in self.db.specificConsult( cpf, index ):
                data = row;
                examDetail = ExamDetail( self, data=data );
                examDetail.show();
        except Exception as e:
            logging.critical("Erro ao tentar abrir a janela de detalhes do exame: "+ str(e));
            raise e;


class AddUserWindow(QtWidgets.QMainWindow, Ui_addUser):
    ''' You can add new users to database of system '''
    def __init__(self, parent=None):
        super(AddUserWindow, self).__init__(parent);
        self.setupUi(self);
        try:
            self.db = DB();
        except Exception as e:
            logging.critical( "Houve um erro com a conexao de banco de dados: " + str(e) );
            raise e

    def register(self):
        name = self.entry_name.text();
        
        cpf = self.entry_cpf.text();
        if not self.__cpfCheck(cpf):
            QtWidgets.QMessageBox.warning(self, 'CPF Invalido', 'Insira um CPF Valido', QtWidgets.QMessageBox.Yes);
            logging.info("Usuario tentou inserir CPF invalido: " + cpf);
            return

        birthDay = self.date_birthDay.date().toPyDate();
        try:
            self.db.insertUser( name, 'Masculino', cpf, birthDay );
        except Exception as e:
            logging.critical( "Erro ao tentar inserir o usuario ao banco de dados: " + str(e) );
            QtWidgets.QMessageBox.information(self, 'Aviso', 'Erro ao inserir usuario ao banco.', QtWidgets.QMessageBox.Yes);
            return

        QtWidgets.QMessageBox.information(self, 'Novo usuário', 'Cadastrado com Sucesso!', QtWidgets.QMessageBox.Yes);
        self.destroy();
		
    #TODO: Do a better
    def __cpfCheck(self,cpf,d1=0,d2=0,i=0):
        if len(cpf) < 11:
            return False;
        while i<10:
            d1,d2,i=(d1+(int(cpf[i])*(11-i-1)))%11 if i<9 else d1,(d2+(int(cpf[i])*(11-i)))%11,i+1
        return (int(cpf[9])==(11-d1 if d1>1 else 0)) and (int(cpf[10])==(11-d2 if d2>1 else 0))

    def __clean(self):
        self.entry_name.setText('');
        self.entry_cpf.setText('');

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent);
        self.setupUi(self);

        self.btn_nuser.clicked.connect(self.on_btnNuser_clicked);
        self.btn_exam.clicked.connect(self.on_btnExam_clicked);
        self.btn_consult.clicked.connect(self.on_btnConsult_clicked);
		
        self.actionPorta_Serial.triggered.connect(self.on_actionSerialText_clicked);

    def on_btnNuser_clicked(self):
        try:
            dialogNUser = AddUserWindow(self);
            dialogNUser.show();
        except Exception as e:
            logging.critical("Erro ao tentar abrir janela de novo usuario: " + str(e));
            QtWidgets.QMessageBox.warning( self, "", "", QtWidgets.QMessageBox.Yes );

    def on_btnConsult_clicked( self ):
        try:
            dialogConsult = ConsultWindow( self );
            dialogConsult.show();
        except Exception as e:
            logging.critical("Erro ao tentar abrir a janela de consulta: "+ str(e));
		
    def on_btnExam_clicked(self):
        try:
            dialogExam = Exam( self );
            dialogExam.show();
        except Exception as e:
            logging.critical("Erro ao tentar a janela de exame: "+ str(e));
            QtWidgets.QMessageBox.warning(self, "Aviso", "Dispositivo Indisponivel", QtWidgets.QMessageBox.Yes);
            
    def on_actionSerialText_clicked(self):
        # How this window is created dinamicaly, it need join with mainWindow
        # TODO: Close connection when close window
        try:
            self.serialText = SerialDebug();
            self.serialText.show();
        except Exception as e:
            logging.critical("Erro ao tentar abrir o serial monitor: " + str(e));
            QtWidgets.QMessageBox.warning(self, "Aviso", "Dispositivo Indisponivel", QtWidgets.QMessageBox.Yes);
		
if __name__ == '__main__':
    import sys
    logger.setup();
    logging.info("\n");

    app = QtWidgets.QApplication(sys.argv);

    splash = QSplashScreen(QPixmap('assets/images/splash.jpg'));
    splash.show();

    main = MainWindow();

    splash.finish(main);
    main.show();

    sys.exit(app.exec_());
