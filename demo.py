from graph import *

# Define the graph
source = Node("Source")
sink = Node("Sink")
a = Node("A")
b = Node("B")
c = Node("C")

source.add_edge(a, 10)
source.add_edge(b, 5)
a.add_edge(b, 15)
a.add_edge(c, 10)
b.add_edge(c, 10)
b.add_edge(sink, 5)
c.add_edge(sink, 10)

# Build the graph
graph = Graph({"Source": source, "A": a, "B": b, "C": c, "Sink": sink})

# Run the step-by-step Edmonds-Karp algorithm
max_flow = graph.edmonds_karp_demo(source, sink)
print(f"\nMaximum Flow from Source to Sink: {max_flow}")
