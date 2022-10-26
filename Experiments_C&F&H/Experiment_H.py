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
demand        =      ((750, 650, 600, 500, 130.3, 650, 600, 750, 650, 600, 500, 550),     # unit
                      (550, 500, 450, 275, 350, 300, 500, 600, 500, 400.6, 300, 250),     
                      (550, 500, 500, 320.5, 300, 150.2, 225, 500, 450, 350, 300, 350))

firingCost = 2000     # euro
trainingCost = 5000   # euro

contractPeriods = 12   # month

# ----- sets -----

I = range(len(holdingCosts))     # Set for the product types
K = range(len(workerCosts))      # Set for the months


# ----- Variables -----

# x[i,k] is the number of workers producing product i at the beginning of month k
x = {} 
for i in I:
    for k in K:
        # Workers only work full time, so x_ik must be an integer
        x[i,k] = model.addVar(lb = 0, vtype = GRB.INTEGER, name = 'X[' + str(i) + ',' + str(k) + ']') 
# Integrate new variables
model.update ()

# r[i,k] is the remaining products of type i of at the end of month k
r = {} 
for i in I:
    for k in K:
        r[i,k] = model.addVar(lb = 0, vtype = GRB.CONTINUOUS, name = 'R[' + str(i) + ',' + str(k) + ']')
# Integrate new variables
model.update ()

# n[i,k] is the number of workers newly hired producing type i at the beginning of month k
n = {}
for i in I:
    for k in K:
        n[i,k] = model.addVar(lb = 0, vtype = GRB.INTEGER, name = 'N[' + str(i) + ',' + str(k) + ']')
model.update ()

# m[i,k] is the number of workers can be fired producing type i at the beginning of month k
m = {}
for i in I:
    for k in K:
        m[i,k] = model.addVar(lb = 0, vtype = GRB.INTEGER, name = 'M[' + str(i) + ',' + str(k) + ']')
model.update ()

# b[i,k] is the number of workers actually fired producing type i at the beginning of month k
b = {}
for i in I:
    for k in K:
        b[i,k] = model.addVar(lb = 0, vtype = GRB.INTEGER, name = 'B[' + str(i) + ',' + str(k) + ']')
model.update ()

a = {}
for k in K:
    a[k] = model.addVar(lb = 0, vtype = GRB.BINARY, name = 'A[' + str(k) + ']')
model.update ()


# ---- Objective Function ----

model.setObjective(quicksum((r[i,k] * holdingCosts[i] + workerCosts[k] * x[i,k] +\
                             firingCost * b[i,k]) for i in I for k in K) + quicksum(trainingCost * a[k] for k in K))
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

# Constraints 2: relationship between x[i,k] n[i,k] & b[i,k]
con2 = {}
for i in I:
    for k in K:
        if k == 0:
            con2[i,k] = model.addConstr(quicksum(x[i,k] for i in I) == quicksum(n[i,k] for i in I) - \
                                        quicksum(b[i,k] for i in I),                                 \
                                        'con2[' + str(i) + ',' + str(k) + ']-')
        else:
            con2[i,k] = model.addConstr(quicksum(x[i,k] for i in I) == quicksum(x[i,k-1] for i in I) + \
                                        quicksum(n[i,k] for i in I) - quicksum(b[i,k] for i in I),      \
                                        'con2[' + str(i) + ',' + str(k) + ']-') 

# Constraints 3: number of workers can be fired at the beginning of month k is calculated based on 
# month workers can be fired k-1
con3 = {} 
for i in I:
    for k in K:
        if k <= contractPeriods-1:
            con3[i,k] = model.addConstr(quicksum(m[i,k] for i in I) == 0, 'con3[' + str(i) + ',' + str(k) + ']-')
        else:
            con3[i,k] = model.addConstr(quicksum(m[i,k] for i in I) == quicksum(m[i,k-1] - b[i,k-1] + 
            n[i,k-contractPeriods] for i in I), 'con3[' + str(i) + ',' + str(k) + ']-')

# Constrain 4: workers actually fired is less than workers can be fired
con4 = {}
for i in I:
    for k in K:
        con4[i,k] = model.addConstr(quicksum(b[i,k] for i in I) <= quicksum(m[i,k] for i in I),
                                    'con4[' + str(i) + ',' + str(k) + ']-')


# Constraints 4: when there are newly hired workers in the beginning of month k, a[k] = 1;
# when no workers are hired in the beginning of month k, a[k] = 0
con5 = {}
for k in K:
    con5[k] = model.addConstr(quicksum(n[i,k] for i in I) <= 1000000 * a[k], 'con5[' + str(k) + ']-')

# ---- Solve ----

model.setParam( 'OutputFlag', True) # silencing gurobi output or not
model.setParam ('MIPGap', 0);       # find the optimal solution
model.write("output.lp")            # print the model in .lp format file

model.optimize()


# --- Print results ---
print('\n--------------------------------------------------------------------\n')
    
if model.status == GRB.Status.OPTIMAL: # If optimal solution is found
    print('%.2f  %.2f  %.2f  %.2f  %.2f' % (model.objVal,    
                                        sum(holdingCosts[i] * r[i,k].x for k in K for i in I),
                                        sum(workerCosts[k] * x[i,k].x for k in K for i in I),
                                        sum(firingCost * b[i,k].x for k in K for i in I),
                                        sum(trainingCost * a[k].x for k in K))) 

    #------------worker fired and hired producing each type of products in each month------------#
    hiredQuant = []
    firedQuant = []
    for i in I:
        for k in K:
            hiredQuant.append(abs(n[i,k].x))
            firedQuant.append(abs(b[i,k].x))
    f_hiredQuant = ['%.2f' % member for member in hiredQuant]
    f_firedQuant = ['%.2f' % member for member in firedQuant]

    # compute worker quantity of each month
    hiredQuantSum = []
    firedQuantSum = []
    for k in K:
        hiredQuantSum.append(sum(n[i,k].x for i in I))
        firedQuantSum.append(sum(b[i,k].x for i in I))
    f_hiredQuantSum = ['%.2f' % member for member in hiredQuantSum]
    f_firedQuantSum = ['%.2f' % member for member in firedQuantSum]

    hired =[f_hiredQuant[0:12], f_hiredQuant[12:24], f_hiredQuant[24:36], f_hiredQuantSum]
    fired =[f_firedQuant[0:12], f_firedQuant[12:24], f_firedQuant[24:36], f_firedQuantSum]
    columnNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Agu","Sept","Oct","Nov","Dec"]
    df_h = pd.DataFrame(hired, columns = columnNames, index=['1', '2', '3', 'sum'])
    df_f = pd.DataFrame(fired, columns = columnNames, index=['1', '2', '3', 'sum'])
    print('-------------------------Worker quantity per month per type-------------------------')
    print(df_h)
    print(df_f)
    print('\n')


else:
    print ('\nNo feasible solution found')

print ('\nREADY\n')
