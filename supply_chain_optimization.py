from pulp import *

# Sets
factories = ['F1', 'F2', 'F3']
warehouses = ['W1', 'W2', 'W3', 'W4']

# Supply for each factory
supply = {
    'F1': 500,
    'F2': 600,
    'F3': 400
}

# Demand for each warehouse
demand = {
    'W1': 400,
    'W2': 300,
    'W3': 500,
    'W4': 300
}

# Transportation cost per unit
cost = {
    ('F1', 'W1'): 2, ('F1', 'W2'): 3, ('F1', 'W3'): 1, ('F1', 'W4'): 4,
    ('F2', 'W1'): 3, ('F2', 'W2'): 1, ('F2', 'W3'): 2, ('F2', 'W4'): 2,
    ('F3', 'W1'): 4, ('F3', 'W2'): 2, ('F3', 'W3'): 5, ('F3', 'W4'): 3
}

# Define the model
model = LpProblem("Supply_Chain_Optimization", LpMinimize)

# Decision variables
x = LpVariable.dicts("Route", (factories, warehouses), lowBound=0, cat='Continuous')

# Objective function: Minimize cost
model += lpSum([cost[(f, w)] * x[f][w] for f in factories for w in warehouses])

# Constraints
# Factory supply
for f in factories:
    model += lpSum([x[f][w] for w in warehouses]) <= supply[f], f"Supply_{f}"

# Warehouse demand
for w in warehouses:
    model += lpSum([x[f][w] for f in factories]) >= demand[w], f"Demand_{w}"

    print("Solving the optimization model...")


# Solve
model.solve()

# Output results
print("Optimal Shipping Plan:\n")
for f in factories:
    for w in warehouses:
        shipped = x[f][w].varValue
        if shipped > 0:
            print(f"Ship {shipped:.0f} units from {f} to {w}")
print(f"\nTotal Transportation Cost: ₹{value(model.objective)}")
