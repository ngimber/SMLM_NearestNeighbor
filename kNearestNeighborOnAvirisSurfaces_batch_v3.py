import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys
import scipy
from scipy.stats import binned_statistic
from tkinter.filedialog import askopenfilenames
import ntpath
from tkinter import *
from tkinter import IntVar

root = Tk()
PathList = askopenfilenames(filetypes=(("Text files", "*.txt"),
                                           ("CSV", "*.cvs"),
                                           ("All files", "*.*") ))

root.destroy()




master = Tk()
var=StringVar()
val=IntVar()

def setx():

    var.set("x")
    global k    
    k=val.get()
    master.destroy() 
    
def sety():
    var.set("y")
    global k    #
    k=val.get()
    master.destroy() 


Button(master, text='Set x channel and proceed', command=setx).grid(row=3, sticky=W, pady=10)
Button(master, text='Set y channel and proceed', command=sety).grid(row=4, sticky=W, pady=10)

spinbox = Spinbox(master, text='k = ', from_=1, to=100000000000000000000000000000, textvariable = val).grid(row=8, sticky=W, pady=10)
Label(master, text="k =").grid(row=7, sticky=W, pady=10)

mainloop()


    
channel=var.get()

#get rid of error when not changing the value
if(k==0):
    k=1
    
print("OK, will sort ", channel,"Arrays and measure k=", str(k))



 
#open the loop for batch processing
for i in range(0, len(PathList)):
    path = PathList[i]
 
 
    folder, file = ntpath.split(path)
    
    print("folder =", folder)
    print("file =", file)
        

    
    #read txt without first row and left column
    myArray = np.loadtxt(path,delimiter="\t", skiprows=1)# skips row 1 and opens the rest
    print("open matrix without header")
    
    myArray = np.delete(myArray, 0, 1)  
    print("delete left row")
    
    #---------determine matrix size
    numrows = len(myArray)
    numcols = len(myArray[0]) #[0] for cols. otherwise rows
    
    #---------sort Array
    print(myArray)
    
    
    if(channel=="y"):
        print("find minimum for each y")
        myArray=np.sort(myArray, axis=1)
        print("\n")
        print(myArray)
        minimum=myArray[:,0]
        kNearest=myArray[:,(k-1)]
    
    elif(channel=="x"):
        print("find minimum for each x")
        myArray=np.sort(myArray, axis=0)
        print(myArray)
        minimum=myArray[0,:]
        kNearest=myArray[(k-1),:]
        
    print("minimum=",minimum)
    print("kNearest=", kNearest)
    

    np.savetxt(folder+"/k"+str(k)+"_Channel_"+channel+"_"+file+".txt",kNearest,delimiter='\t')

    
    n, bins, patches = plt.hist(kNearest, 100, normed=1, facecolor='g', alpha=0.5)

    
    plt.xlabel('distance (µm?)')
    plt.ylabel('Probability')
    plt.xlim(0,3)
    plt.grid(True)
    plt.savefig(folder+"/k"+str(k)+"_Channel_"+channel+"_"+file+".png")
    plt.show()
    plt.close()
        
    