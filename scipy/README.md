# SciPy

`POC` baseada no `Patrick Ágton de Oliveira` sobre [SciPy x Solver: otimizando custos na compra de adubo](https://patrickagton.medium.com/scipy-x-solver-como-otimizar-a-compra-de-adubos-1fc03b035bbf).

## Links úteis

Documentação: [https://docs.scipy.org/doc/scipy/index.html](https://docs.scipy.org/doc/scipy/index.html)
Exemplo de uso: [SciPy x Solver: otimizando custos na compra de adubo](https://patrickagton.medium.com/scipy-x-solver-como-otimizar-a-compra-de-adubos-1fc03b035bbf)

## Problema

Uma dificuldade do produtor rural é a escolha de que adubo utilizar de acordo com suas necessidades. Hoje em dia, análises nutricionais permitem o diagnóstico completo do solo de grandes áreas e, a partir disso, saber a necessidade de complemento nutricional do solo estudado. Basicamente, existem três nutrientes primários que tem um papel fundamental para o desenvolvimento das culturas:

* N : Nitrato

* P: Fósforo

* K: Potássio

E partindo da análise de solo desses três nutrientes específicos e também da cultura desejada, ou seja, da necessidade daquela cultura desses nutrientes para se desenvolverem, o produtor pode saber qual é sua necessidade em toneladas de cada nutriente para dispor no solo e fertiliza-lo.

Pensando nisso foi desenvolvido trabalho tanto usando SciPy Optmize, quanto Solver, para obter respostas a partir da concentração de NPK em cada adubo e também de seus valores no mercado.

### Dados utilizados

Primeiro, para se basear na concentração de adubos, foi levado em consideração tabela disponibilizada a partir de um estudo acadêmico.

|      MATERIAL     | PRODUÇÃO (kg/cab/ano) |  N  |   P  |  K  | Ca (%) |  Mg |  S  |  Cl |
|:-----------------:|:---------------------:|:---:|:----:|:---:|:------:|:---:|:---:|:---:|
| Farinhas e tortas |                       |     |      |     |        |     |     |     |
| Farinhas de ossos |           -           | 2.0 | 12.2 |  -  |  23.6  | 0.3 | 0.2 |  -  |
|  Farinha de peixe |           -           | 9.5 |  2.6 |  -  |   6.1  | 0.3 | 0.2 | 1.5 |
|  Torta de mamona  |           -           | 6.0 |  0.6 | 0.4 |   0.4  | 0.3 |  -  | 0.3 |
|   Torta e cacau   |           -           | 2.5 |  0.6 | 1.0 |   1.2  |  -  |  -  |  -  |
|  Torta de algodão |           -           | 6.6 |  1.1 | 1.2 |   0.4  | 0.9 | 0.2 |  -  |
| Torta de amendoim |           -           | 7.2 |  0.6 | 1.0 |   0.4  | 0.3 | 0.6 | 0.1 |
|   Torta de soja   |           -           | 7.0 |  0.5 | 1.3 |   0.4  | 0.3 | 0.2 |  -  |
|      Estercos     |                       |     |      |     |        |     |     |     |
|      De gado      |          9490         | 0.6 |  0.1 | 0.5 |    -   |  -  |  -  |  -  |
|      De cabra     |          500          | 2.8 |  0.6 | 2.4 |    -   |  -  |  -  |  -  |
|      De porco     |          900          | 1.0 |  0.3 | 0.7 |    -   |  -  |  -  |  -  |
|     De cavalo     |          6000         | 0.7 |  0.1 | 0.4 |    -   |  -  |  -  |  -  |
|     De galinha    |           18          | 1.6 |  0.5 | 0.8 |    -   |  -  |  -  |  -  |
|     De ovelhas    |          500          | 2.0 |  0.4 | 2.1 |    -   |  -  |  -  |  -  |

Além disso, foi levado em conta os seguintes preços dos produtos no mercado:

|                   |  N |  P |  K | Ca |  S | Preço R$/t |
|:-----------------:|:--:|:--:|:--:|:--:|:--:|:----------:|
|       Ureia       | 45 |  0 |  0 |  0 |  0 |    2100    |
| Sulfato de Amônio | 21 |  0 |  0 |  0 | 24 |    1600    |
| Nitrato de Amônio | 32 |  0 |  0 |  0 |  0 |    1700    |
|        MAP        | 10 | 52 |  0 |  0 |  0 |    2500    |
|        DAP        | 16 | 46 |  0 |  0 |  0 |    1970    |
|    Super Triplo   |  0 | 44 |  0 | 10 |  0 |    1630    |
|   Super Simples   |  0 | 18 |  0 | 16 |  8 |    1250    |
|        KCI        |  0 |  0 | 60 |  0 |  0 |    2000    |
|      20-00-20     | 20 |  0 | 20 |  0 |  0 |    1850    |
|   Esterco Bovino  | 17 |  9 | 14 |  0 |  0 |     350    |
|   Esterco Suíno   | 19 |  7 |  4 |  0 |  0 |     280    |
| Composto Orgânico | 14 | 14 |  8 |  0 |  0 |     200    |

Além disso, a partir de Waard (1980) estabelece que para cada quilo de pimenta produzida são extraídos do solo 32g de N, 5g de P, 28g de K, 8g de Ca e 3g de Mg, sendo necessários ainda, para o desenvolvimento da planta, 106g de N, 8g de P, 84g de K, 36g de Ca e 11g de Mg. Assim, as restrição são dadas por:

* N ≥ 138 g

* P ≥ 14 g

* K ≥ 112 g

Sendo esses valores para 1 quilo de pimenta.

Com essas informações é possível fazer a análise necessária para otimização da compra de adubos.

---

## Resolução em Python

Antes de tudo se faz a importação dos pacotes:

```python
import numpy as np
from scipy.optimize import linprog
```

Tendo isso, o produtor terá que dar entrada na quantidade de nutriente NPK necessária para adubação de sua cultura em toneladas.

```python
n = (float(input("Qual a recomendação de N? "))) / 1000
p = (float(input("Qual a recomendação de P205? "))) / 1000
k = (float(input("Qual a recomendação de K? "))) / 1000
```

Assim, com os dados dispostos na Imagem 2 se faz duas arrays; uma dos preços e outra da concentração de nutrientes em cada adubo.

```python
c = np.array([2100, 1600, 1700, 2500, 1970, 1630, 1250, 2000, 1850, 350, 280, 200])

Ac = np.array(
    [
        [0.45, 0, 0],
        [0.21, 0, 0],
        [0.32, 0, 0],
        [0.10, 52, 0],
        [0.16, 46, 0],
        [0.0, 44, 0],
        [0.0, 18, 0],
        [0.0, 0, 60],
        [0.20, 0, 20],
    ]
)
```

Obs: nesta matriz só foi utilizado os nove primeiros nutrientes, ou seja, excluindo os três últimos esterco bovino, esterco suíno e composto orgânico.

Para aplicação na linpro transpomos a matriz de nutrientes. Uma transposição é fazer de uma coluna uma linha em outra matriz.

Assim, temos:

```python
Ae = np.transpose(Ac)

be = np.array([n, p, k])
```

Aplicando a função linpro:

```python
res = linprog(c, A_eq=Ae, b_eq=be, method="simplex")
```

Após isso é só preparar os prints de saída para visualização dos resultados de otimização.

```python
# resultado = [{:8.2f}.format(res.x)]
# apresentando os resultados da otimização
print("Resultados obtidos com problemas de otimização de custos\n\n")
print(f"Custo total de adubação obtido (R$) = { np.format_float_positional(res.fun, precision=2) }")
print(f"Utilização de Uréia (kg) = { np.format_float_positional(res.x[0]*1000, precision=2) }")
print(f"Utilização de Sulfato de Amônia (kg) = {np.format_float_positional(res.x[1]*1000, precision=2)}")
print(f"Utilização de Nitrato de Amônia (kg) = {np.format_float_positional(res.x[2]*1000, precision=2)}")
print(f"Utilização de MAP (kg) = {np.format_float_positional(res.x[3]*1000, precision=2)}")
print(f"Utilização de DAP (kg) = {np.format_float_positional(res.x[4]*1000, precision=2)}")
print(f"Utilização de ST (kg) = {np.format_float_positional(res.x[5]*1000, precision=2)}")
print(f"Utilização de SS (kg) = {np.format_float_positional(res.x[6]*1000, precision=2)}")
print(f"Utilização de Kcl (kg) = {np.format_float_positional(res.x[7]*1000, precision=2)}")
print(f"Utilização de 20-00-20 (kg) = {np.format_float_positional(res.x[8]*1000, precision=2)}")
```