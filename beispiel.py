import algorithmen
import held_karp
import csv
import numpy as np
import time
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


# DEUTSCHLANDS 100 GRÖßTE STÄDTE

file = 'deutschland_staedte_distanzmatrix_100.csv'
size = [5, 10, 20, 50, 75, 100]

for n in size:
    print("n = ", n)
    graph = read_csv(n, file)

    # Für n = 100 wollen wir die Rechenzeit messen:
    if n == 100:
        # NN
        start = time.time()
        nn = graph.nearest_neighbor()
        end = time.time()
        print("NN:		", nn)
        print("Rechenzeit: ", end - start)
        
        # NN Min
        start = time.time()
        nn_min = min({graph.nearest_neighbor(i)[1] for i in range(n)})
        end = time.time()
        print("NN: Min:	", nn_min)
        print("Rechenzeit: ", end - start)

        # 2NN
        start = time.time()
        dnn = graph.double_nearest_neighbor()
        end = time.time()
        print("2NN:		", dnn)
        print("Rechenzeit: ", end - start)

        # 2NN Min
        start = time.time()
        dnn_min = min({graph.double_nearest_neighbor(i)[1] for i in range(n)})
        end = time.time()
        print("2NN: Min:	", dnn_min)
        print("Rechenzeit: ", end - start)

        # CI
        start = time.time()
        ci = graph.cheapest_insertion()
        end = time.time()
        print("CI:		", ci)
        print("Rechenzeit: ", end - start)

        # CI Min
        start = time.time()
        ci_min = min({graph.cheapest_insertion(i)[1] for i in range(n)})
        end = time.time()
        print("CI: Min:	", ci_min)
        print("Rechenzeit: ", end - start)

        # MST
        start = time.time()
        mst = graph.minimum_spanning_tree()
        end = time.time()
        print("MST:		", mst)
        print("Rechenzeit: ", end - start)

        # MST Min
        start = time.time()
        mst_min = graph.minimum_spanning_tree(both_directions = True)
        end = time.time()
        print("MST: Min:       ", mst_min[1])
        print("Rechenzeit: ", end - start)

        # CH
        start = time.time()
        ch = graph.christofides()
        end = time.time()
        print("CH:	    ", ch)
        print("Rechenzeit: ", end - start)

        # CH Min
        start = time.time()
        ch_min = graph.christofides(both_directions = True)
        end = time.time()
        print("CH: Min:        ", ch_min[1])
        print("Rechenzeit: ", end - start)

        # AS
        start = time.time()
        ant = graph.ant_system(ants = n, iterations = 100)
        end = time.time()
        print("AS:		", ant)
        print("Rechenzeit: ", end - start)


    else:
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
        start = time.time()
        hk = held_karp.held_karp(graph.C) # Rückgabewert ist das Tupel (minimale Kosten, Tour)
        end = time.time()
        tour = hk[1]
        tour.pop(0) # 1. Wert kommt doppelt vor
        tour_length = hk[0]
        print("optimal:	", (tour, tour_length))
        if n == 20:
            print("Rechenzeit: ", end - start)
    print("")

    # Für n = 100 wollen wir den Suchverlauf von AS als Plot ausgeben:
    if n == 100:
        # Plot
        plt.figure()
        plt.plot(algorithmen.plot_tour_costs)
        graph.ant_system(ants = n, iterations = 100)
        plt.plot(algorithmen.plot_tour_costs)
        graph.ant_system(ants = n, iterations = 100)
        plt.plot(algorithmen.plot_tour_costs)
        plt.xlabel('Iterationen')
        plt.ylabel('Tourkosten')
        plt.savefig('Ant_System_Iterations.pdf')
        plt.close()