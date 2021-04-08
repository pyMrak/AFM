# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 15:36:02 2020

@author: andmra2
"""
import hashlib, binascii, os
from datetime import datetime
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import sqlite3
from sqlite3 import Error
from PyQt5 import QtWidgets, QtGui


from libs.globalPaths import path



class loginModule(object):
    
    def __init__(self):
        pr_key = RSA.import_key(open(path.encryption+'private_pem.pem', 'r', encoding="utf-8").read())
        self.decrypt = PKCS1_OAEP.new(key=pr_key)
        self.username = ''
        self.userType = 'normal'


    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                      salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt+pwdhash).decode('ascii')
     
    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                      provided_password.encode('utf-8'), 
                                      salt.encode('ascii'), 
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    
    def sendNewUserRequest(self, username, password):
        hashedPassword= self.hash_password(password)
        pu_key = RSA.import_key(open(path.encryption+'public_pem.pem', 'r', encoding="utf-8").read())
        cipher = PKCS1_OAEP.new(key=pu_key)
        BhashedPassword = bytes(hashedPassword, 'utf-8')
        Busername = bytes(username, 'utf-8')
        encryHash = []
        for i in range(10):
            encryHash.append(cipher.encrypt(BhashedPassword[i*20:i*20+20]))
        encryUser = cipher.encrypt(Busername)
        fileName = datetime.now().strftime("%y%m%d%H%M%S")
        with open(path.newUserRequests+fileName+'_0.req', 'wb', encoding="utf-8") as req:
            req.write(encryUser)
        
        for i, h in enumerate(encryHash):
            with open(path.newUserRequests+fileName+'_'+str(i+1)+'.req', 'wb', encoding="utf-8") as req:
                req.write(h)
                
    def decryptUsername(self, encrUsername):
        try:
            return self.decrypt.decrypt(encrUsername).decode("utf-8")
        except Exception as e:
            #print(e)
            return None
    
    def decryptPasswordHash(self, encrPasswordHashTuple):
        passwordHash = b''
        for eph in encrPasswordHashTuple:
            passwordHash += self.decrypt.decrypt(eph)
        return passwordHash
    
    def checkPassword(self, password, userData):
        passHash = self.decryptPasswordHash(userData[2:]).decode('ascii')
        return self.verify_password(passHash, password)
    
    def decryptUserType(self, encrUserType):
        return self.decrypt.decrypt(encrUserType).decode("utf-8")
    
    def createConnection(self):
        """ create a database connection to a SQLite database """
        conn = None
        dbFile = path.usersDatabase + 'usersSettings.db'
        try:
            conn = sqlite3.connect(dbFile)
            #print(sqlite3.version)
        except Error as e:
            pass#print(e)
        return conn
    
    def returnUsersAuthData(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        conn = self.createConnection()
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM UserAuth")
         
            rows = cur.fetchall()
        return rows
    
    def login(self, username, password):
        data = self.returnUsersAuthData()
        #print('len:', len(data))
        #print(self.decryptUsername(data[0][0]))
        #print(self.decryptUsername(data[1][0]))
        for d in data:
            if username == self.decryptUsername(d[0]):
                if self.checkPassword(password, d):
                    self.username = username
                    self.userType = self.decryptUserType(d[1])[64:]
                    return 'OK', self.decryptUserType(d[1])[64:]
                else:
                    #print('Gelso ni pravo.')
                    return 'badPassword', None
        return 'noUser', None


logMod = loginModule()


class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        #super().__init__()
        self.sendReq = sendRequest()
        self.setWindowIcon(QtGui.QIcon('Graphic/Icons/windowIcon.ico'))
        #self.loginModule = loginModule()
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.buttonLogin = QtWidgets.QPushButton('Prijava', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.buttonReq = QtWidgets.QPushButton('Pozabljeno geslo? Nov uporabnik?', self)
        self.buttonReq.clicked.connect(self.openReq)
        layout = QtWidgets.QFormLayout(self)#QVBoxLayout(self)
        up = QtWidgets.QLabel()
        up.setText('Uporabniško ime:')
        ge = QtWidgets.QLabel()
        ge.setText('Geslo:')
        layout.addRow(up, self.textName)
        layout.addRow(ge, self.textPass)
        layout.addRow(self.buttonLogin)
        layout.addRow(self.buttonReq)
        self.setWindowTitle('Prijava v program.')
        self.show()

    def handleLogin(self):
        status, userType = logMod.login(self.textName.text(), self.textPass.text())
        if status == 'OK':
            self.accept()
        elif status == 'noUser':
            QtWidgets.QMessageBox.warning(
                self, 'Napaka', 'Uporabnik ne obstaja')
        elif status == 'badPassword':
            QtWidgets.QMessageBox.warning(
                self, 'Napaka', 'Napačno geslo.')
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Napaka', 'Neznana napaka.')
            
    def openReq(self):
        self.sendReq.setUsername(self.textName.text())
        self.sendReq.openDialog()
        #self.sendReq.exec_()
            

            
class sendRequest(QtWidgets.QWidget):
    def __init__(self):
        self.username = ''
        
    def setUsername(self, username):
        self.username = username
        
        
    def openDialog(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('Graphic/Icons/windowIcon.ico'))
        self.textName = QtWidgets.QLineEdit(self)
        self.textName.setText(self.username)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonReq = QtWidgets.QPushButton('Pošlji zahtevo.', self)
        self.buttonReq.clicked.connect(self.handleReq)
        layout = QtWidgets.QFormLayout(self)#QVBoxLayout(self)
        nas = QtWidgets.QLabel()
        nas.setText('Vnesite svoje podatke:')
        up = QtWidgets.QLabel()
        up.setText('Uporabniško ime:')
        ge = QtWidgets.QLabel()
        ge.setText('(Novo) geslo:')
        op = QtWidgets.QLabel()
        op.setText('POZOR! Izberite geslo, ki ga ne uporabljate za drug račun.')
        layout.addRow(nas)
        layout.addRow(up, self.textName)
        layout.addRow(ge, self.textPass)
        layout.addRow(op)
        layout.addRow(self.buttonReq)
        self.setWindowTitle('Pošlji zahtevo za novega uporabnika oz. geslo.')
        self.show()
        



    def handleReq(self):
        if self.textName.text() != '':
            if len(self.textPass.text()) > 3:
                try:
                    logMod.sendNewUserRequest(self.textName.text(), self.textPass.text())
                    QtWidgets.QMessageBox.information(
                            self, 'Obvestilo', 'Zahteva poslana.\nProsimo počakajte da administrator potrdi vašo zahtevo.')
                except Exception as e:
                    QtWidgets.QMessageBox.warning(
                            self, 'Napaka', str(e))
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, 'Napaka', 'Geslo mora vsebovati vsaj 4 znake.')
        else:
            QtWidgets.QMessageBox.warning(self, 'Napaka', 'Uporabniško ime je prazno.')
        
        

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())        
    

    








