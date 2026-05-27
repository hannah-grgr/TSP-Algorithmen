import algorithmen
import held_karp
import csv
import numpy as np


def read_csv(n, file): # Liest eine CSV-Datei ein und gibt den entsprechenden Graphen mit n Ecken aus
    
    # Vollständigen Graphen G = (V,E) mit |V| = n anlegen
    graph = algorithmen.Graph(n)
    graph.A = np.full((n, n), 1)

    # Aus der CSV-Datei werden die Distanzen gelesen und in die Kostenmatrix eingetragen
    with open(file, mode = 'r') as f:
        reader = csv.reader(f, delimiter = ';')
        headings = next(reader)
        j = 2
        for row in reader:
            for i in range(j,n+1):
                num = row[i]
                num = num.replace(',','.')
                graph.add_weight(j-1, i, float(num))
            j += 1
            
    return graph


# DEUTSCHLANDS 50 GRÖßTE STÄDTE

file = 'deutschland_staedte_distanzen.csv'
size = [5, 10, 20, 50]

for n in size:
    print("n = ", n)
    graph = read_csv(n, file)
    print("NN:		", graph.nearest_neighbor())
    print("NN: Min:	", min({graph.nearest_neighbor(i+1)[1] for i in range(n)}))
    print("2NN:		", graph.double_nearest_neighbor())
    print("2NN: Min:	", min({graph.double_nearest_neighbor(i+1)[1] for i in range(n)}))
    print("CI:		", graph.cheapest_insertion())
    print("MST:		", graph.minimum_spanning_tree())
    print("CH:		", graph.christofides())
    print("AS:		", graph.ant_system())
    
    if n <= 20:
        hk = held_karp.held_karp(graph.C) # Rückgabewert ist das Tupel (minimale Kosten, Tour)
        tour = hk[1]
        tour = [i+1 for i in tour] # bei held_karp wird mit Ecken 0,..,n-1 gearbeitet
        tour.pop(0) # 1. Wert kommt doppelt vor
        tour_length = hk[0]
        print("optimal:	", [tour, tour_length])
    print("")