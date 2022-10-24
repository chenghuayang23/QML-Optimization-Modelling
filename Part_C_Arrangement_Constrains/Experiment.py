# Products Manufacturing with lowest cost
# Gurobi Optimization
#
# Author: Chenghua Yang
# Version 0.0 - flexible arranging 
# 2022-10-11


from gurobipy import *
import pandas as pd

model = Model("ProductsManufactuing")


# ----- parameters -----

# holdingcosts per month per product 
holdingCosts      =  (6, 8, 10)                      # euro/unit

# cost of one worker in each month
workerCosts       =  (2500, 2000, 2500, 2500,        # euro
                      2500, 3000, 3000, 3000, 
                      2500, 2500, 2000, 2000) 

# number of products of each type produced by a worker in a month
prodCapability    =  (15, 20, 10)                    #  unit

# products demond for each type in each month 
demand        =      ((750, 650, 600, 500, 130.3, 650, 600, 750, 650, 600, 500, 550),     # unit
                      (550, 500, 450, 275, 350, 300, 500, 600, 500, 400.6, 300, 250),     
                      (550, 500, 500, 320.5, 300, 150.2, 225, 500, 450, 350, 300, 350))


# ----- sets -----

I = range(len(holdingCosts))     # Set for the product types
K = range(len(workerCosts))      # Set for the months
S = [0, 3, 6, 9]


# ----- Variables -----

# Decision Variable x(i,k) (number of workers producing product i in month k)
x = {} 
for i in I:
    for k in K:
        # Workers only work full time, namely, x_ik must be an integer
        x[i,k] = model.addVar(lb = 0, vtype = GRB.INTEGER, name = 'X[' + str(i) + ',' + str(k) + ']') 
# Integrate new variables
model.update ()

# Auxiliary Variables r(i,k) (remaining products of type i of month k)
r = {} 
for i in I:
    for k in K:
        r[i,k] = model.addVar(lb = 0, vtype = GRB.CONTINUOUS, name = 'R[' + str(i) + ',' + str(k) + ']')

# Integrate new variables
model.update ()


# ---- Objective Function ----

model.setObjective(quicksum((r[i,k] * holdingCosts[i] + workerCosts[k] * x[i,k]) for i in I for k in K))
model.modelSense = GRB.MINIMIZE
model.update()


# ---- Constraints ----

# Constrains 1: production of each type of products must exceed the corresponding demand
con1 = {}
for i in I:
    for k in K:
        if k == 0:
            # The first month dose not have overproduction products from previous month
            con1[i,k] = model.addConstr(r[i,k] == prodCapability[i] * x[i,k] - demand[i][k],\
                                        'con1[' + str(i) + ',' + str(k) + ']-')
        else:
            # The remaining products from previous month are used first to meet the current month need
            con1[i,k] = model.addConstr(r[i,k] == prodCapability[i] * x[i,k] + r[i,k-1] - demand[i][k], \
                                        'con1[' + str(i) + ',' + str(k) + ']-')


# Constrains 2 & 3: Arranging personnel are only allowed 4 times in a year, 
# each at Jannuary, April, July and October
# Constrains 2 & 3 makes sure that worker quantity remains unchanged for each quarter of a year 
con2 = {}
for s in S:
    con2[s] = model.addConstr(quicksum(x[i,s] for i in I) == quicksum(x[i,s+1] for i in I), 'con2[' + str(s) + ']-')
    
con3 = {}
for s in S:
    con2[s] = model.addConstr(quicksum(x[i,s+1] for i in I) == quicksum(x[i,s+2] for i in I), 'con2[' + str(s+1) + ']-')


# ---- Solve ----

model.setParam( 'OutputFlag', True) # silencing gurobi output or not
model.setParam ('MIPGap', 0);       # find the optimal solution
model.write("output.lp")            # print the model in .lp format file

model.optimize()


# --- Print results ---
print('\n--------------------------------------------------------------------\n')
    
if model.status == GRB.Status.OPTIMAL: # If optimal solution is found
    print('Total costs : %10.2f euro' % model.objVal) # Minimum total cost 
    print('Total holding costs: %10.2f euro' % sum(r[i,k].x * holdingCosts[i] for i in I for k in K)) # Minimum total holding cost
    print('Total personnel costs: %10.2f euro' % sum(workerCosts[k] * x[i,k].x for i in I for k in K)) # Minimum total personnel cost
    print ('\n') 

    for i in I:
        print('totoal holding cost for type %d is %10.2f' %  (i, sum(r[i,k].x * holdingCosts[i] for k in K)))

    

else:
    print ('\nNo feasible solution found')

print ('\nREADY\n')
