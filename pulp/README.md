# Solver em Python

`POC` baseada no `Yu Wei Chung` sobre [How to use Solver (Excel) in Python](https://ychung38.medium.com/how-to-use-solver-excel-in-python-458336408c7f).


## Problema

Existe um fabricante de camisetas. Eles produzem dois tipos de camisetas. Uma delas é uma camiseta feita de `seda`. A outra é aquela que é feita em `algodão`. A camiseta de `seda` é vendida por US$ 45 e custa US$ 30 por item. A camiseta de `algodão` é vendida por US$ 20 e custa $ 10 por item. Para atender a demanda do cliente, pelo menos 2.000 unidades de camiseta de `seda` e pelo menos 8.000 unidades de camiseta de `algodão` precisam ser produzidas e vendidas. O fabricante pode produzir no máximo 8.000 unidades de dois tipos de camisetas. Qual é o máximo de receita que a manufatura pode gerar?

|  Camisetas |       |       |         |        |
|:----------:|:-----:|:-----:|:-------:|:------:|
|            | Preço | Custo | Demanda | Margem |
|    Seda    |   45  |   30  |   2000  |   15   |
|   Algodão  |   20  |   10  |   8000  |   10   |
|            |       |       |         |        |
| Capacidade |  8000 |  8000 |         |        |

---

## Resolução em Python

1. Criar um DataFrame de Problema

```python
df = pd.DataFrame({'Variable': ['x1', 'x2'],
                   'Price': [45, 20],
                   'Cost': [30, 10],
                   'Demand': [2000, 8000]
                    })

df.eval('Margin=Price-Cost', inplace=True)
```

|   | Variavel | Preço | Custo | Demanda | Margem |
|:-:|:--------:|:-----:|:-----:|:-------:|--------|
| 0 |    x1    |   45  |   30  |   2000  | 15     |
| 1 |    x2    |   20  |   10  |   8000  | 10     |

2. Defina o problema

```python
from pulp import * 

# set the dictionary for each feature
prob = LpProblem('Sell', LpMaximize) # Objective function

inv_item = list(df['Variable']) # Variable name

margin = dict(zip(inv_items, df['Margin'])) # Function 

demand = dict(zip(inv_items, df['Demand'])) # Function

# next, we are defining our decision variables as investments and are adding a few parameters to it
inv_vars = LpVariable.dicts('Vairable', inv_items, lowBound=0, cat='Integar')

# set the decision variables
# all add in the problem setting
prob += lpSum([inv_vars[i] * margin[i] for i in inv_items])

# Constraint
prob += lpSum([inv_vars[i] for i in inv_items]) <= 8000, 'Total Demand'

# Constraint
prob += inv_vars['x1'] <= 2000, 'x1 Demand'

# Constraint
prob += inv_vars['x2'] <= 8000, 'x2 Demand'
```

É isso. Definimos tudo sobre o problema, como objetivo, variáveis, restrições. Verificamos o 'problema' novamente.

```python
# Rode isto. Por exemplo, clique em resolver para permitir que o Solver seja executado. 
prob.solve()
```
```bash
Problem MODEL has 3 rows, 2 columns and 4 elements
Coin0008I MODEL read with 0 errors
Option for timeMode changed from cpu to elapsed
Presolve 0 (-3) rows, 0 (-2) columns and 0 (-4) elements
Empty problem - 0 rows, 0 columns and 0 elements
Optimal - objective value 90000
After Postsolve, objective 90000, infeasibilities - dual 0 (0), primal 0 (0)
Optimal objective 90000 - 0 iterations time 0.002, Presolve 0.00
Option for printingOptions changed from normal to all
Total time (CPU seconds):       0.00   (Wallclock seconds):       0.00
```

Depois de executarmos o código de resolução, devemos ficar curiosos sobre qual é a resposta para o objetivo e o valor das variáveis.

```python
# Answer
value(prob.objective) # 9000
# Variables' values
print('The optimal answer\n'+'-'*70)
for v in prob.variables():
    if v.varValue > 0:
       print(v.name, '=', v.varValue)
```

```sh
15*Vairable_x1 + 10*Vairable_x2
The optimal answer
----------------------------------------------------------------------
Vairable_x1 = 2000.0
Vairable_x2 = 6000.0
```

Olhar! É a mesma resposta que obtemos no Solver. E é mais fácil fazê-lo.