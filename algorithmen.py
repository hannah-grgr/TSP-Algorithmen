import numpy as np
import networkx
import random
            
            
# G = (V,E) mit V = {0,...,n-1}           
class Graph:
    
    # Initialisierung eines Graph
    def __init__(self, n):
        self.n = n								# Anzahl der Knoten
        self.A = np.zeros((n, n), dtype = int)	# Initialisierung der Adjazenzmatrix
        self.C = np.full((n, n), np.inf)		# Initialisierung der Kostenmatrix
        np.fill_diagonal(self.C, 0)				# Jeder Knoten ist von sich selbst aus ohne Kosten zu erreichen.

    # Kanten hinzufügen
    def add_edge(self, u, v):
        self.A[u][v] += 1
        self.A[v][u] += 1 					    # Symmetrie der Adjazenzmatrix im ungerichteten Graphen
    
    # Kante löschen
    def delete_edge(self, u, v):
        self.A[u][v] -= 1
        self.A[v][u] -= 1 					    # Symmetrie der Adjazenzmatrix im ungerichteten Graphen
        
    # Kantengewicht hinzufügen
    def add_weight(self, u, v, weight):
        self.C[u][v] = weight
        self.C[v][u] = weight 	    			# Symmetrie der Kostenmatrix im ungerichteten Graphen
    
    # Adjazenzmatrix ausgeben
    def display_A(self):
        for i in range(self.n):
            print(self.A[i])
    
    # Kostenmatrix ausgeben
    def display_C(self):
        for i in range(self.n):
            print(self.C[i])
    
    
    ###############
    # HEURISTIKEN #
    ###############

    
    # Nearesr Neighbor (NN)
    def nearest_neighbor(self, start = 0):
        V_m = [k for k in range(self.n)]								# V_m = {0,...,n-1} (enthält alle Knoten, die noch nicht hinzugefügt wurden)
        tour = []														# Initialisiere die Rundtour                           
        tour.append(start)												# Startknoten (standardmäßig wird im 0. Knoten gestartet)
        V_m.remove(start)
        cost = 0														# Initialisiere Kosten
        while len(V_m) > 0:												# Solange wir noch nicht alle Knoten besucht haben:
            i = V_m[0]
            for j in V_m:												# Finde nächsten Knoten mit minimalem Abstand zum letzten ...
                if self.C[j][tour[-1]] < self.C[i][tour[-1]]:
                    i = j
            cost += self.C[i][tour[-1]]
            tour.append(i)												# ... und füge ihn hinzu.
            V_m.remove(i)
        cost += self.C[tour[-1]][tour[0]]				    			# Rundtour schließen
        tour.append(tour[0])
        return tour, cost
    
    
    # Double Nearest Neighbor (2NN)
    def double_nearest_neighbor(self, start = 0):
        V_m = [k for k in range(self.n)]								# V_m = {0,...,n-1} (enthält alle Knoten, die noch nicht hinzugefügt wurden)
        tour = []														# Initialisiere die Rundtour                           
        tour.append(start)												# Startknoten (standardmäßig wird im 0. Knoten gestartet)
        V_m.remove(start)
        cost = 0														# Initialisiere Kosten
        while len(V_m) > 0:												# Solange wir noch nicht alle Knoten besucht haben:
            j_0 = V_m[0]
            for j in V_m:												# Finde nächsten Knoten j_0 mit minimalem Abstand zum ersten.
                if self.C[j][tour[0]] < self.C[j_0][tour[0]]:
                    j_0 = j
            j_1 = V_m[0]
            for j in V_m:												# Finde nächsten Knoten j_1 mit minimalem Abstand zum letzten.
                if self.C[j][tour[-1]] < self.C[j_1][tour[-1]]:
                    j_1 = j
            if self.C[j_0][tour[0]] < self.C[j_1][tour[-1]]:	        # Füge denjenigen Knoten hinzu, der zur geringeren Kostenerhöhung führt.
                cost += self.C[j_0][tour[0]]
                tour.insert(0, j_0)
                V_m.remove(j_0)
            else:
                cost += self.C[j_1][tour[-1]]
                tour.append(j_1)
                V_m.remove(j_1)
        cost += self.C[tour[-1]][tour[0]]   							# Rundtour schließen
        tour.append(tour[0])
        return tour, cost
    
    
    # Cheapest Insertion (CI)
    def cheapest_insertion(self, start = 0):
        V_m = [k for k in range(self.n)]								# V_m enthält alle Knoten, die noch nicht hinzugefügt wurden
        i_1 = start                                                     # Startknoten (standardmäßig wird im 0. Knoten gestartet)
        V_m.remove(i_1)
        d_2 = np.inf                                                    # Finde nächsten Knoten mit minimalem Abstand zum Startknoten.
        for i in V_m:
            if self.C[i_1][i] < d_2:
                d_2 = self.C[i_1][i]
                i_2 = i
        tour = [i_1, i_2, i_1]                                          # Startkreis
        V_m.remove(i_2)
        while len(V_m) > 0:												# Solange wir noch nicht alle Knoten besucht haben:
            d_j_m = np.inf												# Initialisiere minimale Kostenerhöhung für j_m (d(j_m))
            for j in V_m:												# Betrachte alle Knoten, die noch nicht eingefügt wurden.
                d_j = np.inf											# Initialisiere minimale Kostenerhöhung für j (d(j))
                for k in range(len(tour)-1):							# Betrachte alle möglichen Positionen...
                    d_j_k = self.C[tour[k]][j] + self.C[j][tour[k+1]] - self.C[tour[k]][tour[k+1]]
                                                                        # c(i_k,j) + c(j,i_{k+1}) - c(i_k,i_{k+1}
                    if d_j_k < d_j:										# ... und suche das Minimum.
                        d_j = d_j_k
                        k_min = k										# k_min = Position, an der das Minimum für j angenommen wird
                if d_j < d_j_m:											# Finde das Minimum über alle j.
                    j_m = j												# j_m ist der Knoten, der eingefügt werden soll
                    d_j_m = d_j
                    k_j_m = k_min										# k_j_m = Position, an der das Minimum für j_m angenommen wird
            tour.insert(k_j_m + 1, j_m)								    # Füge den Knoten, der zur minimalen Kostenerhöhung führt, hinzu.
            V_m.remove(j_m)
        cost = 0														# Berechne die Kosten der Rundtour.
        for i in range(len(tour)-1):
            cost += self.C[tour[i]][tour[i+1]]    
        return tour, cost
    
    
    # Tiefensuche (Suche nach Kreisen)
    def dfs(self, u, visited, parent):
        visited.append(u)								# Mit dem Aufruf der Tiefensuche für den Knoten u wird dieser besucht.
        for i in range(self.n):							# Iteriere über alle Knoten
            if self.A[u][i] != 0:						# und, wenn der Knoten ein Nachbar von u ist...
                if i not in visited:					# ... und noch nicht besucht wurde,
                    if self.dfs(i, visited, u):			# rufe die Tiefensuche (rekursiv) für diesen Knoten auf (mit u als parent).
                        return True						# und gebe das Ergebnis zurück.
                else:									# ... und bereits besucht wurde,
                    if parent != i:						# aber nicht parent des aktuell betrachteten Knoten u ist,
                        return True						# wurde ein Kreis gefunden und es wird True zurückgegeben.
        return False
        
        
    # Test auf Kreisfreiheit
    def is_cyclic(self):
        visited = []							        # Anfangs sind noch keine Knoten besucht.
        for i in range(self.n):					        # Iteriere über alle Knoten...
            if i not in visited:				        # und führe, falls dieser noch nicht besucht wurden, die Tiefensuche durch.
                if self.dfs(i, visited, None):	        # Wenn die Tiefensuche einen Kreis findet,
                    return True					        # wird True zurückgegeben.
        return False							        # Falls kein Kreis gefunden wurde, False.
    
    
    # Bestimmung MST
    def kruskal(self):
        weighted_edges = []												# Speichere alle Kanten mit endlichem Gewicht in einer Liste.
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.C[i][j] != np.inf:
                    weighted_edges.append([self.C[i][j], i, j])		    # Kanten werden als Tripel (c(i,j), i, j) gespeichert
        sorted_edges = sorted(weighted_edges)							# Sortiere Kanten nach Gewicht.
        MST = Graph(self.n)												# Lege MST mit n Ecken (ohne Kanten) an.
        for i in range(len(sorted_edges)):								# Iteriere über alle Kanten (in sortierter Reihenfolge)
            MST.add_edge(sorted_edges[i][1], sorted_edges[i][2])		# und prüfe, ob der Graph nach Hinzufügen der nächsten Kante
            if MST.is_cyclic():											# immer noch kreisfrei ist.
                MST.delete_edge(sorted_edges[i][1], sorted_edges[i][2])	# Falls sich ein Kreis ergibt, verwerfen wir die Kante.
            else:														# Falls sich kein Kreis ergibt, behalten wir die Kante und nehmen noch ihr Gewicht mit auf.
                MST.add_weight(sorted_edges[i][1], sorted_edges[i][2], sorted_edges[i][0])
        return MST
    
    
    # Hilfsfunktion, um einen Hamiltonkreis aus einem Euler-Zug in einem NetworkX-Graphen zu konstruieren
    def euler_to_hamilton(self, G, both_directions):
        euler_edges = list(networkx.eulerian_circuit(G))				# Finde Euler-Zug
        euler = []														# Wandle euler_edges (Liste von Kanten) in eine Liste von Ecken um.
        for i in range(len(euler_edges)):
            euler.append(euler_edges[i][0])
        euler.append(euler[0])											# Rundtour schließen
        
        # Konstruiere Hamiltonkreis
        tour = [] 													    # Initialisiere Hamiltonkreis
        for i in euler:
            if i not in tour:										    # Bereits durchlaufene Ecken werden übersprungen und
                tour.append(i)										    # neue Ecken werden hinzugefügt.
        tour.append(tour[0])									        # Schließe den Hamilton-Weg zum Hamilton-Kreis.
        
        # Berechne die Kosten der Rundtour.
        cost = 0
        for i in range(len(tour)-1):
            cost += self.C[tour[i]][tour[i+1]]

        # Falls gewünscht, betrachte zusätzlich den Hamiltonkreis, der beim Durchlaufen des Euler-Zugs in die andere Richtung entsteht.
        if both_directions:
            # Konstruiere Hamiltonkreis 
            tour2 = [] 													    # Initialisiere Hamiltonkreis
            for i in reversed(euler):
                if i not in tour2:										    # Bereits durchlaufene Ecken werden übersprungen und
                    tour2.append(i)										    # neue Ecken werden hinzugefügt.
            tour2.append(tour2[0])									        # Schließe den Hamilton-Weg zum Hamilton-Kreis.

            # Berechne die Kosten der Rundtour.
            cost2 = 0
            for i in range(len(tour2)-1):
                cost2 += self.C[tour2[i]][tour2[i+1]]

            # Gebe die günstigere Rundtour zurück
            if cost <= cost2:
                return tour, cost
            else:
                return tour2, cost2

        else:
            return tour, cost


    # Minimum Spanning Tree (MST)
    def minimum_spanning_tree(self, both_directions = False):
        
        # Konstruiere MST (mithilfe von Kruskal)
        MST = self.kruskal()
                    
        # Konstruiere Eulerschen Graphen
        G = networkx.MultiGraph()										# Erzeuge einen Multigraphen der Bibliothek NetworkX (um eulerian_circuit() anwenden zu können),
        for i in range(self.n):											# der dem MST mit verdoppelten Kanten entspricht.
            for j in range(i+1, self.n):
                if MST.A[i][j] != 0:
                    G.add_edge(i, j, weight = MST.C[i][j])
                    G.add_edge(i, j, weight = MST.C[i][j])
        
        # Finde Euler-Zug im Eulerschen Graphen und konstruiere daraus einen Hamiltonkreis:
        return self.euler_to_hamilton(G, both_directions)
    

    # Christofides (CH)
    def christofides(self, both_directions = False):
        
        # Konstruiere MST (mithilfe von Kruskal)
        MST = self.kruskal()
        
        # Betrachte die Menge U der Ecken ungeraden Grades
        U = []
        for i in range(self.n):
            if sum(MST.A[i]) %2 != 0:
                U.append(i)
                
        # Minimales perfektes Matching auf U mithilfe von NetworkX
        U_Graph = networkx.Graph()										# Erzeuge einen Multigraphen der Bibliothek NetworkX (um min_weight_matching() anwenden zu können),
        for i in range(len(U)):											# der dem vollständigen Teilgraphen auf U entspricht.
            for j in range(i+1, len(U)):
                U_Graph.add_edge(U[i], U[j], weight = self.C[U[i]][U[j]])
        matching = networkx.min_weight_matching(U_Graph)				# Finde minimales perfektes Matching
        
        # Konstruiere Eulerschen Graphen
        G = networkx.MultiGraph()										# Erzeuge einen Multigraphen der Bibliothek NetworkX (um eulerian_circuit() anwenden zu können),
        for i in range(self.n):											# der dem MST mit hinzugefügten Kanten entspricht.
            for j in range(i+1, self.n):
                for k in range(MST.A[i][j]):
                    G.add_edge(i, j, weight = MST.C[i][j])
        for edge in matching:
            G.add_edge(edge[0], edge[1], weight = self.C[edge[0]][edge[1]])

        # Finde Euler-Zug im Eulerschen Graphen und konstruiere daraus einen Hamiltonkreis:
        return self.euler_to_hamilton(G, both_directions)
   
   
    # Ant System (AS)
    def ant_system(self, ants = 10, iterations = 50, alpha = 1, beta = 3, rho = 0.5): # Parameter setzen

        # Pheromonspuren initialisieren
        pheromone = np.full((self.n, self.n), ants/(self.nearest_neighbor()[1]))
        np.fill_diagonal(pheromone, 0)	
        
        # beste Tour initialisieren
        best_tour = None
        best_tour_cost = np.inf

        # Tourkosten nach jeder Iteration
        global plot_tour_costs 
        plot_tour_costs = []
        
        # Iteration
        for t in range(iterations):
            tours = []
            tour_costs = []
            
            # Tour-Konstruktion durch jede Ameise
            for k in range(ants):
                
                # visited-Liste als Tour-Memory
                visited = []
                
                # Start in zufälliger Stadt
                i = random.randint(0, self.n-1)
                visited.append(i)
                
                L_k = 0 # Tour-Länge mit 0 initialisieren
                
                # Solange noch nicht alle Knoten besucht wurden:
                while len(visited) < self.n:
                    
                    # N_i Liste der unbesuchten Nachbarn der Ameise k am Punkt i
                    N_i = []
                    for j in range(self.n):
                        if j not in visited and self.A[i][j] != 0: # unbesuchte Nachbarn
                            N_i.append(j)
                    
                    # Wahrscheinlichkeit berechnen, in die Stadt j zu gehen
                    p_i = []
                    for j in N_i:
                        p_ij = (pheromone[i][j]**alpha * (1/self.C[i][j])**beta)
                        p_i.append(p_ij)
                    p_i = p_i / sum(p_i)
                    
                    # zufällige Wahl der nächsten Stadt
                    j = np.random.choice(N_i, p = p_i)
                    visited.append(j)
                    L_k += self.C[i][j]
                    i = j
                    
                # Tour schließen
                L_k += self.C[visited[0]][visited[-1]]
                visited.append(visited[0])

                # Tour hinzufügen
                tours.append(visited)
                tour_costs.append(L_k)
                
                # Verbesserung prüfen
                if L_k < best_tour_cost:
                    best_tour_cost = L_k
                    best_tour = visited
            
            # Pheromon-Update
            
            # Pheromon-Verdunstung
            pheromone *= (1-rho)
            
            # Pheromon auf besuchten Kanten anpassen
            for k in range(ants):
                for i in range(self.n):
                    pheromone[tours[k][i]][tours[k][i+1]] += 1/tour_costs[k]
                    pheromone[tours[k][i+1]][tours[k][i]] += 1/tour_costs[k] # Symmetrie

            # beste bisherige Tour wird nach jeder Iteration für einen Plot gespeichert
            plot_tour_costs.append(best_tour_cost)
            
        return best_tour, best_tour_cost
