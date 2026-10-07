'''
Problem Statement: Product Mix Optimization (Maximize total profit)
A company makes two products: Product A and Product B.
Each product requires machine time and labor hours, both of which are limited.
Resource:[Machine Time, labor time, profit per unit]
Product A:[3hours, 2hours, $30]
Product B:[2hours, 4hours, $50]
Availability:[120hours, 100hours]
'''


#Import libraries
from pulp import LpMaximize, LpProblem, LpVariable, value
from pulp import LpStatus

#Define the problem
model = LpProblem("Product Mix Optimization", LpMaximize)

#Decision Variables: x = units of Product A, y = units of Product B
x = LpVariable("Product_A", lowBound=0, cat='Continuous')
y = LpVariable("Product_B", lowBound=0, cat='Continuous')

#Objective Function: Maximize profit
model += 30 * x + 50 * y, "Total Profit"

#Constraints
model += 3 * x + 2 * y <= 120, "Machine Time Constraint"
model += 2 * x + 4 * y <= 100, "Labor Time Constraint"

#Solve the model
model.solve()

#Output Results
print(f"Status: {LpStatus[model.status]}")
print(f"Optimal number of Product A to produce: {x.varValue}")
print(f"Optimal number of Product B to produce: {y.varValue}")
print(f"Maximum Profit: ${value(model.objective)}")


