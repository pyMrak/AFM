# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 15:25:13 2017

@author: andmra2
"""
from getpass import getuser
from time import strftime
from libs import globalPaths


class newLog():
    characters = 'abcčdefghijklmnoprstuvzžqxywABCČDEFGHIJKLMNOPRSŠTUVZŽQXYW1234567890.:_'
    code = 'IN)hn43098jOIJDJĆ()#z98jhd=ZwdEFF7t542wabxa987%ESG809#SXffm097ds83GERXkd.yhq6mammd%/(amxykjDEWh9908<H/FN9090DNkAKoLKJND&6zdcb76fGZGDS6zgdj(/Gdb8wh(&D"Ghslmcbbvz75/$Dfcvghsjmuw56f2hjLDvkw62ftxujHBkcxbk(/&"&Egikxbwi6)984tgh9bnn)/TF(GIJKASNC(#GGh)/InidbduwdGSHAuhd6%VshjkWtsjMFIa76IUHD/&GEDhdusodjn5rqghajDSVX4r8da29ak>jsz(&TGFHBD876gf94,.ZFDGo4gDv8chSo'
    
    def __init__(self, ver, login):
        #print(login)
        if login:
            self.localUsername = login.username
        else:
            self.localUsername = 'Debug'
        self.startLog(ver)
        
    def startLog(self, ver):
        #localUserFile = open('Graphic/Icons/User.png', 'r')
        #localLines = localUserFile.readlines()
        #localUserFile.close()
        
#        if len(localLines) == 0:
#            self.localUsername = getuser()
#            print('startUser')
#        else:
#            self.localUsername = self.Decode(localLines[0].strip('\n'))
            
        #localUserFile = open('Graphic/Icons/User.png', 'w')
        
        try:
            try:
                userFile = open(globalPaths.path.usage + self.localUsername + '.log', 'r', encoding="utf-8")
                lines = userFile.readlines()
                userFile.close()
            except:
                lines = []
            userFile = open(globalPaths.path.usage + self.localUsername + '.log', 'w', encoding="utf-8")
            userFileLocation = open(globalPaths.path.usage + self.localUsername + '_location.log', 'a', encoding="utf-8")
            for line in lines:
                userFile.write(line)
            
            
            #localUserFile.write(self.Code(self.localUsername) + '\n')
#            if len(localLines)>1:
#                for localLine in localLines[1:]:
#                    localLine = self.Decode(localLine.strip('\n'))
#                    for data in localLine.split('_'):
#                        userFile.write(data + '\t')
#                    userFile.write('local\n')
            userFile.write(getuser() + ':\t' + strftime("%d.%m.%y") + '\t' + strftime("%H:%M:%S") + '\t' + ver + '\n')
            userFileLocation.write(getuser() + ':\t' + strftime("%d.%m.%y") + '\t' + strftime("%H:%M:%S") + '\t' + ver + '\n')
            userFile.close()
            userFileLocation.close()
        except:
            pass
            #localUserFile.write(self.Code(self.localUsername) + '\n')
            #if len(localLines)>1:
                #for localLine in localLines[1:]:
                    #localUserFile.write(localLine)
            #localUserFile.write(self.Code(getuser() + ':_' + strftime("%d.%m.%y") + '_' + strftime("%H:%M:%S")) + '\t ver:' + ver + '\n')
        #localUserFile.close()

    def Code(self, string):
        codedOutput = ''
        for char in string:
            for i, cChar in enumerate(self.characters):
                if cChar == char:
                    codedOutput += self.code[i*5:i*5+5]
                    break
        return codedOutput
    
    def Decode(self, string):
        decodedOutput = ''
        for j in range(int(len(string)/5)):
            for i in range(len(self.characters)):
                if self.code[i*5:i*5+5] == string[j*5:j*5+5]:
                    decodedOutput += self.characters[i]
                    break
        return decodedOutput
        
        
    def writeLocation(self, function, location):
        try:
            userFile = open(globalPaths.path.usage + self.localUsername + '_location.log', 'a', encoding="utf-8")
            userFile.write('\t' + function + '  ' + location + '\n')
            userFile.close()       
        except Exception as e:
            pass
            #print(e)
    
class messageLogger():
    
    def __init__(self):
        self.fileName = 'logfile.log'
        
    def reset(self):
        logFile = open(self.fileName, 'w', encoding="utf-8")
        logFile.write('')
        logFile.close()
        
    def writeProgressInfo(self, msg, app, isMD=True):
        logFile = open(self.fileName, 'a', encoding="utf-8")
        logFile.write('\nProgress INFO: '+msg)
        logFile.close()
        if isMD:
            app = app.gdat
        app.statusBar().showMessage('Progress INFO: '+msg)
        
    def writeWarning(self, msg, app, isMD=True):
        logFile = open(self.fileName, 'a', encoding="utf-8")
        logFile.write('\n!WARNING!: '+msg)
        logFile.close()
        if isMD:
            app = app.gdat
        app.statusBar().showMessage('!WARNING!: '+msg)
        
    def writeError(self, msg, app, isMD=True):
        logFile = open(self.fileName, 'a', encoding="utf-8")
        logFile.write('\n!!!ERROR!!!: '+msg)
        logFile.close()
        if isMD:
            app = app.gdat
        app.statusBar().showMessage('!!!ERROR!!!: '+msg)
        
    def append(self, msg, app, isMD=True):
        logFile = open(self.fileName, 'a', encoding="utf-8")
        logFile.write(msg)
        logFile.close()
        if isMD:
            app = app.gdat
        app.statusBar().showMessage(self.readLog())
        
        
    def readLog(self):
        logFile = open(self.fileName, 'r', encoding="utf-8")
        msg = logFile.readlines()[-1]
        logFile.close()
        return msg
    
    def check(self):
        logFile = open(self.fileName, 'r', encoding="utf-8")
        lines = logFile.readlines()
        logFile.close()
        err = []
        war = []
        for line in lines:
            if 'ERROR' in line:
                err.append(line.strip('\n'))
            elif 'WARNING' in line:
                war.append(line.strip('\n'))
        string = ''
        for w in war:
            string += w + '\n'
        for e in err:
            string += e + '\n'
        return string[:-1], len(war), len(err)
        
            
                

