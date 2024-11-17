from flow_graph import *

# Test Case: Simple Graph with Multiple Augmenting Paths
nodes = {name: Node(name) for name in ["S", "A", "B", "T"]}
nodes["S"].add_edge(nodes["A"], 10)
nodes["S"].add_edge(nodes["B"], 5)
nodes["A"].add_edge(nodes["T"], 10)
nodes["B"].add_edge(nodes["T"], 10)

graph = Graph(nodes)
source = nodes["S"]
sink = nodes["T"]

print(f"Maximum Flow: {graph.edmonds_karp(source, sink)}") 
