# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 08:58:03 2020

@author: andmra2
"""
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import sqlite3
from sqlite3 import Error
from os import remove, listdir

class userCreator(object):
    
    def __init__(self):
        self.path = '//corp.hidria.com/aet/SI-TO-Izmenjava/Andrej_Mrak/ProgramData/AFM/newUserRequests/'
        
    def getRequestDetails(self, ID):
        pr_key = RSA.import_key(open('private_pem.pem', 'r').read())
        decrypt = PKCS1_OAEP.new(key=pr_key)
        
        passwordHash = b''
        with open(self.path+ID+'_0.req', 'rb') as req:
            encrUsername = req.read()
        username = decrypt.decrypt(encrUsername)
        for i in range(1,11):
            with open(self.path+ID+'_'+str(i)+'.req', 'rb') as req:
                passwordHash += decrypt.decrypt(req.read())
        return username, passwordHash
    
    def encryptUserData(self, username, passwordHash, userType='normal'):
        pu_key = RSA.import_key(open('public_pem.pem', 'r').read())
        cipher = PKCS1_OAEP.new(key=pu_key)
        salt = passwordHash[:64]
        BuserType = salt+bytes(userType, 'utf-8')
        sqlRow = ()
        sqlRow += (cipher.encrypt(username),)
        sqlRow += (cipher.encrypt(BuserType),)
        for i in range(10):
            sqlRow += (cipher.encrypt(passwordHash[i*20:i*20+20]),)
        return sqlRow
    
    def createConnection(self):
        """ create a database connection to a SQLite database """
        conn = None
        dbFile = '//corp.hidria.com/aet/SI-TO-Izmenjava/Andrej_Mrak/ProgramData/AFM/users/usersSettings.db'
        try:
            conn = sqlite3.connect(dbFile)
            #print(sqlite3.version)
        except Error as e:
            print(e)
        return conn
    
    def createUserAuthTable(self):
        conn = self.createConnection()
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        create_table_sql = """CREATE TABLE IF NOT EXISTS UserAuth (
                                    username varbinary NOT NULL,
                                    status varbinary NOT NULL,
                                    hash1 varbinary NOT NULL,
                                    hash2 varbinary NOT NULL,
                                    hash3 varbinary NOT NULL,
                                    hash4 varbinary NOT NULL,
                                    hash5 varbinary NOT NULL,
                                    hash6 varbinary NOT NULL,
                                    hash7 varbinary NOT NULL,
                                    hash8 varbinary NOT NULL,
                                    hash9 varbinary NOT NULL,
                                    hash10 varbinary NOT NULL
                                );"""
        with conn:
            c = conn.cursor()
            c.execute(create_table_sql)
            
    def createUser(self, user):
        conn = self.createConnection()
        """
        Create a new task
        :param conn:
        :param task:
        :return:
        """
     
        sql = ''' INSERT INTO UserAuth(username,status,hash1,hash2,hash3,hash4,hash5,hash6,hash7,hash8,hash9,hash10)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
        with conn:
            cur = conn.cursor()
            cur.execute(sql, user)
        return cur.lastrowid
    
    def deleteRequest(self, ID):
        for i in range(11):
            remove(self.path+ID+"_"+str(i)+".req") 
            
            
    def updateUser(self, data):
        conn = self.createConnection()
        data = data[1:]+(data[0],)
        #print(type(data[0]))
        sql = """UPDATE UserAuth
                 SET hash1 = ?,
                    hash2 = ?,
                    hash3 = ?,
                    hash4 = ?,
                    hash5 = ?,
                    hash6 = ?,
                    hash7 = ?,
                    hash8 = ?,
                    hash9 = ?,
                    hash10 = ?
                WHERE
                    username = ?;"""
                    #            FROM
                    #username
#        print(sql)
#        print()
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
        
                    


    
    def resolveReqest(self, ID):
        username, paswordHash = self.getRequestDetails(ID)
        strUser = username.decode("utf-8") 
        created = False
        isStored, encryUser = self.isStoredUser(username)
        if isStored:
            cont = input('Update user '+strUser+'? (y/n)')
            if cont.lower() == 'y': 
                try:
                    sqlLine = self.encryptUserData(username, paswordHash)
                    sqlLine = (encryUser,)+sqlLine[2:]
                    self.updateUser(sqlLine)
                    created = True
                    print('User '+strUser+' updated.')
                except Exception as e:
                    print(e)
            else:
                cont = input('Delete request from user '+strUser+'? (y/n)')
                if cont.lower() == 'y':
                    self.deleteRequest(ID)
        else:
            cont = input('Create user '+strUser+'? (y/n)')
            if cont.lower() == 'y':
                cont = input('Set as admin '+strUser+'? (y/n)')
                if cont == 'y':
                    ut = 'admin'
                else:
                    ut = 'normal'
                sqlLine = self.encryptUserData(username, paswordHash, ut)
                self.createUser(sqlLine)
                created = True
                print('User '+strUser+' created.')
            else:
                cont = input('Delete request from user '+strUser+'? (y/n)')
                if cont.lower() == 'y':
                    self.deleteRequest(ID)
        if created:
            self.deleteRequest(ID)
            
            
    def returnUsernames(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        conn = self.createConnection()
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT username FROM UserAuth")
         
            rows = cur.fetchall()
        return rows
    
    def decryptStoredUsers(self):
        keyFile = '//corp.hidria.com/aet/SI-TO-Izmenjava/Andrej_Mrak/ProgramData/AFM/encryption/private_pem.pem'
        pr_key = RSA.import_key(open(keyFile, 'r').read())
        decrypt = PKCS1_OAEP.new(key=pr_key)
        usernames = []
        for encrUsername in self.returnUsernames():
            usernames.append([decrypt.decrypt(encrUsername[0]), encrUsername[0]])
        return usernames
    
    def isStoredUser(self, username):
        for pair in self.decryptStoredUsers():
            if username == pair[0]:
                return True, pair[1]
        return False, None
    
    def checkRequests(self):
        files = listdir(self.path)
        requests = []
        for r in files:
            if r.split('_')[0] not in requests:
                requests.append(r.split('_')[0])
        for request in requests:
            self.resolveReqest(request)
        
                    
                
                    
#    def decryptUsername(self, encrUsername):
#        fileName = '//corp.hidria.com/aet/SI-TO-Izmenjava/Andrej_Mrak/ProgramData/AFM/encryption/private_pem.pem'
#        pr_key = RSA.import_key(open(fileName, 'r').read())
#        decrypt = PKCS1_OAEP.new(key=pr_key)
#        try:
#            return decrypt.decrypt(encrUsername).decode("utf-8")
#        except Exception as e:
#            print(e)
#            return None
        
    
    

if __name__ == "__main__":
    uc = userCreator()
    #
    #uc.resolveReqest('2001231012')
    try:
        uc.checkRequests()
    except:
        uc.createUserAuthTable()
#print(getRequestDetails('2001221117'))
        
    #user = decrypt.decrypt(cipher_text)