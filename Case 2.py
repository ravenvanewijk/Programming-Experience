# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 20:53:51 2019

@author: Raven
"""

from time import gmtime, strftime, sleep
import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np
import ctypes

"""
This script contains 4 functions. The last function is a fully automized function which pings the website and processes the data.
In total this script uses 6 modules, of which 4 are built-in and 2 have to be downloaded manually (matplotlib.pyplot and numpy).
Programmed in Python 3.7.3
"""

def pingserver():
    """
    First of 4 functions, which pings the KLM webpage.
    Subprocess Popen is a built-in function of Python which pings the given URL 4 times.
    To reduce the probability of outliers, I chose to take the mean of these 4 ping times.
    So, this function outputs the average of the 4 ping responses in ms.
    
    P.S.
    This function might actually looks a bit weird because of all the string manupulations. 
    The cmd.communicate() function outputs datatype "bytes", which had to be converted to datatype "int"
    """
    cmd             = subprocess.Popen(["ping.exe","www.KLM.com"], stdout = subprocess.PIPE)
    output          = cmd.communicate()[0]
    asciioutput     = output.decode('ascii')
    asciioutput     = asciioutput.split("Average =")[-1]
    average         = re.findall("\d",asciioutput)
    mergedaverage   = ''.join(average)
    ping            = int(mergedaverage)
    
    return ping

def sample(sampleamount):
    """
    This function uses the first function to get a dataset of several pingtimes.
    The input is the amount of samples required.
    The while loop stops if the length of the list containing the samples gets bigger than the required amount of samples.
    WHen this happens, the function outputs this list.
    """
    storedsamples   = []
    while len(storedsamples)+1<=sampleamount:
        sample      =pingserver()
        storedsamples.append(sample)

    return storedsamples

def plot(storedsamples):
    """
    This function is made to process the data in the dataset (so, the output of previous function).
    First, two new lists are introduced. 
    One containing the discretisized  samples, and an other containing the number of occurences for each value.
    The dataset is discretisized using the standard deviation of the dataset, to make the results clearer.
    The function requires a raw dataset as input. 
    It returns the processed and discretisezed dataset, and the count of the occurences.
    """
    discrete= []
    x       = []
    storedsamples.sort()
    integerscaling = np.sqrt(np.std(storedsamples))
    for value in storedsamples:
        intvalue   = int(value/integerscaling)*integerscaling
        discrete.append(intvalue)
        discrete.sort()
        x=[]
        for intvalue in discrete:
            xtab = discrete.count(intvalue)
            x.append(xtab)
    return discrete, x   
    
def multiplesamples(numberofbatches,interval,sampleamount, maxping):  
    """
    This last function uses the previous three functions.
    The function is completely automised, amd only requires 4 variable inputs (which are up to the user to decide):
    
        - These are the number of batches (so the number of datasets it will process), 
        - The time interval in which this batches are acquired,
        - The amount of samples in each batch
        - Maximum desired ping time
    
    The function uses a loop to obtain the batches, and (sub)plots the results in rows (so each graph is a seperate batch).
    It also displays the mean and standard deviation of each batch.
    After each obtained batch, it waits the interval which was gives as input.
    It does so until the amount of batches reached the desired number, and then shows the plots for each batch.
    It also gives a popup message if the mean of one or more batches exceeds the maximum desired ping time.  
    """
    i            = 0
    storedsamples= {}
    discrete     = {}
    x            = {}
    fig,ax       = plt.subplots(nrows=numberofbatches,ncols=1)

    while i+1<=numberofbatches:
        
        sample(sampleamount)
        storedsamples[i] = sample(sampleamount)
        discrete[i], x[i]= plot(storedsamples[i])
        ax[i].bar(discrete[i],x[i],np.std(discrete[i])/len(x[i]))
        plt.tight_layout()
        counter          = str(i+1)
        ax[i].set_title("Batch number "+ counter+ ' Sample obtained at: '+ strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        means            = []
        means.append(round(sum(discrete[i])/len(discrete[i]),1))
        mean             = str(round(sum(discrete[i])/len(discrete[i]),1))
        stdev            = str(round(np.std(discrete[i]),1))

        ax[i].set_xlabel("Ping time [ms] \nThe mean is: "+ mean+ " [ms], and the stdev is: "+stdev+" [ms]")
        ax[i].set_ylabel("Number of occurrences")
        i               += 1
        
        
        print("Batch number "+str(i)+" completed")
        sleep(interval)

    
    if max(means)>=maxping:
        ctypes.windll.user32.MessageBoxW(0, "The maximum ping time has been exceeded", "Popup", 1)


