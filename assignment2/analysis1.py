# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 11:17:51 2019

@author: Gebruiker
"""

import csv
import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np

class Properties():
    
    def __init__(self):
        
        self.T = 1
        self.sigma = 0.2
        self.r = 0.06
        self.s0 = 100
        self.K = 99
        self.N = 365
        self.dt = self.T/self.N
        self.M = 10000
        

def ST(props):
    return props.s0 * math.exp((props.r-0.5*props.sigma**2)*props.T+props.sigma*props.T**0.5*np.random.normal())

def option_price(props):
    
    thesum = 0
    
    for i in range(props.M):
        thesum += max(ST(props)-props.K,0)
        
    average = thesum / props.M
    price = math.exp(-props.r*props.T) * average
    return(price)

def option_price_put(props):
    
    thesum = 0
    
    for i in range(props.M):
        thesum += max(props.K-ST(props),0)
        
    average = thesum / props.M
    price = math.exp(-props.r*props.T) * average
    return(price)


def save_values(data):
    
    filename = 'part1data/putprices.csv'
    
    with open(filename, 'a', newline = '') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            
            writer.writerow(data)

props = Properties()

def read_data_convergence(M,N):
    print('uhm')
    thesum = 0
    prices = []

    with open("part1data/putvaluesonceagain.csv", "r") as csvfile:

        reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        counter = 0
        morecounter=0
        print(M)

        # For each reflection with this mua, it is checked if it is in
        # right range for r
        for row in reader:
            counter+= 1
            morecounter+=1
            thesum += row[0]
            
            if counter == M:
                print(morecounter)
                average = thesum / M
                price = math.exp(-props.r*props.T) * average
                prices.append(price)
                thesum = 0
                counter = 0
                if len(prices)==N:
                    print("lack of progress")
                    break

    save_values(prices)
        
def mean_error(thelist):
    
    average = 0
    
    for i in thelist:
        average += i
    
    average = average / len(thelist)
    
    standard = 0
    
    for i in thelist:
        standard += (i-average)**2
        
    standard = (standard/len(thelist)) ** 0.5
    
    return average, standard

def read_data_plot():
    
    prices = []

    with open("part1data/putprices.csv", "r") as csvfile:

        reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        print("someething")
        # For each reflection with this mua, it is checked if it is in
        # right range for r
        for row in reader:
            while '' in row:
                row.remove('')
            prices.append(row)
            
    print(mean_error(prices[-1]))
    
    return prices

def make_the_plots():
    label1 = ["M=1000","M=10000", "M=100000"]
    label2 = ["number of V=100","number of V=1000", "number of V=10000"]
        
    theprice = read_data_plot()
    #print(theprice)
    for i in range(9):
        if i%3==0:
            
            plt.legend()
            plt.show()
            plt.figure()
            plt.title("Distribution of option prices depending on M")
            plt.xlabel("option price")
        #sns.set()
            #plt.xlim(3.5,6)
        sns.distplot(theprice[i], label=label1[i%3])
        
    plt.legend()
    plt.show()
    for i in range(3):
        plt.figure()
        plt.title("Distribution of option prices depending on number of V")
        plt.xlabel("option price")
        #plt.xlim(3.5,6)
        temp = [i,i+3,i+6]
        for j in range(len(temp)):
            sns.distplot(theprice[temp[j]], label=label2[j])
        
        plt.legend()
        plt.show()
            
        
def read_varied_data(filename):
    
    means = []
    errors = []

    with open(filename, "r") as csvfile:

        reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        
        for row in reader:
            mean,error = mean_error(row)
            means.append(mean)
            errors.append(error)
    
    return means, errors
        
def make_varied_plots(xs,filename):
    
    ys,yerror = read_varied_data(filename)
    
    plt.figure()
    plt.plot(xs,ys,'c-')
    plt.errorbar(xs,ys, yerr=yerror,color='c')
    plt.xlabel("strike price")
    plt.ylabel("option price")
    plt.title("Option price as a function of strike price")
    plt.show()

def make_prices():
    
    for i in [100,1000,10000]:
        for j in [1000,10000,100000]:
            
            read_data_convergence(j,i)
            
make_the_plots()
make_varied_plots([i for i in np.arange(0,21,1)],"part1data/putvolashigh.csv")
make_varied_plots([i for i in np.arange(0.0,2.01,0.1)],"part1data/putvolas.csv")
make_varied_plots([i for i in range(90,111)],"part1data/putvaluesstrikeput.csv")
make_varied_plots([i for i in range(0,301,20)],"part1data/putstrikeshigh.csv")