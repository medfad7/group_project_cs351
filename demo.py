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

# nodes = {str(i): Node(str(i)) for i in range(9)}
# nodes["S"] = Node("S")
# nodes["T"] = Node("T")

# # Initialize the graph
# graph = Graph(nodes)

# # Define the source and sink nodes
# source = nodes[str("S")]  # Source is node "10"
# sink = nodes[str("T")]    # Sink is node "9"

# # Source edges
# nodes["S"].add_edge(nodes["0"], 5)
# nodes["S"].add_edge(nodes["1"], 10)
# nodes["S"].add_edge(nodes["2"], 15)

# # Middle edges
# nodes["0"].add_edge(nodes["3"], 10)
# nodes["1"].add_edge(nodes["0"], 15)
# nodes["1"].add_edge(nodes["4"], 20)
# nodes["2"].add_edge(nodes["5"], 25)
# nodes["3"].add_edge(nodes["4"], 25)
# nodes["3"].add_edge(nodes["6"], 10)
# nodes["4"].add_edge(nodes["2"], 5)
# nodes["4"].add_edge(nodes["7"], 30)
# nodes["5"].add_edge(nodes["7"], 20)
# nodes["5"].add_edge(nodes["8"], 10)
# nodes["7"].add_edge(nodes["8"], 15)

# # Sink edges
# nodes["6"].add_edge(nodes["T"], 5)
# nodes["7"].add_edge(nodes["T"], 15)
# nodes["8"].add_edge(nodes["T"], 10)


max_flow = graph.edmonds_karp_demo(source, sink)
print(f"\nMaximum Flow from Source to Sink: {max_flow}")
graph.reset_calculated_flows()
print()
print("Dinic's Algorithm:")
max_flow = graph.dinic_demo(source, sink)
print(f"\nMaximum Flow from Source to Sink: {max_flow}")
graph.plot_graph(2)
