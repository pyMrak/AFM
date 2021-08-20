# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 14:34:18 2017

@author: andmra2
"""

#import sys import argv, exit
from PyQt5.QtWidgets import QMainWindow, QWidget, QCheckBox, QAction, QFileDialog, QComboBox, QPushButton, QInputDialog, QMessageBox, QFormLayout, QLineEdit, QLabel, QTextEdit, QRadioButton
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from getpass import getuser
from time import strftime
from sys import  exc_info
from traceback import print_exception
from os import listdir

#from os import system

from libs import functional as start
from libs.logger import newLog, messageLogger
from libs.read_data import measurment_data as data
#from libs.read_data import readDefFolder
from libs.read_data import readSettings
#from libs.write_data import saveDefFolder
from libs.write_data import saveSettings
from libs import globalPaths
from libs import printProgram
from libs.TTreport import TTreport as TT
from libs import transformMeas
from libs.initialChecker import checkSettings







class permissionError():

    def __init__(self, app,  message):
        # The QWidget widget is the base class of all user interface objects in PyQt4.
        w = QWidget()
        # Show a message box
        buttonReply = QMessageBox.critical(w, 'Napaka.', message, QMessageBox.Ok, QMessageBox.Ok)
        if buttonReply == QMessageBox.Ok:
            app.exec_()
        # Show window
        w.show()
    def closeEvent(self, event):
        event.accept()



class Main(QMainWindow):#QWidget):
    
    def __init__(self, version, online=True, login=False):
        
        super().__init__()
        #self.logger = newLog()
        self.online = online
        self.login = login
        if login:
            checkSettings(login.username)
            self.username = login.username
            if self.login.userType == 'admin':
                self.checkForRequests()
                self.checkForReports()
                self.checkForIdeas()
        else:
            checkSettings('Debug')
            self.username = 'Debug'
            self.checkForRequests()
            self.checkForReports()
            self.checkForIdeas()
        self.setWindowIcon(QIcon('Graphic/Icons/windowIcon.ico'))
#        self.podatki=data(folder=readDefFolder())
        if self.online:
            QCp = readSettings(1, self.username)
        else:
            QCp = 'local'
        self.podatki=data(self, folder=readSettings(0, self.username), QCpath=QCp)
        self.TC=False
        self.IG=False
        self.R=False
        self.QCs=self.podatki.qcs
        self.nastavitveA = Settings(self.username, self.online)   
        self.nastavitveG = Settings(self.username, self.online)
        self.nastavitveP = Settings(self.username, self.online)
        self.nastavitveT = Settings(self.username, self.online)
        self.podatki.setGraphSett(self.nastavitveG)
        self.pomoc = Help()
        self.ideje = Ideas()
        self.actions = Settings(self.username, self.online)
        self.version = version
        self.lastFiles = []
        if readSettings(3, self.username) == 'True':
            self.showTC = True
        else:
            self.showTC = False
        self.logger = newLog(self.version, self.login)
        self.TTreportModule = TT(self, login)
        self.TTreportModule.setFolder(readSettings(0, self.username))
        self.TTreportW = TTreportWindow(self.TTreportModule, self.username)
        self.initUI()
        self.statusBar().showMessage('')
        self.messageLogger = messageLogger()
        self.fileChanger = transformMeas.transformMedoMeas()
        self.changeFileW = changeFileWindow()
        #print('username:', self.username)
        
    def checkForRequests(self):
        if len(listdir(globalPaths.path.newUserRequests)) > 0:
            message = 'Imate nove zahteve uporabnikov.'
            QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
        
    def checkForReports(self):
        if len(listdir(globalPaths.path.reports)) > 0:
            message = 'Imate nova poročila o napakah.'
            QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
            
    def checkForIdeas(self):
        if len(listdir(globalPaths.path.ideas)) > 0:
            message = 'Imate nove ideje uporabnikov.'
            QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
        

    def closeEvent(self, event):
        event.accept()

        
    def initUI(self):      
        #self.textEdit = QTextEdit()
        #self.setCentralWidget(self.textEdit)
        
        #self.statusBar()
        
        selectFolder = QAction(QIcon('Graphic/Icons/pickFolder.png'), 'Izberi mapo z meritvami', self)
        selectFolder.setShortcut('Ctrl+F')
        selectFolder.triggered.connect(self.showDialog)
        
        changeFiles = QAction(QIcon('Graphic/Icons/transformFiles.png'), 'Pretvori meritve iz proizvodnje', self)
        changeFiles.setShortcut('Ctrl+C')
        changeFiles.triggered.connect(self.changeFiles)
        
        AnalysisSettings = QAction(QIcon('Graphic/Icons/measSett.png'), 'Nastavi parametre analize', self)
        AnalysisSettings.setShortcut('Ctrl+S')
        AnalysisSettings.triggered.connect(self.nastavitve_analize)
        
        GraphSettings = QAction(QIcon('Graphic/Icons/graphSett.png'), 'Nastavi obliko grafov', self)
        GraphSettings.setShortcut('Ctrl+G')
        GraphSettings.triggered.connect(self.nastavitve_grafov)
        
        FunAnalysis = QAction(QIcon('Graphic/Icons/funAnalysis.png'), 'Analiziraj meritve', self)
        FunAnalysis.setShortcut('Ctrl+A')
        FunAnalysis.triggered.connect(self.startFuncAnalysis)
        
        TTreport = QAction(QIcon('Graphic/Icons/TTreport.png'), 'Izdelaj TT poročilo', self)
        TTreport.setShortcut('Ctrl+T')
        TTreport.triggered.connect(self.createTTreport)
        
        
        TCreport = QAction(QIcon('Graphic/Icons/TCreport.png'), 'Izdelaj TC poročilo', self)
        TCreport.setShortcut('Ctrl+R')
        TCreport.triggered.connect(self.createTCreport)
        
        OpenReport = QAction(QIcon('Graphic/Icons/OpenReport.png'), 'Odpri zadnje/a poročilo/a', self)
        OpenReport.setShortcut('Ctrl+O')
        OpenReport.triggered.connect(self.openReport)
        
        PrintDocuments = QAction(QIcon('Graphic/Icons/Print.png'), 'Printaj dokumente', self)
        PrintDocuments.setShortcut('Ctrl+P')
        PrintDocuments.triggered.connect(self.printFiles)
        
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
        self.AnaSet.addAction(changeFiles)
        self.AnaSet.addAction(AnalysisSettings)
        self.AnaSet.addAction(GraphSettings)
        #self.GraSet = self.addToolBar('Graphs')
        #self.GraSet.addAction(GraphSettings)
        
        
        self.Analysis = self.addToolBar('Run program')
        self.Analysis.addAction(FunAnalysis)
        self.Analysis.addAction(TTreport)
        if self.showTC:
            self.Analysis.addAction(TCreport) #za dodat termočleni
        self.Analysis.addAction(OpenReport)
        self.Analysis.addAction(PrintDocuments)
        
        self.Program = self.addToolBar('Program')
        self.Program.addAction(ProgSett)
        self.Program.addAction(Ideas)
        self.Program.addAction(Help)
        #self.Analysis.addAction(TCreport)
        

        
        self.setGeometry(450, 50, 450, 50)
        self.setWindowTitle('Analiza Fun. Meritev Hidria d.o.o. ' + self.version.replace('_', '.')+ ' - '+self.username)
        self.show()
        try:
            messageFile = open(globalPaths.path.messages + self.version + '.txt', 'r', encoding="utf-8")
            message = messageFile.read()
            QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
        except:
            pass
        
        
        
    def showDialog(self):

        folder = QFileDialog.getExistingDirectory(self, 'Izberi mapo z meritvami', self.nastavitveA.fname)
        if folder == "":
            self.nastavitveA.fname  = self.podatki.folder
            try:
                self.TTreportModule.setFolder(self.podatki.folder)
            except:
                self.TTreportModule.setFolder('measurements')
        else:
            self.nastavitveA.fname = folder
            try:
                self.TTreportModule.setFolder(folder)
            except:
                self.TTreportModule.setFolder('measurements')
        #saveDefFolder(self.nastavitveA.fname)
        saveSettings(0, self.nastavitveA.fname, self.username)

    def changeFiles(self):
        self.changeFileW.setup(self.fileChanger, self.nastavitveA.fname)

        
            
    def nastavitve_analize(self):
        #print(self.nastavitveP.QCs)
        try:
            self.nastavitveA.analize(self.nastavitveP.QCs, self.TTreportModule)
        except Exception as e:
            pass
            #print(e)
        
        
        #self.QCs=self.podatki.qcs
        
    def nastavitve_grafov(self):
        self.nastavitveG.grafov()
        
    def nastavitve_programa(self):
        self.nastavitveP.programa(self.login)
        
    def Pomoc(self):
        self.pomoc.dialog()
        
    def Ideje(self):
        self.ideje.vnos()
        
        
    def startFuncAnalysis(self):
        #self.actions.analizaMeritev(self)
        self.messageLogger.reset()
        self.logger.writeLocation('Functional analysis:', self.podatki.folder)
        try:
            self.lastFiles = start.Func_Analysis(self)
            if self.nastavitveP.openReport:
                self.openReport()
            msg, w, e = self.messageLogger.check()
            if w+e > 0:
                message = 'Med analizo smo zaznali '+str(w)+' opozoril in '+str(e)+' napak:\n'
                message += msg
                message += '\n\nSkrbno preverite če opozorila vplivajo na rezultate.'
                QMessageBox.warning(self, 'Pozor!', message, QMessageBox.Ok, QMessageBox.Ok)
#        except UnboundLocalError:
#            exc_type, exc_value, exc_traceback = exc_info()
#            message = 'Neznana glava dokumenta. Preverite glavo datoteke meritev, če se sklada z nastavitvami v Settings/headers.txt'
#            self.messageLogger.writeError(message, self, isMD=False)
#            QMessageBox.warning(self, 'Napaka!', message[:58]+'\n'+message[59:], QMessageBox.Ok, QMessageBox.Ok)
#            logFile = open(globalPaths.path.izmenjava+'Andrej_Mrak/__Nove_Meritve/_Reports/debug_'  + getuser() + '_' + strftime("%d%m") + strftime("%y")[0:2] +strftime("%H%M%S") + '.log','w')
#            print_exception(exc_type, exc_value, exc_traceback, file=logFile)
#            logFile.close()
        except ValueError:
            message = 'V izbrani mapi nismo našli meritev.'
            QMessageBox.warning(self, 'Pozor!', message, QMessageBox.Ok, QMessageBox.Ok)
            exc_type, exc_value, exc_traceback = exc_info()
            logFile = open(globalPaths.path.reports+'debug_'  + self.username + '_' + strftime("%d%m") + strftime("%y")[0:2] +strftime("%H%M%S") + '.log','w', encoding="utf-8")
            #logFile.write(str(error)+'\n'+str(exc_type)+'\n'+str(exc_value)+'\n'+str(exc_traceback))
            print_exception(exc_type, exc_value, exc_traceback, file=logFile)
            logFile.close()
        except UnboundLocalError:
            message = 'Neznana glava meritve. Preverite nastavitve glave v\nAFM/Settings/headers.txt'
            QMessageBox.warning(self, 'Pozor!', message, QMessageBox.Ok, QMessageBox.Ok)
            exc_type, exc_value, exc_traceback = exc_info()
            logFile = open(globalPaths.path.reports+'debug_'  + self.username + '_' + strftime("%d%m") + strftime("%y")[0:2] +strftime("%H%M%S") + '.log','w', encoding="utf-8")
            #logFile.write(str(error)+'\n'+str(exc_type)+'\n'+str(exc_value)+'\n'+str(exc_traceback))
            print_exception(exc_type, exc_value, exc_traceback, file=logFile)
            logFile.close()
        except Exception:
            exc_type, exc_value, exc_traceback = exc_info()
            message = 'Prišlo je do napake. Napaka bo v najkrajšem\n možnem času odpravljena. Opravičujemo se za nevšečnost.'
            QMessageBox.error(self, 'Napaka!', message, QMessageBox.Ok, QMessageBox.Ok)
            

            logFile = open(globalPaths.path.reports+'debug_'  + self.username + '_' + strftime("%d%m") + strftime("%y")[0:2] +strftime("%H%M%S") + '.log','w', encoding="utf-8")
            #logFile.write(str(error)+'\n'+str(exc_type)+'\n'+str(exc_value)+'\n'+str(exc_traceback))
            print_exception(exc_type, exc_value, exc_traceback, file=logFile)
            logFile.close()
        self.podatki.reset()
                
    def createTCreport(self):
        self.messageLogger.reset()
        self.logger.writeLocation('TC report:', self.podatki.folder)
        try:
            self.lastFiles = start.TC_report(self)
            if self.nastavitveP.openReport:
                self.openReport()
            msg, w, e = self.messageLogger.check()
            if w+e > 0:
                message = 'Med analizo smo zaznali '+str(w)+' opozoril in '+str(e)+' napak:\n'
                message += msg
                message += '\n\nSkrbno preverite če opozorila vplivajo na rezultate.'
                QMessageBox.warning(self, 'Pozor!', message, QMessageBox.Ok, QMessageBox.Ok)
        except UnboundLocalError:
            exc_type, exc_value, exc_traceback = exc_info()
            message = 'Neznana glava dokumenta. Preverite glavo datoteke meritev, če se sklada z nastavitvami v Settings/headers.txt'
            self.messageLogger.writeError(message, self, isMD=False)
            QMessageBox.warning(self, 'Napaka!', message[:58]+'\n'+message[59:], QMessageBox.Ok, QMessageBox.Ok)
            logFile = open(globalPaths.path.reports+'debug_'  + self.username + '_' + strftime("%d%m") + strftime("%y")[0:2] +strftime("%H%M%S") + '.log','w', encoding="utf-8")
            print_exception(exc_type, exc_value, exc_traceback, file=logFile)
            logFile.close()
        except Exception:
            exc_type, exc_value, exc_traceback = exc_info()
            message = 'Prišlo je do napake. Napaka bo v najkrajšem\n možnem času odpravljena. Opravičujemo se za nevšečnost.'
            QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
            

            logFile = open(globalPaths.path.reports+'debug_'  + self.username + '_' + strftime("%d%m") + strftime("%y")[0:2] +strftime("%H%M%S") + '.log','w', encoding="utf-8")
            #logFile.write(str(error)+'\n'+str(exc_type)+'\n'+str(exc_value)+'\n'+str(exc_traceback))
            print_exception(exc_type, exc_value, exc_traceback, file=logFile)
            logFile.close()
        self.podatki.reset()
        
    def createTTreport(self):
        self.messageLogger.reset()
        self.logger.writeLocation('TT report:', self.podatki.folder)
        
        #self.TTreportModule.setFolder(self.podatki.folder)
        try:
            #TTR.setCikli('Do odpovedi.')
            #TTR.setAuthor('Andrej Mrak')
            #TTR.setNamenTesta('Validacija upora.')
            #TTR.setKodaSvecke('5011-721-968')
            #self.TTreportW.initialSettings()
            #self.TTreportModule.setFolder(self.nastavitveA.fname)
            self.lastFiles = self.TTreportModule.createReport()
            if len(self.lastFiles) > 0:
                #self.lastFiles = self.TTreportModule.getLastFile()
                if self.nastavitveP.openReport:
                    self.openReport()
                message = 'TT poročilo ustvarjeno.\nNe pozabi na komentarje :)'
                QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
                msg, w, e = self.messageLogger.check()
                if w+e > 0:
                    message = 'Med ustvarjanjem poročila smo zaznali '+str(w)+' opozoril in '+str(e)+' napak:\n'
                    message += msg
                    message += '\n\nSkrbno preverite če opozorila vplivajo na poročilo.'
                    QMessageBox.warning(self, 'Pozor!', message, QMessageBox.Ok, QMessageBox.Ok)
            else:
                message = 'V izbrani mapi ni dokumenta formata ...AFM.xlsx'
                QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
#        except UnboundLocalError:
#            exc_type, exc_value, exc_traceback = exc_info()
#            message = 'Neznana glava dokumenta. Preverite glavo datoteke meritev, če se sklada z nastavitvami v Settings/headers.txt'
#            self.messageLogger.writeError(message, self, isMD=False)
#            QMessageBox.warning(self, 'Napaka!', message[:58]+'\n'+message[59:], QMessageBox.Ok, QMessageBox.Ok)
#            logFile = open(globalPaths.path.izmenjava+'Andrej_Mrak/__Nove_Meritve/_Reports/debug_'  + getuser() + '_' + strftime("%d%m") + strftime("%y")[0:2] +strftime("%H%M%S") + '.log','w')
#            print_exception(exc_type, exc_value, exc_traceback, file=logFile)
#            logFile.close()
        except Exception:
            exc_type, exc_value, exc_traceback = exc_info()
            message = 'Prišlo je do napake. Napaka bo v najkrajšem\n možnem času odpravljena. Opravičujemo se za nevšečnost.'
            QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
            

            logFile = open(globalPaths.path.reports+'debug_'  + self.username + '_' + strftime("%d%m") + strftime("%y")[0:2] +strftime("%H%M%S") + '.log','w', encoding="utf-8")
            #logFile.write(str(error)+'\n'+str(exc_type)+'\n'+str(exc_value)+'\n'+str(exc_traceback))
            print_exception(exc_type, exc_value, exc_traceback, file=logFile)
            logFile.close()
        self.podatki.reset()
            
    def openReport(self):
        if len(self.lastFiles) > 0:
            start.openFiles(self.lastFiles)
        else:
            message = 'V spominu ni nobene datoteke.'
            QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
        
    def printFiles(self):
        self.nastavitveT.printa(self.lastFiles, self.nastavitveA.fname)
        
    def update(self):
        self.podatki.get_QC()
                      
        
        


class Communicate(QObject):
    
    closeApp = pyqtSignal()  
    
    
    
class Ideas(QWidget):
    def __init__(self):
        self.path = globalPaths.path.ideas#izmenjava+"Andrej_Mrak/__Nove_Meritve/_Reports/Ideas/"
        
        
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
        file = open(self.path+getuser()+'_'+strftime("%d%m")+strftime("%y")[0:2]+strftime("%H%M%S")+'.txt', 'w', encoding="utf-8")
        file.write(self.ideja.toPlainText())#str(self.ideja.text()))
        file.close()
        message = 'Hvala.\nVaša ideja je bila oddana.'
        QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
        self.close()
        
    


class Help(QWidget):  
    def __init__(self):
        
        self.path = globalPaths.path.download
    
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
        Readme = QPushButton("Navodila", self)
        #Tutorial.move(40, 10)
        OKbtn = QPushButton("OK", self)
        #OKbtn.move(160, 40)
        layout.addRow(Tutorial, tab)
        layout.addRow(Readme, tab)
        layout.addRow(tab, OKbtn)
        
        
        #self.setGeometry(300, 300, 250, 70)
        self.setLayout(layout)
        self.setWindowTitle('Pomoč programa AFM')
        
        OKbtn.clicked.connect(self.close)
        Tutorial.clicked.connect(self.playUvod)
        Readme.clicked.connect(self.openReadme)
        
        self.show()
        
        #OKbtn.clicked.connect(self.close)
        
        
    def playUvod(self, file):
        file = 'HitriUvod.mp4'
        file = [self.path + file]
        start.openFiles(file)
        
    def openReadme(self):
        file = [self.path + 'Navodila.pdf']
        start.openFiles(file)
        
        
class TTreportWindow(QWidget):
    
    def __init__(self, TTreportModule, username):
        super().__init__()
        self.username = username
        self.TTreportModule = TTreportModule
        self.nrPerRow = ['1', '2', '3', '4']
        self.TTreportModule.setRTGperRow(int(readSettings(27, self.username)))
        self.iGroup = 0
        
    def initialSettings(self):
        super().__init__()
        self.iGroup = 0
        self.setWindowIcon(QIcon('Graphic/Icons/TTreport.png'))
        layout = QFormLayout()
        
        tab = QLabel()
        tab.setText('\t')
        
        nastTT = QLabel()
        nastTT.setText('Splošne nastavitve TT poročila.')
        
        #TTR.setKodaSvecke('5011-721-968')
        kodaL = QLabel()
        kodaL.setText('Koda svečke: ')
        self.koda = QLineEdit('', self)
        self.koda.setText(str(self.TTreportModule.getKodaSvecke()))
        
        
        #TTR.setNamenTesta('Validacija upora.')
        namenL = QLabel()
        namenL.setText('Namen testa: ')
        self.namen = QLineEdit('', self)
        self.namen.setText(str(self.TTreportModule.getNamenTesta()))
        
        #TTR.setAuthor('Andrej Mrak')
        sIzvedbaL = QLabel()
        sIzvedbaL.setText('Skupna izvedba: ')
        self.sIzvedba = QLineEdit('', self)
        self.sIzvedba.setText(str(self.TTreportModule.getIzvedbaSkupno()))
        
        
        #TTR.setCikli('Do odpovedi.')
        cikliL = QLabel()
        cikliL.setText('Št. ciklov TT: ')
        self.cikli = QLineEdit('', self)
        self.cikli.setText(str(self.TTreportModule.getCikli()))
        
        
        #TTR.setAuthor('Andrej Mrak')
        avtorL = QLabel()
        avtorL.setText('Avtor: ')
        self.avtor = QLineEdit('', self)
        self.avtor.setText(str(self.TTreportModule.getAuthor()))
        
        
        IZcb = QCheckBox('Enake izvedbe vzorcev', self)
#        TCcb.move(20, 40)
        if self.TTreportModule.getEnakaIzvedba():
            IZcb.toggle()
        IZcb.stateChanged.connect(self.setIZ)
        
        
        PRcb = QCheckBox('Enak profil TT', self)
#        TCcb.move(20, 40)
        if self.TTreportModule.getEnakaProcedura():
            PRcb.toggle()
        PRcb.stateChanged.connect(self.setPR)
        
        
        
        nastRTGnr = QLabel()
        nastRTGnr.setText('Število RTG slik v vrsti:')
        
        RTGrowL = QLabel()
        RTGrowL.setText('Število RTG slik na vrstico: ')
        RTGrowSet = QComboBox(self)
        RTGrowSet.addItem(str(self.TTreportModule.getRTGperRow()))
        for nr in self.nrPerRow:
            RTGrowSet.addItem(nr)

        RTGrowSet.activated[str].connect(self.RTGnrPick)
            

        Fbtn = QPushButton("Naprej>", self)
        Fbtn.clicked.connect(self.naprejS)
        if len(self.TTreportModule.settings.groups) == 0:
            Fbtn.setEnabled(False)
        OKbtn = QPushButton("OK", self)
        OKbtn.clicked.connect(self.closeGeneral)

        layout.addRow(nastTT)
        layout.addRow(kodaL, self.koda)
        layout.addRow(namenL, self.namen)
        layout.addRow(sIzvedbaL, self.sIzvedba)
        layout.addRow(cikliL, self.cikli)
        layout.addRow(avtorL, self.avtor)
        
        
        layout.addRow(tab,IZcb)
        layout.addRow(tab,PRcb)
        layout.addRow(RTGrowL, RTGrowSet)
        
        layout.addRow(tab, Fbtn)
        layout.addRow(tab, OKbtn)
        #self.setGeometry(300, 300, 250, 150)
        self.setLayout(layout)
        #self.setLayout(layout)
        self.setWindowTitle('Nastavitve TT poročila')
        self.show()
        
        
    def groupSettings(self): #TODO definiraj funkcijo!!!
        super().__init__()
        self.setWindowIcon(QIcon('Graphic/Icons/TTreport.png'))
        layout = QFormLayout()
        
        tab = QLabel()
        tab.setText('\t')
        
        self.nastTT = QLabel()
        
        
        #nastRTGnr = QLabel()
        #nastRTGnr.setText('Število RTG slik v vrsti:')
        
        
        izvedbaL = QLabel()
        izvedbaL.setText('Izvedba svečke: ')
        self.izvedba = QLineEdit('', self)
        try:
            if self.TTreportModule.getEnakaIzvedba():
                self.izvedba.setDisabled(True)
        except Exception as e:
            pass
            #print(e)
        
        
        proceduraL = QLabel()
        proceduraL.setText('Profil TT: ')
        self.procedura = QLineEdit('', self)
        
        self.spremeniG()
        

        self.Fbtn = QPushButton("Naprej>", self)
        self.Fbtn.clicked.connect(self.naprejG)
        
        OKbtn = QPushButton("OK", self)
        OKbtn.clicked.connect(self.zapriG)
        
        self.Bbtn = QPushButton("<Nazaj", self)
        self.Bbtn.clicked.connect(self.nazajG)
        

        layout.addRow(self.nastTT)
        layout.addRow(izvedbaL, self.izvedba)
        layout.addRow(proceduraL, self.procedura)
        
        layout.addRow(self.Bbtn, self.Fbtn)
        layout.addRow(OKbtn)
        #self.setGeometry(300, 300, 250, 150)
        self.setLayout(layout)
        #self.setLayout(layout)
        self.setWindowTitle('Nastavitve TT poročila')
        self.show()
        
        
    def naprejG(self):
        self.nastaviG()
        self.iGroup += 1
        if self.iGroup >= len(self.TTreportModule.settings.groups)-1:
            self.Fbtn.setEnabled(False)
        self.spremeniG()
        
#    def setGroup(self):
#        group = self.TTreportModule.settings.groups[self.iGroup]
#        self.naslov.setText('Nastavitve skupine '+group)
#        self.izvedba.setText(str(self.TTreportModule.getIzvedba(group)))
#        self.procedura.setText(str(self.TTreportModule.getProcedura(group)))
    
    def nazajG(self):
        self.nastaviG()
        self.iGroup -= 1
        self.Fbtn.setEnabled(True)
        if self.iGroup < 0:
            self.zapriG(False)
            self.initialSettings()
        else:
            self.spremeniG()
        
        
    def RTGnrPick(self, text):
        self.TTreportModule.setRTGperRow(int(text))
        
    def setIZ(self, state):
        if state == Qt.Checked:
            self.TTreportModule.setEnakaIzvedba(True)
        else:
            self.TTreportModule.setEnakaIzvedba(False)

            
            
    def setPR(self, state):
        if state == Qt.Checked:
            self.TTreportModule.setEnakaProcedura(True)
        else:
            self.TTreportModule.setEnakaProcedura(False)
        
            

    def nastaviG(self):
        group = self.TTreportModule.settings.groups[self.iGroup]
        self.TTreportModule.setIzvedba(group, self.izvedba.text())
        self.TTreportModule.setProcedura(group, self.procedura.text())
        
    def spremeniG(self):
        group = self.TTreportModule.settings.groups[self.iGroup]
        self.nastTT.setText('Nastavitve skupine '+group)
        self.izvedba.setText(str(self.TTreportModule.getIzvedba(group)))
        self.procedura.setText(str(self.TTreportModule.getProcedura(group)))
    
    def zapriG(self, settG=True):
        if settG:
            self.nastaviG()
        self.close()
        
    def naprejS(self):
        self.closeGeneral()
        self.groupSettings()
        
            
    def closeGeneral(self):
        #TTR.setCikli('Do odpovedi.')
        self.TTreportModule.setCikli(self.cikli.text())
        #TTR.setAuthor('Andrej Mrak')
        self.TTreportModule.setAuthor(self.avtor.text())
        #TTR.setNamenTesta('Validacija upora.')
        self.TTreportModule.setNamenTesta(self.namen.text())
        #TTR.setKodaSvecke('5011-721-968')
        self.TTreportModule.setKodaSvecke(self.koda.text())
        
        self.TTreportModule.setIzvedbaSkupno(self.sIzvedba.text())
        self.close()
        
class changeFileWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.opt = True

        
    def setup(self, changeFun, path):
        super().__init__()
        self.changeFun = changeFun
        self.path = path
        self.setWindowIcon(QIcon('Graphic/Icons/transformFiles.png'))
        layout = QFormLayout()
        
        self.opt = False

        
        tab = QLabel()
        tab.setText('\t')
        
        nas = QLabel()
        nas.setText('Izberite željen pirometer za analizo (pri meritvah v kontroli):')
        
        
        radiobutton1 = QRadioButton("2B")
        radiobutton1.setChecked(True)
        radiobutton1.B = False
        radiobutton1.toggled.connect(self.changeOpt)
        
        
        radiobutton2 = QRadioButton("1B")
        #radiobutton.setChecked(True)
        radiobutton2.B = True
        radiobutton2.toggled.connect(self.changeOpt)
        
        opomba = QLabel()
        opomba.setText('(drug pirometer se vpiše pod TC)')
        
        OKbtn = QPushButton("OK", self)
        OKbtn.clicked.connect(self.transform)

        layout.addRow(nas)
        layout.addRow(radiobutton1, radiobutton2)
        layout.addRow(opomba)
        layout.addRow(tab, OKbtn)

        self.setLayout(layout)
        #self.setLayout(layout)
        self.setWindowTitle('Transformiraj meritve.')
        self.show()
#        except Exception as e:
#            print(e)
   
    def changeOpt(self):
        radioButton = self.sender()
        self.opt = radioButton.B
        
        
    def transform(self):
        self.close()
        fs = self.changeFun.change(self.path, self.opt)
        if len(fs) > 0:
            message = 'Datoteke\n'
            for f in fs:
                message += '- '+f+'\n'
            message += 'so pretvorjene in premeknjene v mapo /originals.'
        else:
            message = 'Ni datotek primernih za pretvorbo.'
        QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
        


        
            
class Settings(QWidget):#QWidget):
    
    def __init__(self, username, online=True):
        super().__init__()
        self.username = username
        self.online = online
        self.TC = "True"==readSettings(23, self.username)
        self.IG = "True"==readSettings(24, self.username)
        self.R = "True"==readSettings(21, self.username)
        self.maxlines = int(readSettings(25, self.username))#6505
        self.TT = "True"==readSettings(26, self.username)
        self.QC = readSettings(22, self.username)#"414"
        self.fname = self.readFolder()
        self.nG = 1
        self.readLegendPosition()
        
        self.tfG = self.readTitleFont()
        self.atfG = self.readAxisTitleFont()
        self.lfG = self.readLegendFont()
        self.afG = self.readAxisFont()
        self.talG = self.readtAxisLimits()
        self.UIalG = self.readUIaxisLimits()
        self.TalG = self.readTaxisLimits()
        self.lpG = self.readGLegendPosition()
    
    def readLegendPosition(self):
        
        self.nomV = readSettings(15, self.username)#'5V'
        self.stNarocila = readSettings(16, self.username)#''
        self.datumProizvodnje = readSettings(17, self.username)#''
        self.oznakaGP = int(readSettings(18, self.username))#1
        self.kodaIzdelka =  readSettings(19, self.username)#''
        self.avtor =  readSettings(20, self.username)#''
        if self.online:
            self.QCpath = readSettings(1, self.username)
        else:
            self.QCpath = 'local'
        self.readQCs()
        if readSettings(2, self.username) == 'True':
            self.openReport = True
        else:
            self.openReport = False
        if readSettings(3, self.username) == 'True':
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
        
        
    def analize(self, QCs, TTreportModule):    
        #podatki.get_QC()
        super().__init__()
        self.setWindowIcon(QIcon('Graphic/Icons/measSett.png'))
        layout = QFormLayout()
        
        self.TTRW = TTreportWindow(TTreportModule, self.username)
        tab = QLabel()
        tab.setText('\t')
        
        nastFun = QLabel()
        nastFun.setText('Nastavitve za funkcionalno analizo')
        
        QCset = QComboBox(self)
        for qc in QCs:
            if qc == "":
                if self.QC in QCs:
                    QCset.addItem(self.QC)
                else:
                    QCset.addItem("Nastavi QC           ")
                    self.QC = "5011-721-414"
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
        
        TTcb = QCheckBox('Dodaj stolpec za TT', self)
        if self.TT:
            TTcb.toggle()
        TTcb.stateChanged.connect(self.setTT)
        
        TTbtn = QPushButton("Nastavitve TT poročila", self)
        TTbtn.clicked.connect(self.TTRW.initialSettings)
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
            self.author.setText(self.username)#self.avtor)#login.username)
            
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
        layout.addRow(TTcb)
        layout.addRow(tab)
        layout.addRow(TTbtn)
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
        try:
           if not self.GPnumber.text() == '':
               try:
                   self.oznakaGP = int(self.GPnumber.text())
                   saveSettings(18, str(self.oznakaGP), self.username)
                   intOK = True
               except:
                   #print('Gpnr: ',self.GPnumber.text())
                   message = 'Oznaka 1. vzorca je lahko le celo število.'
                   intOK = False
                   QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)
               if intOK:
                   self.stNarocila =  str(self.narocilo.text())
                   saveSettings(16, self.stNarocila, self.username)
                   self.datumProizvodnje =  str(self.proizvodnja.text())
                   saveSettings(17, self.datumProizvodnje, self.username)
                   self.kodaIzdelka =  str(self.GPcode.text())
                   if not self.kodaIzdelka == '' and not self.kodaIzdelka[-3:] == '200':
                       self.kodaIzdelka += '-200'
                   saveSettings(19, self.kodaIzdelka, self.username)
                   self.avtor =  str(self.author.text())
                   saveSettings(20, self.avtor, self.username)
                   #print('št. naročila: ', self.stNarocila)
                   #print('Datum proizvodnje: ', self.datumProizvodnje)
                   #print('Koda izdelka: ', self.kodaIzdelka)
                   #print('Oznaka 1. vzorca: ', self.oznakaGP)
                   #print('Avtor: ', self.avtor)
                   self.close()
           else:
                #print('Gpnr: _',self.GPnumber.text())
                self.close()
        except Exception as e:
            pass
            #print(e)

       
    
            
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
        graph.setText('Št. meritev na graf: ')
        self.GraphNr = QLineEdit('', self)
        self.GraphNr.setText(str(self.nG))
        
        graphTitle = QLabel()
        graphTitle.setText('Velikost pisave naslova: ')
        self.GraphTFont = QLineEdit('', self)
        self.GraphTFont.setText(str(self.tfG))
        graphAxisT = QLabel()
        graphAxisT.setText('Velikost pisave naslovov osi: ')
        self.GraphAxTFont = QLineEdit('', self)
        self.GraphAxTFont.setText(str(self.atfG))
        graphLegendF = QLabel()
        graphLegendF.setText('Velikost pisave legende: ')
        self.LegendF = QLineEdit('', self)
        self.LegendF.setText(str(self.lfG))
        graphAx = QLabel()
        graphAx.setText('Velikost pisave osi: ')
        self.GraphAxFont = QLineEdit('', self)
        self.GraphAxFont.setText(str(self.afG))
        
        graphXlim = QLabel()
        graphXlim.setText('Meje X osi:')
        self.GraphXlim = [QLineEdit('', self), QLineEdit('', self)]
        self.GraphXlim[0].setText(str(self.talG[0]))
        self.GraphXlim[1].setText(str(self.talG[1]))
        
        graphY1lim = QLabel()
        graphY1lim.setText('Meje Y1 (UI) osi:')
        self.GraphY1lim = [QLineEdit('', self), QLineEdit('', self)]
        self.GraphY1lim[0].setText(str(self.UIalG[0]))
        self.GraphY1lim[1].setText(str(self.UIalG[1]))
        
        graphY2lim = QLabel()
        graphY2lim.setText('Meje Y2 (T) osi:')
        self.GraphY2lim = [QLineEdit('', self), QLineEdit('', self)]
        self.GraphY2lim[0].setText(str(self.TalG[0]))
        self.GraphY2lim[1].setText(str(self.TalG[1]))

        #TODO  dodaj še pozicijo legende
        #self.lpG 
        
        tab = QLabel()
        tab.setText('\t')
        
        OKbtn = QPushButton("OK", self)
        #OKbtn.move(250, 120)
        #GraphBtn = QPushButton(str(self.nG) + " meritve/ev na 1 graf", self)
        #GraphBtn.move(20, 30)
        layout.addRow(graph, self.GraphNr)
        layout.addRow(IGcb)
        layout.addRow(graphTitle, self.GraphTFont)
        layout.addRow(graphAxisT, self.GraphAxTFont)
        layout.addRow(graphLegendF, self.LegendF)
        layout.addRow(graphAx, self.GraphAxFont)
        layout.addRow(graphXlim, self.GraphXlim[0])
        layout.addRow(tab, self.GraphXlim[1])
        layout.addRow(graphY1lim, self.GraphY1lim[0])
        layout.addRow(tab, self.GraphY1lim[1])
        layout.addRow(graphY2lim, self.GraphY2lim[0])
        layout.addRow(tab, self.GraphY2lim[1])
        
        layout.addRow(tab, OKbtn)
        
        
        
        #self.setGeometry(300, 300, 350, 150)
        self.setLayout(layout)
        self.setWindowTitle('Nastavitve grafov')
        
        OKbtn.clicked.connect(self.closeBoxG)
        #GraphBtn.clicked.connect(self.GraphDialog)
        
        self.show()
        
    def closeBoxG(self):
       if not self.GraphNr.text() == '':
           intOK = True
           try:
               nG = int(self.GraphNr.text())
               if nG > 0:
                   self.nG = nG
                   
               else:
                   #print('Gpnr: ',self.GraphNr.text())
                   message = 'Število meritev na graf je lahko le naravno število.'
                   intOK = False
                   QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)
           except:
               #print('Gpnr: ',self.GraphNr.text())
               message = 'Število meritev na graf je lahko le pozitivno število.'
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)
           message = 'Velikost pisave je lahko le naravno število.'
           try:
               num = float(self.GraphTFont.text())
               if num > 0:
                   self.tfG = num
                   saveSettings(4, str(num), self.username)
               else:
                   #print('Gpnr: ',self.GraphNr.text())
                   
                   intOK = False
                   QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)
           except:
               #print('Gpnr: ',self.GraphNr.text())
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok) 
           try:
               num = float(self.GraphAxTFont.text())
               if num > 0:
                   self.atfG = num
                   saveSettings(5, str(num), self.username)
               else:
                   #print('Gpnr: ',self.GraphNr.text())
                   
                   intOK = False
                   QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)
           except:
               #print('Gpnr: ',self.GraphNr.text())
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok) 
           try:
               num = float(self.LegendF.text())
               if num > 0:
                   self.lfG = num
                   saveSettings(6, str(num), self.username)
               else:
                   #print('Gpnr: ',self.GraphNr.text())
                   
                   intOK = False
                   QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)
           except:
               #print('Gpnr: ',self.GraphNr.text())
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok) 
           try:
               num = float(self.GraphAxFont.text())
               if num > 0:
                   self.afG = num
                   saveSettings(7, str(num), self.username)
               else:
                   intOK = False
                   QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)
           except:
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok) 
           message = 'Meje osi so lahko le realno število.'
           try:
               self.talG[0]  = float(self.GraphXlim[0].text())
               saveSettings(8, str(self.talG[0]), self.username)
           except:
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)  
           try:
               self.talG[1]  = float(self.GraphXlim[1].text())
               saveSettings(9, str(self.talG[1]), self.username)
           except:
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)    
           try:
               self.UIalG[0]  = float(self.GraphY1lim[0].text())
               saveSettings(10, str(self.UIalG[0]), self.username)
           except:
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok) 
           try:
               self.UIalG[1]  = float(self.GraphY1lim[1].text())
               saveSettings(11, str(self.UIalG[1]), self.username)
           except:
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok) 
           try:
               self.TalG[0]  = float(self.GraphY2lim[0].text())
               saveSettings(12, str(self.TalG[0]), self.username)
           except:
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)
           try:
               self.TalG[1]  = float(self.GraphY2lim[1].text())
               saveSettings(13, str(self.TalG[1]), self.username)
           except:
               intOK = False
               QMessageBox.warning(self, 'Opozorilo.', message, QMessageBox.Ok, QMessageBox.Ok)               
           if intOK:
               #print('sm tu')
               self.close()
       else:
            #print('sm pa tu')
            self.close()
        
        
    def programa(self, login):
        
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
        
        if not self.online:
            QCpath.setEnabled(False)
        
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
        
        
#    def analizaMeritev(self, main):
#
#        self.setGeometry(300, 300, 350, 150)
#        self.setWindowTitle('Izdelava analize meritev')
#        self.show()
#        
#        quit()
#        
#        
#    def izdelavaTcPoročila(self, main):
#
#        self.setGeometry(300, 300, 350, 150)
#        self.setWindowTitle('Izdelava TC poročila')
#        self.show()
#        self.lastFiles = start.TC_report(main)
#        quit()
        

        
        
            
    def setTC(self, state):
        if state == Qt.Checked:
            self.TC = True
        else:
            self.TC = False
        saveSettings(23, str(self.TC), self.username)
        #print('TC:',self.TC)
        
    def setR(self, state):
        if state == Qt.Checked:
            self.R = True
        else:
            self.R = False
        saveSettings(21, str(self.R), self.username)
        #print('R:',self.R)
        
    def setTT(self, state):
        if state == Qt.Checked:
            self.TT = True
        else:
            self.TT = False
        saveSettings(26, str(self.TT), self.username)
        
        
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
            #print('nG:', self.nG)
        

        
    def setIG(self, state):
        if state == Qt.Checked:
            self.IG = True
        else:
            self.IG = False
        saveSettings(24, str(self.IG), self.username)
        #print('IG:',self.IG)
        
        
    def setQCpath(self, state):
        if state == Qt.Checked:
            self.QCpath = 'local'
        else:
            self.QCpath = 'global'
        saveSettings(1, self.QCpath, self.username)
        self.readQCs()
        
        #print('QCpath:', self.QCpath)
        
        
    def readQCs(self):
        #print('QCp:',self.QCpath)
        if self.QCpath == 'local':
            fileName = 'QC/QC.txt'
        else:
            fileName = globalPaths.path.QC
        file=open(fileName, 'r', encoding="utf-8").read()   
        self.QCs=[]
        for qc in file.split('QC'):
            self.QCs.append(qc.split('>')[0].split('<')[-1])
        #print('QCp:',self.QCs)
        
        
    def setOpenReport(self, state):
        if state == Qt.Checked:
            self.openReport = True
        else:
            self.openReport = False
        saveSettings(2, str(self.openReport), self.username)
        
        #print('openReport:', self.openReport)
        
        
        
    def setTCshow(self, state):
        if state == Qt.Checked:
            self.showTC = True
        else:
            self.showTC = False
        saveSettings(3, str(self.showTC), self.username)
        #print('show TC:', self.showTC)
        
    def setVW(self, state):
        if state == Qt.Checked:
            self.maxlines = 6505
        else:
            self.maxlines = 6005
        saveSettings(25, str(self.maxlines), self.username)
        #print('maxlines:',self.maxlines)
        
    def QCpick(self, text):
        
        if text == "Nastavi QC":
            self.QC = "414"
        else:
            self.QC = text
        saveSettings(22, str(self.QC), self.username)
        #print(self.QC)
        
    def Vpick(self, text):
        self.nomV = text
        #print(self.nomV)
        
    def readFolder(self):
        return readSettings(0, self.username)
    
    def readTitleFont(self):
        return float(readSettings(4, self.username))
    
    def readAxisTitleFont(self):
        return float(readSettings(5, self.username))
    
    def readLegendFont(self):
        return float(readSettings(6, self.username))
    
    def readAxisFont(self):
        return float(readSettings(7, self.username))
    
    def readtAxisLimits(self):
        return [float(readSettings(8, self.username)), float(readSettings(9, self.username))]
    
    def readUIaxisLimits(self):
        return [float(readSettings(10, self.username)), float(readSettings(11, self.username))]
    
    def readTaxisLimits(self):
        return [float(readSettings(12, self.username)), float(readSettings(13, self.username))]
    
    def readGLegendPosition(self):
        return readSettings(14, self.username)
    
    
    
    
    
    def printLastFiles(self):
        if len(self.lastFiles) > 0:
            self.printDialog(self.lastFiles)
        else:
            message = 'V spominu ni nobene datoteke.'
            QMessageBox.information(self, 'Obvestilo.', message, QMessageBox.Ok, QMessageBox.Ok)
    
    def printFiles(self):
        filters = "XLSX (*.xlsx);;XLSM (*.xlsm);;TXT (*.txt);;PDF (*.pdf);;DOCX (*.docx);;DOC (*.doc);;ALL (*)"
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
                                           documentString+'\nNadaljuj? Še enkrat premislite - okolje vam bo hvaležno :)', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            printProgram.printFiles(files)
        
        
#if __name__ == '__main__':
#    
#    app = QApplication(argv)
#    ex = Main(["","Ubuntuehrejhtjtejee", "Mandriva", "Fedora", "Arch", "Gentoo"])
#    exit(app.exec_())

    