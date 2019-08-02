# -*- coding: utf-8 -*-
"""
Created on Mon May 14 14:42:22 2018

@author: Raven
"""
import os

def idxabc(ch):
    #return index in alphabet 0-25
    i = ord(ch.upper())-ord("A")
    return i

def shiftch(ch,ikey):
    #ch= character to change
    #ikey= number of places to shift up
    
    #upper case alphabetic character
    if 65<=ord(ch)<=90:
        i=(ord(ch)-ord("A")+ikey)%26+ord("A")
        newch=chr(i)
    
    #lower case alphabetic character
    elif 97<=ord(ch)<=122:
        i=(ord(ch)-ord("a")+ikey)%26+ord("a")
        newch=chr(i)
        
    #others
    else:
        newch=ch
        
    return newch

def shiftlines(lines,ikey):
    #do caesar shift on a list of lines
    newlines= []
    for line in lines:
        newline= ""
        for ch in line:
            ch = shiftch(ch,ikey)
            newline = newline+ch
        newlines.append(newline)
    return newlines

def getfreq(lines):
    #get list with frequencies for A to Z
    lines=str(lines)
    totals=26*[0]
    for ch in lines:
        if (ord("A")<=ord(ch)<=ord("Z")) or (ord("a")<=ord(ch)<=ord("z")):
            totals[idxabc(ch)] = totals[idxabc(ch)] +1
        else:
            totals=totals
    # %-calculations
    freqlist=[]
    grandtotal= sum(totals)
    for total in totals:
        freq=(total/grandtotal)*100
        freqlist.append(freq)
    return freqlist

def listdif(a,b):
    # find sum of absolute value of pairwise
    #differences of the elements of the lists
    total=0.0
    i=0
    while i<len(a):
        total=total+abs(a[i]-b[i])
        i=i+1
    return total

def idxmin(lst):
    #find lowest value in a list
    #lst - list with values
    #Returns the index of the lowest value, in case of two elements having this lowest value, returns the first.
    idx=lst.index(min(lst))
    
    return idx

#opening files and getting freqs
    
#empty list
lst= 26*[0.0]
f=open("ch-freq-en.txt","r")
lines= f.readlines()
for line in lines:
    
    ch=line[0]
    line=line[1:]
    #append lst
    lst[idxabc(ch)]= float(line.strip())+ lst[idxabc(ch)]
    
#print(lst) #alphabetic order freq
f.close()   

for ifile in range(1,7):
    
    filename= "secret{:d}.txt".format(ifile)
    resultfilename= "decoded{:d}.txt".format(ifile)
    o=open("secret{:d}.txt".format(ifile),"r")
    
    reading=o.readlines()
    
    keydif=[]
    key=0
    while 0<=key<=26:
        x=shiftlines(reading,key)
        y=getfreq(x)
        p=listdif(lst,y)
        keydif.append(p)
        key=key+1
    ikey=idxmin(keydif)
        
    print(filename,ikey)
    
    h=open("decoded{:d}.txt".format(ifile),"w")
    h.writelines(shiftlines(reading,ikey))
    h.close()
    
    o.close()
    


















