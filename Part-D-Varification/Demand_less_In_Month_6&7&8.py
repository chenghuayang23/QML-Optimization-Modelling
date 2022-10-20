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
workerCosts       =  (2000, 2000, 2500, 2500,        # euro
                      2500, 3000, 3000, 3000, 
                      2500, 2500, 2000, 2000) 

# number of products of each type produced by a worker in a month
prodCapability    =  (15, 20, 10)                    #  unit

# products demond for each type in each month 
demand        =      ((750, 650, 600, 500, 130.3, 0, 0, 0, 650, 600, 500, 550),     # unit
                      (550, 500, 450, 275, 350, 300, 500, 600, 500, 400.6, 300, 250),     
                      (550, 500, 500, 320.5, 300, 150.2, 225, 500, 450, 350, 300, 350))


# ----- sets -----

I = range(len(holdingCosts))     # Set for the product types
K = range(len(workerCosts))      # Set for the months


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

model.setObjective(quicksum(r[i,k] * holdingCosts[i] + workerCosts[k] * x[i,k] for i in I for k in K) )
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


# Constrains 3: Arranging personnel is only allowed at three quadrature points in a year, 
# namely, Jannuary, April, July and October
# Constrains 3 makes sure that worker quantity remains unchanged for each quarter of a year 
con2 = {}
for k in K:
    # The worker quantities of January, February and March are equal to each other 
    if (0 <= k <= 2): 
        con2[k] = model.addConstr(quicksum(x[i,k] for i in I) == quicksum(x[i, 0] for i in I), 'con2[' + str(k) + ']-')
    # The worker quantities of April, May and June are equal to each other
    if (3 <= k <= 5): 
        con2[k] = model.addConstr(quicksum(x[i,k] for i in I) == quicksum(x[i, 3] for i in I), 'con2[' + str(k) + ']-') 
    # The worker quantities of July, August and September are equal to each other
    if (6 <= k <= 8): 
        con2[k] = model.addConstr(quicksum(x[i,k] for i in I) == quicksum(x[i, 6] for i in I), 'con2[' + str(k) + ']-')
    # The worker quantities of October, November and December are equal to each other
    if (9 <= k <= 11): 
        con2[k] = model.addConstr(quicksum(x[i,k] for i in I) == quicksum(x[i, 9] for i in I), 'con2[' + str(k) + ']-')


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

    #------------worker quantity for each type of products in each month------------#
    workerQuant = []
    for i in I:
        for k in K:
            workerQuant.append(abs(x[i,k].x))
    f_workerQuant = ['%.2f' % member for member in workerQuant]

    # compute worker quantity of each month
    workerQuantSum = []
    for k in K:
        workerQuantSum.append(sum(x[i,k].x for i in I))
    f_workerQuantSum = ['%.2f' % member for member in workerQuantSum]

    # print the result in the table form
    workers =[f_workerQuant[0:12], f_workerQuant[12:24], f_workerQuant[24:36], f_workerQuantSum]
    columnNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Agu","Sept","Oct","Nov","Dec"]
    df = pd.DataFrame(workers, columns = columnNames, index=['1', '2', '3', 'sum'])
    print('--------------------------worker quantity per month per type---------------------------')
    print(df)
    print('\n')

    #-----------Porducts per type per month produced------------#
    productQuant = []
    for i in I:
        for k in K:
            productQuant.append(abs(x[i,k].x * prodCapability[i]))
    f_productQuant = ['%.2f' % member for member in productQuant]

    # print the result in the table form
    products =[f_productQuant[0:12], f_productQuant[12:24], f_productQuant[24:36]]
    df = pd.DataFrame(products, columns = columnNames, index=['1', '2', '3'])
    print('-----------------------------product quantity per month per type------------------------------')
    print(df)

else:
    print ('\nNo feasible solution found')

print ('\nREADY\n')
