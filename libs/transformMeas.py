# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 09:47:06 2019

@author: andmra2
"""
from os import rename, listdir, mkdir

from shutil import move
from os.path import isdir
from numpy import zeros

#path = 'Medo mer/'#//corp.hidria.com/aet/SI-TO-Izmenjava/Kobal/VW/Meritev Kontrola/
#trPath = 'transformed/'


class transformMedoMeas(object):
    
    def __init__(self):
        self.originalFolder = 'originals'
        
    def readFile(self, fileName, switch, prevzem=False):
        #print('switch:', switch)
        file = open(fileName, 'r', encoding="utf-8")
        lines = file.readlines()
        file.close()
        
        if prevzem:
            mL = len(lines)
            mN = len(lines[0].split('\t'))
            N = int((mN-1)/5)
            mN = N*4+1
            fileStructure = zeros((mN,mL-1))
            locations = zeros(mN, dtype='int8')
            #print(mL, mN, N)
            try:
                for i, ch in enumerate(lines[0].split('\t')):
                    if ch == 't(s)':
                        locations[0] = i
                    elif ch[0] == 'U':
                        nr = int(ch[2])
                        locations[nr*4-3] = i
                    elif ch[0] == 'I':
                        nr = int(ch[2])
                        locations[nr*4-2] = i
                    elif  ch[0:2] == 'T[':
                        nr = int(ch[2])
                        locations[nr*4] = i
                    elif  ch[0:2] == 'T1':
                        nr = int(ch[3])
                        locations[nr*4-1] = i
            except Exception as e:
                pass
                #print(e)
        else:
            mL = len(lines)
            mN = len(lines[0].split('\t'))
            N = int((mN-1)/4)
            fileStructure = zeros((mN,mL-1))
            locations = zeros(mN, dtype='int8')
            for i, ch in enumerate(lines[0].split('\t')):
                if ch == 't(s)':
                    locations[0] = i
                elif ch[0] == 'U':
                    nr = int(ch[2])
                    locations[nr*4-3] = i
                elif ch[0] == 'I':
                    nr = int(ch[2])
                    locations[nr*4-2] = i
                elif  ch[0:2] == 'T1':
                    nr = int(ch[3])
                    if switch:
                        locations[nr*4] = i
                    else:
                        locations[nr*4-1] = i
                elif  ch[0:2] == 'T2':
                    nr = int(ch[3])
                    if switch:
                        locations[nr*4-1] = i
                    else:
                        locations[nr*4] = i
        for i, line in enumerate(lines[1:]):
            line = line.replace(',','.').strip('\n').split('\t')
            for j, loc in enumerate(locations):
                fileStructure[j,i] = float(line[loc])
        return fileStructure
    
    def saveFiles(self, fileStructure, fileName=''):
        if fileName != '':
            fileName = fileName.strip('.txt')
        mN = fileStructure.shape[0]

        N = int((mN-1)/4)
        for m in range(N):
            m += 1
            string = ('t[s]\tU[V]\tI[A]\tPiro[C]\tTC[C]\n-0.01\t-0.01\t-0.01\t'+
            str(round(fileStructure[m*4-1,0],1))+'\t'+str(round(fileStructure[m*4,0],1))+'\n')
    #        if fileName[-1] == '1':
    #            T1 = 1
    #            T2 = 0
    #            subfolder = '1B/'
    #            cikli = -2
    #        elif fileName[-1] == '4':
    #            T1 = 0
    #            T2 = 1
    #            subfolder = '2B/'
    #            cikli = -3
            T1 = 0
            T2 = 1
            subfolder = ''
            cikli = -2
            for line in range(fileStructure.shape[1]):
                if fileStructure[m*4-3,line] > 4:
                    string += str(round(fileStructure[0,line],2)) + '\t'
                    string += str(round(fileStructure[m*4-3,line],2)) + '\t'
                    string += str(round(fileStructure[m*4-2,line],2)) + '\t'
                    string += str(round(fileStructure[m*4-T1,line],1)) + '\t'
                    string += str(round(fileStructure[m*4-T2,line],1)) + '\n'
                    lastLine = line
                    tEnd = fileStructure[0,line]
            while tEnd < 61:
                string += str(round(tEnd,2)) + '\t'
                string += str(round(fileStructure[m*4-3,lastLine],2)) + '\t'
                string += str(round(fileStructure[m*4-2,lastLine],2)) + '\t'
                string += str(round(fileStructure[m*4-T1,lastLine],1)) + '\t'
                string += str(round(fileStructure[m*4-T2,lastLine],1)) + '\n'
                tEnd += 0.01
             
            #file = open(path+trPath+subfolder+fileName+'_'+str(m)+'.txt', 'w')#+'_'+fileName[:cikli]+'.txt', 'w')
            file = open(fileName+'_'+str(m)+'.txt', 'w', encoding="utf-8")
            file.write(string[:-1])
            file.close()
            
    def moveFile(self, filename, path=''):
        move(path+filename, path+'originals/'+filename)
        
        
    def change(self, path, switch=False):
    
        if path[-1] != '/':
            path += '/'
        
        files = listdir(path)
        if not isdir(path+'originals'):
            mkdir(path+'originals')
        tFiles = []    
        for file in files:
            if file[-4:] == '.txt':
                fileName = file
                header  = ''
                try:
                    with open(path+fileName, 'r', encoding="utf-8") as f:
                        header = f.readlines()[0]
                    if 'U[1]' in header:
                        tFiles.append(file)
                        if 'T[1]' in header:
                            structure = self.readFile(path+fileName, switch, True)
                        else:
                            structure = self.readFile(path+fileName, switch)
                        self.saveFiles(structure, path+fileName)
                        self.moveFile(fileName, path)
                except Exception as e:
                    pass
                    #print(e)
        return tFiles
                

        