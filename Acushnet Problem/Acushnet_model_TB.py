# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 14:47:34 2022

Acushnet 

@author: tbayley
"""

from docplex.mp.model import Model
import numpy as np
import random
import matplotlib.pyplot as plt

#%%
# ----------------------------------------------------------------------------
# Initialize the problem data
# ----------------------------------------------------------------------------
returnOnCapital = 0.13/12 #monthly rate
dutyRate = [0.19, 0.13, 0.05, 0.185]
palletValue = [9600, 35280, 105600, 37800]
storageCostPerCarton = [0.36, 0.22, 0.44, 0.32]
cartonsPerPallet = [20, 15, 48, 15]

maxStorage = [[350, 330, 140, 60, 0, 80, 140, 200, 220, 220, 230, 240],
              [70, 100, 20, 0, 0, 50, 70, 90, 100, 110, 115, 100],
              [18, 16, 10, 8, 5, 3, 5, 15, 25, 30, 30, 30],
              [12, 10, 8, 8, 6, 3, 3, 30, 70, 70, 80, 80]]

warehouseCapacity = 200
totalTimePeriods = 12
TimePeriods = list(range(1,totalTimePeriods + 1))


#%%
# ----------------------------------------------------------------------------
# Build the model
# ----------------------------------------------------------------------------
# We are building a function that will return the objective function value at optimality 

def solveAcushnet(): #naming the function "solveAcushnet"
    myMdl = Model('Acushnet') #give the model a name
    
    #define the variables and add them to the model
    shoes = myMdl.integer_var_dict(TimePeriods, name = "S")
    gloves = myMdl.integer_var_dict(TimePeriods, name = "G")
    clubs = myMdl.integer_var_dict(TimePeriods, name = "C")
    outerwear = myMdl.integer_var_dict(TimePeriods, name = "O")
    
    #define expressions to calculate total cash savings and storage cost
    totalReturn = returnOnCapital * (dutyRate[0]*palletValue[0]*myMdl.sum(shoes[t] for t in TimePeriods)
                                    +dutyRate[1]*palletValue[1]*myMdl.sum(gloves[t] for t in TimePeriods)
                                    +dutyRate[2]*palletValue[2]*myMdl.sum(clubs[t] for t in TimePeriods)
                                    +dutyRate[3]*palletValue[3]*myMdl.sum(outerwear[t] for t in TimePeriods))
    
    totalStorageCost = (storageCostPerCarton[0] * cartonsPerPallet[0]*myMdl.sum(shoes[t] for t in TimePeriods) 
                        + storageCostPerCarton[1] * cartonsPerPallet[1]*myMdl.sum(gloves[t] for t in TimePeriods)
                        + storageCostPerCarton[2] * cartonsPerPallet[2]*myMdl.sum(clubs[t] for t in TimePeriods)
                        + storageCostPerCarton[3] * cartonsPerPallet[3]*myMdl.sum(outerwear[t] for t in TimePeriods))
    
    #define the objective function equation
    myMdl.maximize(totalReturn - totalStorageCost)
    
    
    #define constraints
    #capacity constraints
    for t in TimePeriods:
        myMdl.add_constraint(shoes[t] + gloves[t] + clubs [t] + outerwear[t] <= warehouseCapacity)
    
    
    for t in TimePeriods:
        myMdl.add_constraint(shoes[t] <= maxStorage[0][t-1])
        myMdl.add_constraint(gloves[t] <= maxStorage[1][t-1])
        myMdl.add_constraint(clubs[t] <= maxStorage[2][t-1])
        myMdl.add_constraint(outerwear[t] <= maxStorage[3][t-1])
    
    #generate the formulation of your model using your variable naming convention
    #print(myMdl.export_as_lp_string())
    
    #solve the model
    myMdl.solve() # it won't print anything, it just solves the model.
    
    netRevenue = myMdl.solution.get_objective_value()
    print(netRevenue)
    #return netRevenue


#%%
# ----------------------------------------------------------------------------
# Sensitivity
# ----------------------------------------------------------------------------
#Let's run several scenarios where we change the maxStorage
#Define a function that solves the LP and returns the netRevenue

#copy the original maxStorage values and we'll use it to manipulate the RHS
originalMaxStorage = maxStorage
maxStorage= np.asarray(originalMaxStorage)*0.9

#solveAcushnet()

#Let's run 100 scenarios where maxStorage changes
#save values to an array
revenueArray = []

for iter in range(0,100):
    maxStorage = np.asarray(originalMaxStorage)*random.normalvariate(1.0, 0.2)
    #maxStorage = np.asarray(originalMaxStorage)*random.uniform(0.9, 1.1)
    revenueArray.append(solveAcushnet())

#Find some basic statistics
print ("Average = ", np.mean(revenueArray))
print("SD = ", np.std(revenueArray))

plt.hist(revenueArray)
plt.show
