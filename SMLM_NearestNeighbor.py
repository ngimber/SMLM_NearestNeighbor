
################################


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os
import math
import scipy.spatial
plt.style.use(['seaborn-white', 'seaborn-deep'])
import csv
from tkinter.filedialog import askopenfilenames
from tkinter import *
from tkinter import IntVar
import tkinter as tk
from os import path





###############get Files
root = Tk()

PathList = askopenfilenames(filetypes=(
("ThunderSTORM file", "*csv"),
("All files", "*.*") 
))

root.destroy()


files=[]
for thisfile in PathList:
    folder, file = path.split(thisfile)
    files=files+[file]
    
path=folder+"/"



###############get Parameters








def getParameters():

    
    def saveParameters():
        
        
    
        global k
        global shift
        global subset
        global packagesize
        global subjectIdentifyer
        global referenceIdentifyer

        k=e1.get()
        shift=e2.get() 
        subset= e3.get()
        packagesize=e4.get() #poionts to process simultaneously (dependent on RAM size)
        subjectIdentifyer=e5.get()
        referenceIdentifyer=e6.get()
        
        master.destroy()

        
    
    master = Tk()
    master.title("tesseler for ThunderSTORM")
    Label(master, text="k           ").grid(row=0, column=0,sticky=W)
    Label(master, text="Toroidal Shift [units]").grid(row=1, column=0,sticky=W)
    Label(master, text="Subset (reduces computational time by processing only a subset of 'subjects'', 0 = whole dataset)").grid(row=2, column=0,sticky=W)
    Label(master, text="Block size (Dataset ist processed blockwise, reducing this value saves memory) ").grid(row=3, column=0,sticky=W)
    Label(master, text="File identifyer subject").grid(row=4, column=0,sticky=W)
    Label(master, text="File identifyer reference").grid(row=5, column=0,sticky=W)
    Label(master, text="niclas.gimber@charite.de ").grid(row=7, column=1,columnspan=1000)
    
    v = IntVar()
    v.set(1)
    e1 = Entry(master, text=v)
    e1.grid(row=0, column=2)
    
    v2 = IntVar()
    v2.set(10)
    e2 = Entry(master, text=v2)
    e2.grid(row=1, column=2)
    
    v3 = IntVar()
    v3.set(5000)
    e3 = Entry(master, text=v3)
    e3.grid(row=2, column=2)
   
    v4 = IntVar()
    v4.set(500)
    e4 = Entry(master, text=v4)
    e4.grid(row=3, column=2)
    
    v5 = StringVar()
    v5.set("ch1")
    e5 = Entry(master, text=v5)
    e5.grid(row=4, column=2)
    
    v6 = StringVar()
    v6.set("ch2")
    e6 = Entry(master, text=v6)
    e6.grid(row=5, column=2)
    
    Label(master, text=" ").grid(row=7, column=0,sticky=W)
    Button(master, text='Go',fg="green",bg="gray83", command=saveParameters).grid(row=8, column=2)
    #master.attributes("-fullscreen", True)
    master.attributes("-topmost", True)

    
    mainloop()
 
getParameters()
k=int(k)
shift=float(shift)
subset= int(subset)
packagesize=int(packagesize)
subjectIdentifyer=str(subjectIdentifyer)
referenceIdentifyer=str(referenceIdentifyer)


#################################


newPath=path+"kNN_"+str(k)+"\\"
if (os.path.exists(newPath)==False):
    os.makedirs(newPath)    
    

###############################################################

def kNN(a,b,k):# a=subject,b=reference, k=k
    kNNs=[]    
    for j in range(1,math.floor(len(a)/packagesize)):
        matrix=scipy.spatial.distance_matrix(a[(j-1)*packagesize:j*packagesize],b)
        # circumvent the problem of k0 = zero in cale of identivcal reference and subject
        matrix=np.where(matrix == 0,np.nan,matrix) 
        matrix=np.where(matrix == shift,np.nan,matrix)
        matrix=np.sort(matrix,axis=1)
        kNNs+=matrix[:,k].tolist()

    return kNNs
 
 
for i in range(0,len(files)): # main loop

    
    
    subjectTable=pd.read_csv(path+files[i])
    referenceTable=pd.read_csv(path+files[i][0:files[i].find(subjectIdentifyer)]+referenceIdentifyer+".csv")
    

    ################################
    #auto NN


    a=subjectTable[["x [nm]","y [nm]"]].values
    b=subjectTable[["x [nm]","y [nm]"]].values


    if(subset>0):
        if(subset<len(a)):
            if(subset>packagesize):
                print(files[i]+": generate subset")
                np.random.shuffle(a)
                a=a[:subset]
                print("subset calculated")

    print("start NN")
    kNNs=kNN(a,b,k)
    shifted=np.where((a+shift) < a.max(), a+shift, a+shift-a.max())
    kNNsRandom=kNN(shifted,b,k)
    fig=plt.figure()
    plt.hist(np.array(kNNs)[np.array(kNNs)<np.median(kNNs)*10],bins=41,alpha=0.5,range=[0,3*np.median(kNNs)])
    plt.hist(np.array(kNNsRandom)[np.array(kNNsRandom)<np.median(kNNs)*10],bins=41,alpha=0.5,range=[0,3*np.median(kNNs)])
    plt.title("k = "+str(k)+" Subject: "+subjectIdentifyer+" Reference: "+subjectIdentifyer)
    plt.xlabel("NN distance [nm]")
    plt.ylabel("Counts")
    plt.savefig(newPath+files[i]+"_S-"+subjectIdentifyer+"_R-"+subjectIdentifyer+".png")


    saveMe=pd.DataFrame([a[:,0],a[:,1],kNNs,kNNsRandom]).T
    saveMe.columns=["x [nm]","y [nm]","kNN k="+str(k),"toroidal shift "+str(shift)]
    saveMe.to_csv(newPath+files[i]+"_S-"+subjectIdentifyer+"_R-"+subjectIdentifyer+".csv")
    
    
    
    
# and nov inverse   

    a=referenceTable[["x [nm]","y [nm]"]].values
    b=referenceTable[["x [nm]","y [nm]"]].values


    if(subset>0):
        if(subset<len(a)):
            if(subset>packagesize):
                print(files[i]+": generate subset")
                np.random.shuffle(a)
                a=a[:subset]
                print("subset calculated")

    print("start NN")
    kNNs=kNN(a,b,k)
    shifted=np.where((a+shift) < a.max(), a+shift, a+shift-a.max())
    kNNsRandom=kNN(shifted,b,k)
    fig=plt.figure()
    plt.hist(np.array(kNNs)[np.array(kNNs)<np.median(kNNs)*10],bins=41,alpha=0.5)
    plt.hist(np.array(kNNsRandom)[np.array(kNNsRandom)<np.median(kNNs)*10],bins=41,alpha=0.5)
    plt.title("k = "+str(k)+" Subject: "+referenceIdentifyer+" Reference: "+referenceIdentifyer)
    plt.xlabel("NN distance [nm]")
    plt.ylabel("Counts")
    plt.savefig(newPath+files[i]+"_S-"+referenceIdentifyer+"_R-"+referenceIdentifyer+".png")


    saveMe=pd.DataFrame([a[:,0],a[:,1],kNNs,kNNsRandom]).T
    saveMe.columns=["x [nm]","y [nm]","kNN k="+str(k),"toroidal shift "+str(shift)]
    saveMe.to_csv(newPath+files[i]+"_S-"+referenceIdentifyer+"_R-"+referenceIdentifyer+".csv")
    
    
    
    ################################
    #calc NN between channels 
    

    a=subjectTable[["x [nm]","y [nm]"]].values
    b=referenceTable[["x [nm]","y [nm]"]].values


    if(subset>0):
        if(subset<len(a)):
            if(subset>packagesize):
                print(files[i]+": generate subset")
                np.random.shuffle(a)
                a=a[:subset]
                print("subset calculated")

    print("start NN")
    kNNs=kNN(a,b,k)
    shifted=np.where((a+shift) < a.max(), a+shift, a+shift-a.max())
    kNNsRandom=kNN(shifted,b,k)
    fig=plt.figure()
    plt.hist(np.array(kNNs)[np.array(kNNs)<np.median(kNNs)*10],bins=41,alpha=0.5)
    plt.hist(np.array(kNNsRandom)[np.array(kNNsRandom)<np.median(kNNs)*10],bins=41,alpha=0.5)
    plt.title("k = "+str(k)+" Subject: "+subjectIdentifyer+" Reference: "+referenceIdentifyer)
    plt.xlabel("NN distance [nm]")
    plt.ylabel("Counts")
    plt.savefig(newPath+files[i]+"_S-"+subjectIdentifyer+"_R-"+referenceIdentifyer+".png")

    saveMe=pd.DataFrame([a[:,0],a[:,1],kNNs,kNNsRandom]).T
    saveMe.columns=["x [nm]","y [nm]","kNN k="+str(k),"toroidal shift "+str(shift)]
    saveMe.to_csv(newPath+files[i]+"_S-"+subjectIdentifyer+"_R-"+referenceIdentifyer+".csv")
    
    
    
    
    
# the same inverse   

    b=subjectTable[["x [nm]","y [nm]"]].values
    a=referenceTable[["x [nm]","y [nm]"]].values


    if(subset>0):
        if(subset<len(a)):
            if(subset>packagesize):
                print(files[i]+": generate subset")
                np.random.shuffle(a)
                a=a[:subset]
                print("subset calculated")

    print("start NN")
    kNNs=kNN(a,b,k)
    shifted=np.where((a+shift) < a.max(), a+shift, a+shift-a.max())
    kNNsRandom=kNN(shifted,b,k)
    fig=plt.figure()
    plt.hist(np.array(kNNs)[np.array(kNNs)<np.median(kNNs)*10],bins=41,alpha=0.5)
    plt.hist(np.array(kNNsRandom)[np.array(kNNsRandom)<np.median(kNNs)*10],bins=41,alpha=0.5)
    plt.title("k = "+str(k)+" Subject: "+referenceIdentifyer+" Reference: "+subjectIdentifyer)
    plt.xlabel("NN distance [nm]")
    plt.ylabel("Counts")
    plt.savefig(newPath+files[i]+"_S-"+referenceIdentifyer+"_R-"+subjectIdentifyer+".png")

    saveMe=pd.DataFrame([a[:,0],a[:,1],kNNs,kNNsRandom]).T
    saveMe.columns=["x [nm]","y [nm]","kNN k="+str(k),"toroidal shift "+str(shift)]
    saveMe.to_csv(newPath+files[i]+"_S-"+referenceIdentifyer+"_R-"+subjectIdentifyer+".csv")
    
    
    