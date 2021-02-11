# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 07:40:41 2017

@author: andmra2
"""
from libs import read_data as rd
from math import ceil
import re

def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    float regex comes from https://stackoverflow.com/a/12643073/190597
    '''
    return [atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text)]

def rearrange_up(lis):
    if lis is not None:
        temp = []
        for item in lis:
            temp.append(item.split('.', 1)[0].replace(',', '.'))
        lis = temp
        lis.sort(key=natural_keys)
        return lis
    else:
        print('there')
        return []
    """
    temp=[]
    print(lis)
    for item in lis:
        try:
            temp.append(item.strip('.txt'))
        except:
            temp.append(item.strip('.txt'))
    lis=temp
    print(lis)
    
    intNr = []
    for item in lis:
        nr = 0
        for char in item:
            try:
                char=int(char)
                nr += 1
            except:
                break
        intNr.append(nr)
        
    maxNr = max(intNr)
    chlis = []
    for i,nr in enumerate(intNr):
        if nr == 0 or nr == maxNr:
            chlis.append(lis[i])
        else:
            chlis.append('0'*(maxNr - nr) + lis[i])
        
    temp=[]
    for i in range(len(lis)):
        curr=chlis[0]
        pos=0
        for j in range(len(lis)):
            if chlis[j]<curr:
                curr=chlis[j]
                pos=j
        temp.append(lis[pos])
        del lis[pos]
        del chlis[pos]
    
    for item in temp:
        try:
            lis.append(str(item))
        except:
            lis.append(item)
    return lis
    """
    
def transform_to_write(gdat):
    lis=gdat.data
    l=ceil(gdat.length/10)
    gdat.w_data=[]
    dw=[]
    line=[]
    for k in range(l):
        for j in range(gdat.maxlines):
            for i in range(10):
                try:
                    for h in lis[k*10+i][j]:  #range(len(lis[k*10+i][j])):
                        line.append(h)  #lis[k*10+i][j][h])
                except:
                    pass

            dw.append(line)
            line=[]
        gdat.w_data.append(dw)
        dw=[]
    return gdat
    
def set_parameters(gdat):
    
    gdat.podatki.TC=gdat.nastavitveA.TC
    gdat.podatki.R=gdat.nastavitveA.R
    gdat.podatki.mark=False
    gdat.podatki.MeasDur=60
    gdat.podatki.maxlines=gdat.nastavitveA.maxlines
    gdat.podatki.graph=gdat.nastavitveG.nG
    gdat.podatki.curr=gdat.nastavitveG.IG
    gdat.podatki.setQC = gdat.nastavitveA.QC
    gdat.podatki.QCpath = gdat.nastavitveP.QCpath
    gdat.podatki.readQCs()
    if gdat.nastavitveA.fname == 0:
        gdat.podatki.folder = 'measurements'
        #print(gdat.podatki.path+gdat.podatki.folder)
        gdat.podatki.filenames = rearrange_up(rd.get_data_names(gdat.podatki.path+gdat.podatki.folder))
    else:
        gdat.podatki.folder = gdat.nastavitveA.fname
        gdat.podatki.filenames = rearrange_up(rd.get_data_names(gdat.podatki.folder))
    gdat.podatki.length=len(gdat.podatki.filenames)
    gdat.podatki.get_QC(gdat.podatki.setQC)  

    
    return gdat
    
    
def set_TC_report(gdat):
    gdat.podatki.define_TC_header(order_nr=gdat.nastavitveA.stNarocila, ProductionDate=gdat.nastavitveA.datumProizvodnje, nomVoltage=gdat.nastavitveA.nomV, gp_nr=gdat.nastavitveA.kodaIzdelka, author=gdat.nastavitveA.avtor) #date='5.5.2017'
    gdat.podatki.TCnr = gdat.nastavitveA.oznakaGP
    
    return gdat
            
            