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
    
    def __init__(self, ver):
        self.startLog(ver)
        
    def startLog(self, ver):
        localUserFile = open('Graphic/Icons/User.png', 'r')
        localLines = localUserFile.readlines()
        localUserFile.close()
        
        if len(localLines) == 0:
            self.localUsername = getuser()
            print('startUser')
        else:
            self.localUsername = self.Decode(localLines[0].strip('\n'))
            
        localUserFile = open('Graphic/Icons/User.png', 'w')
        
        try:
            try:
                userFile = open(globalPaths.paths.izmenjava+'Andrej_Mrak/__Nove_Meritve/_Reports/Usage/' + self.localUsername + '.log', 'r')
                lines = userFile.readlines()
                userFile.close()
            except:
                lines = []
            userFile = open(globalPaths.paths.izmenjava+'Andrej_Mrak/__Nove_Meritve/_Reports/Usage/' + self.localUsername + '.log', 'w')
            userFileLocation = open(globalPaths.paths.izmenjava+'Andrej_Mrak/__Nove_Meritve/_Reports/Usage/' + self.localUsername + '_location.log', 'a')
            for line in lines:
                userFile.write(line)
            
            
            localUserFile.write(self.Code(self.localUsername) + '\n')
            if len(localLines)>1:
                for localLine in localLines[1:]:
                    localLine = self.Decode(localLine.strip('\n'))
                    for data in localLine.split('_'):
                        userFile.write(data + '\t')
                    userFile.write('local\n')
            userFile.write(getuser() + ':\t' + strftime("%d.%m.%y") + '\t' + strftime("%H:%M:%S") + '\t' + ver + '\n')
            userFileLocation.write(getuser() + ':\t' + strftime("%d.%m.%y") + '\t' + strftime("%H:%M:%S") + '\t' + ver + '\n')
            userFile.close()
            userFileLocation.close()
        except:
            localUserFile.write(self.Code(self.localUsername) + '\n')
            if len(localLines)>1:
                for localLine in localLines[1:]:
                    localUserFile.write(localLine)
            localUserFile.write(self.Code(getuser() + ':_' + strftime("%d.%m.%y") + '_' + strftime("%H:%M:%S")) + '\t ver:' + ver + '\n')
        localUserFile.close()

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
            userFile = open(globalPaths.paths.izmenjava+'Andrej_Mrak/__Nove_Meritve/_Reports/Usage/' + self.localUsername + '_location.log', 'a')
            userFile.write('\t' + function + '  ' + location + '\n')
            userFile.close()       
        except:
            pass
    


