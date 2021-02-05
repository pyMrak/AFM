# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 14:34:18 2017

@author: andmra2
"""

#import sys import argv, exit
from PyQt5.QtWidgets import QMainWindow, QWidget, QCheckBox, QAction, QFileDialog, QComboBox, QPushButton, QInputDialog, QMessageBox, QFormLayout, QLineEdit, QLabel, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
import getpass
import time

from libs import functional as start
from libs.logger import newLog
from libs.read_data import measurment_data as data
#from libs.read_data import readDefFolder
from libs.read_data import readSettings
#from libs.write_data import saveDefFolder
from libs.write_data import saveSettings
from libs import globalPaths
from libs import printProgram



class Main(QMainWindow):#QWidget):
    
    def __init__(self, version):

        super().__init__()
        #self.logger = newLog()
        self.setWindowIcon(QIcon('Graphic/Icons/windowIcon.ico'))
#        self.podatki=data(folder=readDefFolder())
        self.podatki=data(folder=readSettings(0), QCpath=readSettings(1))
        self.TC=False
        self.IG=False
        self.R=False
        self.QCs=self.podatki.qcs
        self.nastavitveA = Settings()   
        self.nastavitveG = Settings()
        self.nastavitveP = Settings()
        self.nastavitveT = Settings()
        self.pomoc = Help()
        self.ideje = Ideas()
        self.actions = Settings()
        self.version = version
        self.lastFiles = []
        if readSettings(3) == 'True':
            self.showTC = True
        else:
            self.showTC = False
        self.logger = newLog(self.version)
        self.initUI()
        
        



        
    def initUI(self):      
        #self.textEdit = QTextEdit()
        #self.setCentralWidget(self.textEdit)
        
        self.statusBar()
        
        selectFolder = QAction(QIcon('Graphic/Icons/pickFolder.png'), 'Izberi mapo z meritvami', self)
        selectFolder.setShortcut('Ctrl+F')
        selectFolder.triggered.connect(self.showDialog)
        
        AnalysisSettings = QAction(QIcon('Graphic/Icons/measSett.png'), 'Nastavi parametre analize', self)
        AnalysisSettings.setShortcut('Ctrl+S')
        AnalysisSettings.triggered.connect(self.nastavitve_analize)
        
        GraphSettings = QAction(QIcon('Graphic/Icons/graphSett.png'), 'Nastavi obliko grafov', self)
        GraphSettings.setShortcut('Ctrl+G')
        GraphSettings.triggered.connect(self.nastavitve_grafov)
        
        FunAnalysis = QAction(QIcon('Graphic/Icons/funAnalysis.png'), 'Analiziraj meritve', self)
        FunAnalysis.setShortcut('Ctrl+A')
        FunAnalysis.triggered.connect(self.startFuncAnalysis)
        
        
        TCreport = QAction(QIcon('Graphic/Icons/TCreport.png'), 'Izdelaj TC poročilo', self)
        TCreport.setShortcut('Ctrl+R')
        TCreport.triggered.connect(self.createTCreport)
        
        OpenReport = QAction(QIcon('Graphic/Icons/OpenReport.png'), 'Odpri zadnje/a poročilo/a', self)
        OpenReport.setShortcut('Ctrl+O')
        OpenReport.triggered.connect(self.openReport)
        
        OpenReport = QAction(QIcon('Graphic/Icons/Print.png'), 'Printaj dokumente', self)
        OpenReport.setShortcut('Ctrl+P')
        OpenReport.triggered.connect(self.printFiles)
        
        ProgSett = QAction(QIcon('Graphic/Icons/sett.png'), 'Nastavitve programa', self)
        ProgSett.setShortcut('Ctrl+E')
        ProgSett.triggered.connect(self.nastavitve_programa)
        
        Ideas = QAction(QIcon('Graphic/Icons/Idea.png'), 'Predlagaj izboljšavo', self)
        Ideas.setShortcut('Ctrl+I')
        Ideas.triggered.connect(self.Ideje)
        
        Help = QAction(QIcon('Graphic/Icons/Help.png'), 'Pomoč', self)
        Help.setShortcut('Ctrl+H')
        Help.triggered.connect(self.Pomoc)
        
        self.AnaSet = self.addToolBar('Analysis')
        self.AnaSet.addAction(selectFolder)
        self.AnaSet.addAction(AnalysisSettings)
        self.AnaSet.addAction(GraphSettings)
        #self.GraSet = self.addToolBar('Graphs')
        #self.GraSet.addAction(GraphSettings)
        
        
        self.Analysis = self.addToolBar('Run program')
        self.Analysis.addAction(FunAnalysis)
        if self.showTC:
            self.Analysis.addAction(TCreport) #za dodat termočleni
        self.Analysis.addAction(OpenReport)
        
        self.Program = self.addToolBar('Program')
        self.Program.addAction(ProgSett)
        self.Program.addAction(Ideas)
        self.Program.addAction(Help)
        #self.Analysis.addAction(TCreport)
        

        #openFile = QAction(QIcon('open.png'), 'Odpri mapo meritev', self)
        #openFile.setShortcut('Ctrl+O')
        #openFile.setStatusTip('Določi mapo meritev')
        #openFile.triggered.connect(self.showDialog)
        
        #settings = QAction(QIcon('settings.png'), 'Nastavitve analize', self)
        #settings.setShortcut('Ctrl+N')
        #settings.setStatusTip('Nastavi parametre analize')
        #settings.triggered.connect(self.nastavitve_analize)
        
        #graphSet = QAction(QIcon('settings.png'), 'Nastavitve grafov', self)
        #graphSet.setShortcut('Ctrl+G')
        #graphSet.setStatusTip('Nastavi obliko grafov')
        #graphSet.triggered.connect(self.nastavitve_grafov)

        #menubar = self.menuBar()
        ##fileMenu = menubar.addMenu('&Analiza')
        #fileMenu.addAction(openFile)
        #fileMenu.addAction(settings)
        
        #graphMenu = menubar.addMenu('&Grafi')
        #graphMenu.addAction(graphSet)
        
#        StartAnaBtn = QPushButton("Analiziraj meritve")
#        okButton = QPushButton("OK")
#        cancelButton = QPushButton("Cancel")
#        #Startbtn.move(220, 150)
#        
#        hbox = QHBoxLayout()
#        hbox.addStretch(1)
#        hbox.addWidget(okButton)
#        hbox.addWidget(cancelButton)
#
#        vbox = QVBoxLayout()
#        vbox.addStretch(1)
#        vbox.addLayout(hbox)
#        
#        self.setLayout(vbox) 
#        
#        self.setLayout(vbox) 
        
        #StartAnaBtn.clicked.connect(self.startMainProg)
        
        self.setGeometry(380, 50, 380, 50)
        self.setWindowTitle('Analiza fun. meritev Hidria AET d.o.o. ' + self.version.replace('_', '.'))
        self.show()
        try:
            messageFile = open(globalPaths.path.izmenjava + 'Andrej_Mrak/__Nove_Meritve/_Reports/Messages/' + self.version + '.txt', 'r')
            message = messageFile.read()
            buttonReply1 = QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
        except:
            pass
        
        
        
    def showDialog(self):

        folder = QFileDialog.getExistingDirectory(self, 'Izberi mapo z meritvami', self.nastavitveA.fname)
        if folder == "":
            self.nastavitveA.fname  = self.podatki.folder
        else:
            self.nastavitveA.fname = folder
        #saveDefFolder(self.nastavitveA.fname)
        saveSettings(0, self.nastavitveA.fname)

        #if self.nastavitveA.fname[0]:
            #print(self.nastavitveA.fname)
            
    def nastavitve_analize(self):
        self.nastavitveA.analize(self.nastavitveP.QCs)
        
        
        #self.QCs=self.podatki.qcs
        
    def nastavitve_grafov(self):
        self.nastavitveG.grafov()
        
    def nastavitve_programa(self):
        self.nastavitveP.programa()
        
    def Pomoc(self):
        self.pomoc.dialog()
        
    def Ideje(self):
        self.ideje.vnos()
        
        
    def startFuncAnalysis(self):
        #self.actions.analizaMeritev(self)
        self.logger.writeLocation('Functional analysis:', self.podatki.folder)
        try:
            self.lastFiles = start.Func_Analysis(self)
            if self.nastavitveP.openReport:
                self.openReport()
        except:
            buttonReply = QMessageBox.question(self, 'Napaka programa', "Ups.. prišlo je do napake.\nPošljem poročilo napake?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                if self.nastavitveP.QCpath == 'local':
                    IN = 1
                else:
                    IN = 0
                print(self.podatki.folder + "'"
                + "," + str(self.nastavitveA.maxlines)
                + "," + "'" + str(self.nastavitveA.QC) + "'"
                + "," + str(self.nastavitveA.R)
                + "," + str(self.nastavitveA.TC)
                + "," + str(self.nastavitveG.nG)
                + "," + str(self.nastavitveG.IG))
                system('python -c "from libs import Debug; Debug.Analysis('
                + "'" + self.podatki.folder + "'"
                + "," + str(self.nastavitveA.maxlines)
                + "," + "'" + str(self.nastavitveA.QC) + "'"
                + "," + str(self.nastavitveA.R)
                + "," + str(self.nastavitveA.TC)
                + "," + str(self.nastavitveG.nG)
                + "," + str(self.nastavitveG.IG)
                + ',' + str(IN) + ')" > '+globalPaths.path.izmenjava+'Andrej_Mrak/__Nove_Meritve/_Reports/debug_'  + getpass.getuser() + '_' + time.strftime("%d%m") + time.strftime("%y")[0:2] +time.strftime("%H%M%S") + '.log 2>&1')
                buttonReply = QMessageBox.question(self, 'Napaka poslana.', "Napaka je bila poslana\nin bo v najkrajšem možnem času odpravljena.\nHvala.", QMessageBox.Ok, QMessageBox.Ok)
        
    def createTCreport(self):
        self.logger.writeLocation('TC report:', self.podatki.folder)
        try:
            self.lastFiles = start.TC_report(self)
            if self.nastavitveP.openReport:
                self.openReport()
        except:
            buttonReply = QMessageBox.question(self, 'Napaka programa', "Ups.. prišlo je do napake.\nPošljem poročilo napake?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                if self.nastavitveP.QCpath == 'local':
                    IN = 1
                else:
                    IN = 0
                print(self.podatki.folder + "'"
                + "," + str(self.nastavitveA.maxlines)
                + "," + "'" + str(self.nastavitveA.QC) + "'"
                + "," + str(self.nastavitveA.R)
                + "," + str(self.nastavitveA.TC)
                + "," + str(self.nastavitveG.nG)
                + "," + str(self.nastavitveG.IG)
                + ',' + str(IN)
                + "," + "'" + self.nastavitveA.stNarocila + "'"
                + "," + "'" + self.nastavitveA.datumProizvodnje + "'"
                + "," + "'" + self.nastavitveA.nomV + "'"
                + "," + "'" + self.nastavitveA.kodaIzdelka + "'"
                + "," + "'" + self.nastavitveA.avtor + "'"
                + "," + str(self.nastavitveA.oznakaGP)+ ')"')
                system('python -c "from libs import Debug; Debug.TCreport('
                + "'" + self.podatki.folder + "'"
                + "," + str(self.nastavitveA.maxlines)
                + "," + "'" + str(self.nastavitveA.QC) + "'"
                + "," + str(self.nastavitveA.R)
                + "," + str(self.nastavitveA.TC)
                + "," + str(self.nastavitveG.nG)
                + "," + str(self.nastavitveG.IG)
                + ',' + str(IN)
                + "," + "'" + self.nastavitveA.stNarocila + "'"
                + "," + "'" + self.nastavitveA.datumProizvodnje + "'"
                + "," + "'" + self.nastavitveA.nomV + "'"
                + "," + "'" + self.nastavitveA.kodaIzdelka + "'"
                + "," + "'" + self.nastavitveA.avtor + "'"
                + "," + str(self.nastavitveA.oznakaGP)+ ')" > '+globalPaths.path.izmenjava+'Andrej_Mrak/__Nove_Meritve/_Reports/debug_'  + getpass.getuser() + '_' + time.strftime("%d%m") + time.strftime("%y")[0:2] +time.strftime("%H%M%S") + '.log 2>&1')
                buttonReply = QMessageBox.question(self, 'Napaka poslana.', "Napaka je bila poslana\nin bo v najkrajšem možnem času odpravljena.\nHvala.", QMessageBox.Ok, QMessageBox.Ok)
                  
    def openReport(self):
        if len(self.lastFiles) > 0:
            start.openFiles(self.lastFiles)
        else:
            message = 'V spominu ni nobene datoteke.'
            buttonReply1 = QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
        
    def printFiles(self):
        self.nastavitveT.printa(self.lastFiles, self.nastavitveA.fname)
        
    def update(self):
        self.podatki.get_QC()


class Communicate(QObject):
    
    closeApp = pyqtSignal()  
    
    
    
class Ideas(QWidget):
    def __init__(self):
        self.path = globalPaths.path.izmenjava+"Andrej_Mrak/__Nove_Meritve/_Reports/Ideas/"
        
        
    def vnos(self):
        super().__init__()
        self.setWindowIcon(QIcon('Graphic/Icons/Idea.png'))
        layout = QFormLayout()
        tab = QLabel()
        tab.setText('\t\t\t')
        napis = QLabel()
        napis.setText('Napiši kar misliš, da bi se dalo izboljšati, dopolniti:')
        self.ideja = QTextEdit('', self)
        OddajBtn = QPushButton("Oddaj", self)
        OddajBtn.clicked.connect(self.oddaj)
        layout.addRow(napis)
        layout.addRow(self.ideja)
        layout.addRow(tab, OddajBtn)
        self.setLayout(layout)
        self.setWindowTitle('Oddaj idejo.')
        
       
        
        self.show()
        
        
    def oddaj(self):
        file = open(self.path+getpass.getuser()+'_'+time.strftime("%d%m")+time.strftime("%y")[0:2]+time.strftime("%H%M%S")+'.txt', 'w')
        file.write(self.ideja.toPlainText())#str(self.ideja.text()))
        file.close()
        message = 'Hvala.\nVaša ideja je bila oddana.'
        buttonReply1 = QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
        self.close()
        
    


class Help(QWidget):  
    def __init__(self):
        
        self.path = globalPaths.path.izmenjava+"Andrej_Mrak/AFM/"
    
    def dialog(self):
        super().__init__()
        self.setWindowIcon(QIcon('Graphic/Icons/Help.png'))
        layout = QFormLayout()
        tab = QLabel()
        tab.setText('\t')
        #IGcb = QCheckBox('Prikaži tokove vseh svečk (samo pri grafih z večimi svečkami)', self)
        #IGcb.move(20, 60)
        #if self.IG:
         #   IGcb.toggle()
        #IGcb.stateChanged.connect(self.setIG)
        
        Tutorial = QPushButton("Hitri uvod", self)
        #Tutorial.move(40, 10)
        OKbtn = QPushButton("OK", self)
        #OKbtn.move(160, 40)
        layout.addRow(Tutorial, tab)
        layout.addRow(tab, OKbtn)
        
        
        #self.setGeometry(300, 300, 250, 70)
        self.setLayout(layout)
        self.setWindowTitle('Pomoč programa AFM')
        
        OKbtn.clicked.connect(self.close)
        Tutorial.clicked.connect(self.playUvod)
        
        self.show()
        
        #OKbtn.clicked.connect(self.close)
        
        
    def playUvod(self, file):
        file = 'HitriUvod.mp4'
        file = [self.path + file]
        start.openFiles(file)
        
            
class Settings(QWidget):#QWidget):
    
    def __init__(self):
        super().__init__()
        self.TC = False
        self.IG = False
        self.R = False
        self.maxlines = 6505
        self.QC = "414"
        self.fname = self.readFolder()
        self.nG = 1
        self.nomV = '5V'
        self.stNarocila = ''
        self.datumProizvodnje =  ''
        self.oznakaGP = 1
        self.kodaIzdelka =  ''
        self.avtor =  ''
        self.QCpath = readSettings(1)
        self.readQCs()
        if readSettings(2) == 'True':
            self.openReport = True
        else:
            self.openReport = False
        if readSettings(3) == 'True':
            self.showTC = True
        else:
            self.showTC = False
        
        
        #self.initUI(QCs)
        
    def printa(self, lastFiles, lastFolder):
        self.lastFiles = lastFiles
        self.lastFolder = lastFolder
        super().__init__()
        self.setWindowIcon(QIcon('Graphic/Icons/Print.png'))
        layout = QFormLayout()
        
        tab = QLabel()
        tab.setText('\t')
        
        napis = QLabel()
        napis.setText('Izberite možnost printanja.')
        
        zadnjiPrintBtn = QPushButton("\tPrintaj zadnje datoteke\t", self)
        izberiPrintBtn= QPushButton("\tIzberi datoteke za print\t", self)
        zadnjiPrintBtn.clicked.connect(self.printLastFiles)
        izberiPrintBtn.clicked.connect(self.printFiles)
        
        

        
        layout.addRow(napis)
        layout.addRow(zadnjiPrintBtn,izberiPrintBtn)
        self.setLayout(layout)
        self.setWindowTitle('Printanje dokumentov.')
        self.show()
        
        
    def analize(self, QCs):    
        #podatki.get_QC()
        super().__init__()
        self.setWindowIcon(QIcon('Graphic/Icons/measSett.png'))
        layout = QFormLayout()
        
        tab = QLabel()
        tab.setText('\t')
        
        nastFun = QLabel()
        nastFun.setText('Nastavitve za funkcionalno analizo')
        
        QCset = QComboBox(self)
        for qc in QCs:
            if qc == "":
                if self.QC == "414":
                    QCset.addItem("Nastavi QC           ")
                else:
                    QCset.addItem(self.QC) 
            else:
                QCset.addItem(qc)


#        QCset.move(20, 15)
        QCset.activated[str].connect(self.QCpick)
            
        TCcb = QCheckBox('Termočlen analiza', self)
#        TCcb.move(20, 40)
        if self.TC:
            TCcb.toggle()
        TCcb.stateChanged.connect(self.setTC)
#        
#        
#        
        VWcb = QCheckBox('VW predshranjevanje (5s)', self)
#        VWcb.move(20, 60)
        if self.maxlines > 6500:
            VWcb.toggle()
        VWcb.stateChanged.connect(self.setVW)
#        
        Rcb = QCheckBox('Dodaj stolpec za upornost', self)
#        Rcb.move(20, 80)
        if self.R:
            Rcb.toggle()
        Rcb.stateChanged.connect(self.setR)
        
        if self.showTC:
            nastTer = QLabel()
            nastTer.setText('\n\nNastavitve za termočlen poročila')
            
            naro = QLabel()
            naro.setText('Št. naročila: ')
            self.narocilo = QLineEdit('', self)
            self.narocilo.setText(self.stNarocila)
            
            proi = QLabel()
            proi.setText('Datum proizvodnje: ')
            self.proizvodnja = QLineEdit('', self)
            self.proizvodnja.setText(self.datumProizvodnje)
            
            nomv = QLabel()
            nomv.setText('Nominalna napetost: ')
            #self.GPnumber = QLineEdit('', self)
            
            gpcode = QLabel()
            gpcode .setText('Koda izdelka: ')
            self.GPcode  = QLineEdit('', self)
            self.GPcode.setText(self.kodaIzdelka)
            
            gpnr = QLabel()
            gpnr.setText('Oznaka 1. vzorca: ')
            self.GPnumber = QLineEdit('', self)
            self.GPnumber.setText(str(self.oznakaGP))
            
            auth = QLabel()
            auth.setText('Avtor: ')
            self.author = QLineEdit('', self)
            self.author.setText(self.avtor)
            
            VoltagePick = QComboBox(self)
            vol = [self.nomV] + ['4,4V', '5V', '11V', '13,5V', '23V']
            for V in vol:
                VoltagePick.addItem(V)
            VoltagePick.activated[str].connect(self.Vpick)
        
        OKbtn = QPushButton("OK", self)
        if self.showTC:
            OKbtn.clicked.connect(self.closeBoxA)
        else:
            OKbtn.clicked.connect(self.close)
        
        
        
        layout.addRow(nastFun)
        layout.addRow(QCset)
        layout.addRow(TCcb)
        layout.addRow(VWcb)
        layout.addRow(Rcb)
        if self.showTC:
            layout.addRow(nastTer)
            layout.addRow(nomv, VoltagePick)
            layout.addRow(gpcode, self.GPcode)
            layout.addRow(proi, self.proizvodnja)
            layout.addRow(gpnr, self.GPnumber)
            layout.addRow(naro, self.narocilo)
            layout.addRow(auth, self.author)
        layout.addRow(tab, OKbtn)
        
        
        
        
        #self.setGeometry(300, 300, 250, 150)
        self.setLayout(layout)
        #self.setLayout(layout)
        self.setWindowTitle('Nastavitve analize')
        self.show()
        
        

            
    def closeBoxA(self):
       if not self.GPnumber.text() == '':
           try:
               self.oznakaGP = int(self.GPnumber.text())
               intOK = True
           except:
               #print('Gpnr: ',self.GPnumber.text())
               message = 'Oznaka 1. vzorca je lahko le celo število.'
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)
           if intOK:
               self.stNarocila =  str(self.narocilo.text())
               self.datumProizvodnje =  str(self.proizvodnja.text())
               self.kodaIzdelka =  str(self.GPcode.text())
               if not self.kodaIzdelka == '' and not self.kodaIzdelka[-3:] == '200':
                   self.kodaIzdelka += '-200'
               self.avtor =  str(self.author.text())
               print('št. naročila: ', self.stNarocila)
               print('Datum proizvodnje: ', self.datumProizvodnje)
               print('Koda izdelka: ', self.kodaIzdelka)
               print('Oznaka 1. vzorca: ', self.oznakaGP)
               print('Avtor: ', self.avtor)
               self.close()
       else:
            print('Gpnr: _',self.GPnumber.text())
            self.close()

       
    
            
    def grafov(self):
        super().__init__()
        self.setWindowIcon(QIcon('Graphic/Icons/graphSett.png'))
        layout = QFormLayout()
        
        IGcb = QCheckBox('Prikaži tokove vseh svečk\n(samo pri grafih z večimi svečkami)', self)
        #IGcb.move(20, 60)
        if self.IG:
            IGcb.toggle()
        IGcb.stateChanged.connect(self.setIG)
        
        graph = QLabel()
        graph .setText('Št. meritev na graf: ')
        self.GraphNr = QLineEdit('', self)
        self.GraphNr.setText(str(self.nG))
        tab = QLabel()
        tab.setText('\t')
        
        OKbtn = QPushButton("OK", self)
        #OKbtn.move(250, 120)
        #GraphBtn = QPushButton(str(self.nG) + " meritve/ev na 1 graf", self)
        #GraphBtn.move(20, 30)
        layout.addRow(graph, self.GraphNr)
        layout.addRow(IGcb)
        layout.addRow(tab, OKbtn)
        
        
        
        #self.setGeometry(300, 300, 350, 150)
        self.setLayout(layout)
        self.setWindowTitle('Nastavitve grafov')
        
        OKbtn.clicked.connect(self.closeBoxG)
        #GraphBtn.clicked.connect(self.GraphDialog)
        
        self.show()
        
    def closeBoxG(self):
       if not self.GraphNr.text() == '':
           try:
               nG = int(self.GraphNr.text())
               if nG > 0:
                   self.nG = nG
                   intOK = True
               else:
                   #print('Gpnr: ',self.GraphNr.text())
                   message = 'Število meritev na graf je lahko le naravno število.'
                   intOK = False
                   QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)
           except:
               #print('Gpnr: ',self.GraphNr.text())
               message = 'Število meritev na graf je lahko le naravno število.'
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)
           if intOK:
               print('GraphNr: ',self.GraphNr.text())
               self.close()
       else:
            print('GraphNr: _',self.GraphNr.text())
            self.close()
        
        
    def programa(self):
        
        super().__init__()
        self.setWindowIcon(QIcon('Graphic/Icons/sett.png'))
        layout = QFormLayout()
        
        QCpath = QCheckBox('Beri lokalni QC', self)
        #QCpath.move(20, 15)
        if self.QCpath == 'local':
           QCpath.toggle()
           
        openReport = QCheckBox('Po shranjevanju avtomatsko odpri poročilo', self)
        #openReport.move(20, 30)
        if self.openReport:
           openReport.toggle()
           
        TCshow = QCheckBox('Prikaži možnost termočlenov\n(potreben ponoven zagon programa)', self)
        #openReport.move(20, 30)
        if self.showTC:
           TCshow.toggle()  
           
        QCpath.stateChanged.connect(self.setQCpath)
        openReport.stateChanged.connect(self.setOpenReport)
        TCshow.stateChanged.connect(self.setTCshow)
        
        tab = QLabel()
        tab.setText('\t\t\t')
        OKbtn = QPushButton("OK", self)
        #OKbtn.move(150, 50)
        
        layout.addRow(QCpath)
        layout.addRow(openReport)
        layout.addRow(TCshow)
        layout.addRow(tab, OKbtn)
        
        
        #self.setGeometry(300, 300, 250, 80)
        self.setLayout(layout)
        self.setWindowTitle('Nastavitve programa')
        
        OKbtn.clicked.connect(self.close)
        self.show()
        
        
    def analizaMeritev(self, main):

        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('Izdelava analize meritev')
        self.show()
        
        quit()
        
        
    def izdelavaTcPoročila(self, main):

        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('Izdelava TC poročila')
        self.show()
        self.lastFiles = start.TC_report(main)
        quit()
        

        
        
            
    def setTC(self, state):
        if state == Qt.Checked:
            self.TC = True
        else:
            self.TC = False
        print('TC:',self.TC)
        
    def setR(self, state):
        if state == Qt.Checked:
            self.R = True
        else:
            self.R = False
        print('R:',self.R)
        
        
    def GraphDialog(self):
        text, ok = QInputDialog.getText(self, 'Nastavitev grafov', 'Nastavi število meritev prikazanih na 1 graf:')
        if ok:
            try:
                Input = int(text)
                if Input > 0:
                    self.nG = Input
                else:
                    pass
            except:
                pass
            self.close()
            self.grafov()
            print('nG:', self.nG)
        

        
    def setIG(self, state):
        if state == Qt.Checked:
            self.IG = True
        else:
            self.IG = False
        print('IG:',self.IG)
        
        
    def setQCpath(self, state):
        if state == Qt.Checked:
            self.QCpath = 'local'
        else:
            self.QCpath = 'global'
        saveSettings(1, self.QCpath)
        self.readQCs()
        
        print('QCpath:', self.QCpath)
        
        
    def readQCs(self):
        if self.QCpath == 'local':
            fileName = 'QC/QC.txt'
        else:
            fileName = globalPaths.path.QC
        file=open(fileName, 'r').read()   
        self.QCs=[]
        for qc in file.split('QC'):
            self.QCs.append(qc.split('>')[0].split('<')[-1])
        
        
    def setOpenReport(self, state):
        if state == Qt.Checked:
            self.openReport = True
        else:
            self.openReport = False
        saveSettings(2, str(self.openReport))
        
        print('openReport:', self.openReport)
        
        
        
    def setTCshow(self, state):
        if state == Qt.Checked:
            self.showTC = True
        else:
            self.showTC = False
        saveSettings(3, str(self.showTC))
        print('show TC:', self.showTC)
        
    def setVW(self, state):
        if state == Qt.Checked:
            self.maxlines = 6505
        else:
            self.maxlines = 6005
        print('maxlines:',self.maxlines)
        
    def QCpick(self, text):
        
        if text == "Nastavi QC":
            self.QC = "414"
        else:
            self.QC = text
        print(self.QC)
        
    def Vpick(self, text):
        self.nomV = text
        print(self.nomV)
        
    def readFolder(self):
        return readSettings(0)
    
    def printLastFiles(self):
        if len(self.lastFiles) > 0:
            self.printDialog(self.lastFiles)
        else:
            message = 'V spominu ni nobene datoteke.'
            buttonReply1 = QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
    
    def printFiles(self):
        filters = "XLSX (*.xlsx);;XLSM (*.xlsm);;TXT (*.txt);;PDF (*.pdf);;DOCX (*.docx);;DOC (*.doc)"
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        files = file_name.getOpenFileNames(self, caption="Izberi dokumente", directory=self.lastFolder, filter=filters)
        if len(files[0]) > 0:
           self.printDialog(files[0])
    
    def printDialog(self, files):
        documentString = ''
        for f in files:
            documentString += f+'\n'
        if len(files) > 4:
            doc = ' dokumentov'
        elif len(files) > 2:
            doc = ' dokumente'
        elif len(files) > 1:
            doc = ' dokumenta'
        else:
            doc = ' dokument'
        buttonReply = QMessageBox.warning(self, 'Opozorilo pred printanjem', "Pozor! Naprintali boste "+str(len(files))+doc+':\n'+
                                           documentString+'\nŠe enkrat premislite - okolje vam bo hvaležno :)', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            printProgram.printFiles(files)
        
        
#if __name__ == '__main__':
#    
#    app = QApplication(argv)
#    ex = Main(["","Ubuntuehrejhtjtejee", "Mandriva", "Fedora", "Arch", "Gentoo"])
#    exit(app.exec_())

    