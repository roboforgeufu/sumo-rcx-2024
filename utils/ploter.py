import csv
import sys

import matplotlib.pyplot as plt

"""
Módulo pra plotar CSVs genéricos

Eixo horizontal: primeira coluna do csv
Cada uma das colunas depois da primeira será plotada como uma linha do gráfico

Primeiro argumento da linha de comando deve ser o arquivo csv.
O segundo argumento é a flag "-y", pra pular a etapa de confirmação.
"""

GRAPHS_DIRECTORY = "graphs"


FILENAME = sys.argv[1]
print(f"GENERATING GRAPH FOR {FILENAME}")

if len(sys.argv) <= 2 or sys.argv[2] != "-y":
    input("Press any key to continue...")

with open(FILENAME) as file:
    data = list(csv.reader(file))


headers = True
x_data = [] # lista com valores pro eixo horizontal
ys_data = [] # lista de listas de valores para cada uma das linhas do eixo vertical

headers = data[0]

for row in data[1:]: # skip headers
    x_data.append(float(row[0]))

    for index, row_data in enumerate(row[1:]):
        if len(ys_data) < len(row) - 1:
            # povoamento inicial de cada uma das listas de valores (p/ cada uma das colunas)
            ys_data.append([])
        
        ys_data[index].append(float(row_data))


plt.figure(figsize=(15,6))
for y_data in ys_data:
    plt.plot(x_data, y_data)
plt.grid()


FILENAME = FILENAME.split("/")[-1] # pega a última parte do nome do arquivo

plt.title(FILENAME)
print(f"Saving to {GRAPHS_DIRECTORY}/{FILENAME}.png")
plt.savefig(f"{GRAPHS_DIRECTORY}/{FILENAME}.png", bbox_inches='tight')
