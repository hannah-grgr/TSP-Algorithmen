# TSP-Algorithmen

## Heuristiken für das TSP an einem Beispiel getestet

Hier wurden die Heuristiken

- (Double) Nearest Neighbor
- Cheapest Insertion
- MST
- Christofides
- Ant System

zur Bestimmung einer Rundtour in einem vollständigen ungerichteten Graphen in Python implementiert.
Die Algorithmen wurden am Beispiel der größten 100 deutschen Städte und ihrer Distanzen getestet.

In der Datei algorithmen.py wird eine Klasse für Graphen implementiert, innerhalb derer alle Algorithmen umgesetzt werden. Das Beispiel lässt sich über die Datei beispiel.py ausführen. Die Beispieldaten sind in der Datei deutschland_staedte_distanzmatrix_100.csv enthalten. Verglichen werden die Ergebnisse mit der optimalen Lösung, die vom Held-Karp-Algorithmus bestimmt wird (held_karp.py). Das Programm produziert den Plot Ant_System_Iterations.pdf, der den Verlauf der Suche innerhalb der ersten 100 Iteration des Ant System Algorithmus veranschaulicht.

## Programm ausführen:

1. Dieses Repository clonen.
2. Das Programm in der Datei beispiel.py ausführen.
3. Ggf. an eigenen Beispielen ausführen, indem in der Datei beispiel.py eine eigene CSV-Datei ((n x n)-Matrix) in die Variable file geschrieben wird und ggf. die Variable size angepasst wird.
