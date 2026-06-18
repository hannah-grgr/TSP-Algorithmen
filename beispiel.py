import algorithmen
import held_karp
import csv
import numpy as np
import matplotlib.pyplot as plt


def read_csv(n, file): # Liest eine CSV-Datei ein und gibt den entsprechenden Graphen mit n Ecken aus
    
    # Vollständigen Graphen G = (V,E) mit |V| = n anlegen
    graph = algorithmen.Graph(n)
    graph.A = np.full((n, n), 1)
    np.fill_diagonal(graph.A, 0)

    # Aus der CSV-Datei werden die Distanzen gelesen und in die Kostenmatrix eingetragen
    with open(file, mode = 'r') as f:
        reader = csv.reader(f, delimiter = ';')
        headings = next(reader)
        j = 1
        for row in reader:
            for i in range(j+1,n+1):
                num = row[i]
                num = num.replace(',','.')
                graph.add_weight(j-1, i-1, float(num))
            j += 1
            
    return graph


# DEUTSCHLANDS 50 GRÖßTE STÄDTE

file = 'deutschland_staedte_distanzmatrix_100.csv'
size = [5, 10, 20, 50, 75, 100]

for n in size:
    print("n = ", n)
    graph = read_csv(n, file)
    print("NN:		", graph.nearest_neighbor())
    print("NN: Min:	", min({graph.nearest_neighbor(i)[1] for i in range(n)}))
    print("2NN:		", graph.double_nearest_neighbor())
    print("2NN: Min:	", min({graph.double_nearest_neighbor(i)[1] for i in range(n)}))
    print("CI:		", graph.cheapest_insertion())
    print("CI: Min:	", min({graph.cheapest_insertion(i)[1] for i in range(n)}))
    print("MST:		", graph.minimum_spanning_tree())
    print("MST: Min:       ", graph.minimum_spanning_tree(both_directions = True)[1])
    print("CH:		", graph.christofides())
    print("CH: Min:        ", graph.christofides(both_directions = True)[1])
    print("AS:		", graph.ant_system(ants = n, iterations = 100))
    
    # Für n <= 20 können wir die optimale Lösung berechnen:
    if n <= 20:
        hk = held_karp.held_karp(graph.C) # Rückgabewert ist das Tupel (minimale Kosten, Tour)
        tour = hk[1]
        tour.pop(0) # 1. Wert kommt doppelt vor
        tour_length = hk[0]
        print("optimal:	", (tour, tour_length))
    print("")

    # Für n = 100 wollen wir den Suchverlauf von AS als Plot ausgeben:
    if n == 100:
        # Plot
        plt.plot(algorithmen.plot_tour_costs)
        plt.xlabel('Iterationen')
        plt.ylabel('Tourkosten')
        plt.savefig('Ant_System_Iterations.pdf')
        plt.show()