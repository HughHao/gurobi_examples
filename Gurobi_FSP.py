# -*- coding: utf-8 -*-
# @Time : 2023/4/23 17:34
# @Author : hhq
# @File : Gurobi_FSP.py
import gurobipy as gp
from gurobipy import GRB

# Define the problem data
p = [[2, 1, 3], [4, 2, 1], [3, 1, 2]] # processing times
m = len(p[0]) # number of machines
n = len(p) # number of jobs

# Create a new Gurobi model
model = gp.Model("flow_shop")

# Create the decision variables
x = model.addVars(n, m, vtype=GRB.CONTINUOUS, name="x")
s = model.addVars(n, m, vtype=GRB.CONTINUOUS, name="s")

# Set the objective function
model.setObjective(s[n-1,m-1] + p[n-1][m-1], GRB.MINIMIZE)

# Add the constraints
for i in range(n):
    for j in range(m):
        if i == 0 and j == 0:
            model.addConstr(s[i,j] == x[i,j] * p[i][j])
        elif j == 0:
            model.addConstr(s[i,j] == s[i-1,m-1] + x[i,j] * p[i][j])
        else:
            model.addConstr(s[i,j] == s[i,j-1] + x[i,j] * p[i][j])
    model.addConstr(gp.quicksum(x[i,j] for j in range(m)) == 1)

# Optimize the model
model.optimize()

# Print the solution
print("Optimal solution:")
for i in range(n):
    for j in range(m):
        if x[i,j].x > 0.5:
            print("Job", i+1, "is processed on machine", j+1, "starting at time", s[i,j].x)
print("Total processing time:", s[n-1,m-1].x + p[n-1][m-1])
