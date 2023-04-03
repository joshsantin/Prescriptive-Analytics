# -*- coding: utf-8 -*-
"""
Choosing Neighbourhood Community Projects - TEMPLATE

Created on Mon Oct 17 20:47:02 2022

@author: joshsantin
"""

from docplex.mp.model import Model
import pandas as pd

#%%
# ----------------------------------------------------------------------------
# Initialize the problem data
# ----------------------------------------------------------------------------
#Be sure to save this program file in the same directory as the data file

#Read the data
allData = pd.read_excel('CommunityProjectsData.xlsx', sheet_name='Exhibit 1')
print(allData.head()) #prints the first 5 rows of the dataframe

#separate the data by neighbourhood
uptownData = allData[allData["Neighbourhood"] == "Uptown"]
uptownData = uptownData.reset_index(drop = True) #resets the index so that it starts at 0; not needed here but included for clarity
#print(uptownData.to_string())  #will display all of the data
#print(uptownData) #will display some, but not all, of the data

''' Do the same for East, West, and Downtown data'''
eastData = allData[allData["Neighbourhood"] == "East"]
eastData = eastData.reset_index(drop = True)

westData = allData[allData["Neighbourhood"] == "West"]
westData = westData.reset_index(drop = True)

downtownData = allData[allData["Neighbourhood"] == "Downtown"]
downtownData = downtownData.reset_index(drop = True)


#Set up model parameters
#Number of projects in each district
numUptownProjects = len(uptownData)
''' complete the code below '''
numEastProjects = len(eastData) 
numWestProjects = len(westData)
numDowntownProjects = len(downtownData)



#set up indices
uptownProjects = list(range(1,numUptownProjects + 1))
eastProjects = list(range(1,numEastProjects+1))
westProjects = list(range(1,numWestProjects+1))
downtownProjects = list(range(1,numDowntownProjects+1))

budgetPerNeighbourhood = 75000



#%%
# ----------------------------------------------------------------------------
# Build the model
# ----------------------------------------------------------------------------
myMdl = Model('Community')

#define the variables
uptownVar = myMdl.binary_var_dict(uptownProjects, name = 'U')
''' complete the code below '''
eastVar = myMdl.binary_var_dict(eastProjects, name = 'E')
westVar = myMdl.binary_var_dict(westProjects, name = 'W')
downtownVar = myMdl.binary_var_dict(downtownProjects, name = 'D')


#develop parts of the objective function equation
#for each neighbourhood, multiply the number of votes by the binary variable
uptownSatisfiedVotes = myMdl.sum(uptownData["# of Votes"].iloc[i-1]*uptownVar[i] for i in uptownProjects)
''' complete the code below '''
eastSatisfiedVotes = myMdl.sum(eastData["# of Votes"].iloc[i-1]*eastVar[i] for i in eastProjects)
westSatisfiedVotes = myMdl.sum(westData["# of Votes"].iloc[i-1]*westVar[i] for i in westProjects)
downtownSatisfiedVotes = myMdl.sum(downtownData["# of Votes"].iloc[i-1]*downtownVar[i] for i in downtownProjects)



''' complete the code below '''
#define objective function equation
myMdl.maximize(uptownSatisfiedVotes + eastSatisfiedVotes + westSatisfiedVotes + downtownSatisfiedVotes)

#%%
#define constraints
#budget constraint for each district
myMdl.add_constraint(myMdl.sum(uptownData["Cost"].iloc[i-1]*uptownVar[i] for i in uptownProjects) <= budgetPerNeighbourhood)
''' complete the code below '''
myMdl.add_constraint(myMdl.sum(eastData["Cost"].iloc[i-1]*eastVar[i] for i in eastProjects) <= budgetPerNeighbourhood)
myMdl.add_constraint(myMdl.sum(westData["Cost"].iloc[i-1]*westVar[i] for i in westProjects) <= budgetPerNeighbourhood)
myMdl.add_constraint(myMdl.sum(downtownData["Cost"].iloc[i-1]*downtownVar[i] for i in downtownProjects) <= budgetPerNeighbourhood)

#%%
# ----------------------------------------------------------------------------
# Format results
# ----------------------------------------------------------------------------
#store solution in dataframe by neighbourhood
'''
solution_U = myMdl.solution.get_value_df(uptownVar)
solution_E = myMdl.solution.get_value_df(eastVar)
solution_W = myMdl.solution.get_value_df(westVar)
solution_D = myMdl.solution.get_value_df(downtownVar)

#Total spent in each neighbourhood
uptownCost = (solution_U["value"]*uptownData["Cost"]).sum()
eastCost = (solution_E["value"]*eastData["Cost"]).sum()
westCost = (solution_W["value"]*westData["Cost"]).sum()
downtownCost = (solution_D["value"]*downtownData["Cost"]).sum()

#concatenate solution with data
newUptownData = pd.concat([solution_U,uptownData], axis=1)
newEastData = pd.concat([solution_E,eastData], axis=1)
newWestData = pd.concat([solution_W,westData], axis=1)
newDowntownData = pd.concat([solution_D,downtownData], axis=1)

#print only chosen projects
print("\n Total Cost of Projects in Uptown = ", uptownCost)
print(newUptownData[newUptownData["value"]==1].to_string())

print("\n Total Cost of Projects in East = ", eastCost)
print(newEastData[newEastData["value"]==1].to_string())

print("\n Total Cost of Projects in West = ", westCost)
print(newWestData[newWestData["value"]==1].to_string())

print("\n Total Cost of Projects in Downtown = ", downtownCost)
print(newDowntownData[newDowntownData["value"]==1].to_string())
'''

#%% #Add constraints#
#%% #For every park project you select for Downtown, you must select at least two park projects in each of the other 3 districts#

downtownParkProject = (downtownData["Primary Type"] == "Park") | (downtownData["Secondary Type"] == "Park")
uptownParkProject = (uptownData["Primary Type"] == "Park") | (uptownData["Secondary Type"] == "Park")
eastParkProject = (eastData["Primary Type"] == "Park") | (eastData["Secondary Type"] == "Park")
westParkProject = (westData["Primary Type"] == "Park") | (westData["Secondary Type"] == "Park")

myMdl.add_constraint(myMdl.sum(uptownParkProject.iloc[i-1].astype(int)*uptownVar[i] for i in uptownProjects) >= 2*myMdl.sum(downtownParkProject.iloc[i-1].astype(int)*downtownVar[i] for i in downtownProjects)) 
myMdl.add_constraint(myMdl.sum(eastParkProject.iloc[i-1].astype(int)*eastVar[i] for i in eastProjects) >= 2*myMdl.sum(downtownParkProject.iloc[i-1].astype(int)*downtownVar[i] for i in downtownProjects)) 
myMdl.add_constraint(myMdl.sum(westParkProject.iloc[i-1].astype(int)*westVar[i] for i in westProjects) >= 2*myMdl.sum(downtownParkProject.iloc[i-1].astype(int)*downtownVar[i] for i in downtownProjects)) 

myMdl.solve()
myMdl.print_solution()
print(myMdl.export_as_lp_string())
