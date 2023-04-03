# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:23:34 2022

@author: jsantin
"""


from docplex.mp.model import Model
import numpy as np
import random
import matplotlib.pyplot as plt
import copy

#%%
# ----------------------------------------------------------------------------
# Initialize the problem data
# ----------------------------------------------------------------------------
demand = [4400, 4400, 6000, 8000, 6600, 11800, 13000, 11200, 10800, 7600, 6000, 5600]
hiringCost = 1800 #cost to hire one worker
layoffCost = 1200 #cost to layoff one worker
regularCost = 2400 #monthly cost of one worker on regular time
overtimeCost = 3300 #monthly cost of one worker on overtime
holdingCost = 8 #unit cost of holding inventory for one month
outputRate = 480/12 #monthly output (units) per worker
initialInventory = 240
initialWorkers = 160
maxProduction = 13000

TimePeriods = list(range(1,len(demand) + 1))

#%%

def MacPherson(): #naming the function "MacPherson"

# Build model

    myMdl = Model('MacPherson')

#define variables
    P = myMdl.continuous_var_dict(TimePeriods, name = 'P') #units produced
    I = myMdl.continuous_var_dict(TimePeriods, name = 'I') #units held in inventory
    H = myMdl.continuous_var_dict(TimePeriods, name = 'H') #workers hired
    L = myMdl.continuous_var_dict(TimePeriods, name = 'L') #workers laid off
    O = myMdl.continuous_var_dict(TimePeriods, name = 'O') #overtime workers
    R = myMdl.continuous_var_dict(TimePeriods, name = 'R') #regular workers

#define components of objective function
    totalHiring = hiringCost*myMdl.sum(H[t] for t in TimePeriods)
    totalLayoffs = layoffCost*myMdl.sum(L[t] for t in TimePeriods)
    totalHolding = holdingCost*myMdl.sum(I[t] for t in TimePeriods)
    totalRegular = regularCost*myMdl.sum(R[t] for t in TimePeriods)
    totalOvertime = overtimeCost*myMdl.sum(O[t] for t in TimePeriods)

#define objective function equation
    myMdl.minimize(totalHiring + totalLayoffs + totalHolding + totalRegular + totalOvertime)

#add constraints
#worker balance constraint
#month 1
    myMdl.add_constraint(R[1] == initialWorkers + H[1] - L[1])
#months 2-12
    for t in TimePeriods [1:]: #array_name [1:] means element 2 until the end"
        myMdl.add_constraint(R[t] == R[t-1] + H[t] - L[t])

#print(myMdl.export_as_lp_string()) # - expression tells you what you've coded so far


#inventory balance constraint
#month 1
    myMdl.add_constraint(initialInventory + P[1] - I[1] == demand[0])
#months 2-12
    for t in TimePeriods [1:]: #array_name [1:] means element 2 until the end"
        myMdl.add_constraint(I[t-1] + P[t] - I[t] == demand [t-1])
    
#production capacity constraints
    for t in TimePeriods:
            myMdl.add_constraint(P[t] <= maxProduction)
            myMdl.add_constraint(P[t] == outputRate*(R[t] + O[t]))
            myMdl.add_constraint(R[t] >= O[t])

#print(myMdl.export_as_lp_string()) # - expression tells you what you've coded so far
#%%
#solve model

    print(myMdl.export_as_lp_string())
    myMdl.solve()
    print(myMdl.get_solve_status())
    myMdl.solve()
    
    production = (myMdl.solution.get_objective_value())
    print(production)
    
    return production


#%%

#Run 100 scenarios where hiring cost changes
#save values to an array
hiringArray = [] 
originalHC = hiringCost


for iter in range(0,100):
    hiringCost = np.asarray(originalHC)*random.normalvariate(1.0, 0.3)
    hiringArray.append(MacPherson())
    
    print(hiringArray)
    

plt.hist(hiringArray)
plt.show
    






























