import pandas as pd

from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

df = pd.DataFrame(
    {
        "Variable": ["x1", "x2"],
        "Price": [45, 20],
        "Cost": [30, 10],
        "Demand": [2000, 8000],
    }
)

df.eval("Margin=Price-Cost", inplace=True)

# set the dictionary for each feature
prob = LpProblem("Sell", LpMaximize)  # Objective function

inv_item = list(df["Variable"])  # Variable name

margin = dict(zip(inv_item, df["Margin"]))  # Function

demand = dict(zip(inv_item, df["Demand"]))  # Function

# next, we are defining our decision variables as investments and are adding a few parameters to it
inv_vars = LpVariable.dicts("Vairable", inv_item, lowBound=0, cat="Integar")

# set the decision variables
# all add in the problem setting
prob += lpSum([inv_vars[i] * margin[i] for i in inv_item])

# Constraint
prob += lpSum([inv_vars[i] for i in inv_item]) <= 8000, "Total Demand"

# Constraint
prob += inv_vars["x1"] <= 2000, "x1 Demand"

# Constraint
prob += inv_vars["x2"] <= 8000, "x2 Demand"

prob.solve()

# Answer
print(value(prob.objective))  # 90000
# Variables' values
print("The optimal answer\n" + "-" * 70)
for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)
