import time
import matplotlib.pyplot as plt
from graph import Graph  # Assuming the Graph and other classes are already defined

def measure_runtime_vs_maxflow_E():
    # Lists to store graph sizes, computed max flow * E values, and runtimes
    sizes = []
    maxflow_E_values = []
    runtimes = []

    # Test on various sizes of graphs
    for size in [10, 100, 1000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]:
        # Generate the random graph with `size` nodes and `size*2` edges
        graph = Graph.generate_random_graph(size, size * 2, 10)
        source = next(iter(graph.nodes.values()))  # Start node
        sink = next(reversed(graph.nodes.values()))  # End node
        
        # Measure runtime
        start_time = time.time()
        max_flow = graph.edmonds_karp(source, sink)
        end_time = time.time()
        
        runtime = end_time - start_time
        E = size * 2  # Number of edges
        maxflow_E = max_flow * E * E  # max flow * number of edges
        
        # Store the data
        sizes.append(size)
        maxflow_E_values.append(maxflow_E)
        runtimes.append(runtime)
        
        # Print the result for the current graph
        print(f"Size: {size}, Max Flow: {max_flow}, Time: {runtime:.16f} seconds")

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(maxflow_E_values, runtimes, label="Runtime vs Max Flow * E^2", marker='o', color='b')
    plt.xlabel("Max Flow * E^2")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime vs Max Flow * E for Edmonds-Karp Algorithm")
    plt.grid(True)
    plt.legend()
    plt.show()

# Run the function to measure runtime and plot
measure_runtime_vs_maxflow_E()


# Create Node instances
a = Node('a')
b = Node('b')
c = Node('c')
d = Node('d')
e = Node('e')
f = Node('f')

# Add edges
a.add_edge(f, 4)
a.add_edge(e, 1)
a.add_edge(b, 5)

b.add_edge(a, 5)
b.add_edge(c, 2)

c.add_edge(b, 2)
c.add_edge(f, 1)
c.add_edge(d, 6)
c.add_edge(e, 1)

d.add_edge(c, 6)
d.add_edge(e, 3)

e.add_edge(d, 3)
e.add_edge(c, 1)
e.add_edge(a, 1)

f.add_edge(c, 1)
f.add_edge(a, 4)

# Create the Graph instance
nodes = {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f}
g = Graph(nodes)


def stoer_wagner_min_cut(G: Graph) -> int:
    min_cut = float('inf')

    while len(G.nodes) > 1:
        cut = min_cut_phase(G)
        if cut < min_cut:
            min_cut = cut

    return min_cut


def min_cut_phase(G: Graph) -> int:
    # Initialize the supernode
    supernode = {next(iter(G.nodes.values()))}
    supernode_neighbors = {
        node: weight
        for node, weight in next(iter(G.nodes.values())).edges.items()
    }

    # Start with the most connected vertex
    most_connected_vertex = get_most_connected_vertex(supernode_neighbors)

    # Expand supernode until it contains all but one of the nodes
    while len(supernode_neighbors) > 1:
        # Add the most connected vertex to the supernode
        most_connected_vertex = get_most_connected_vertex(supernode_neighbors)
        supernode_neighbors.pop(most_connected_vertex)

        supernode.add(most_connected_vertex)

        for neighbor, weight in most_connected_vertex.edges.items():
            if neighbor in supernode:
                continue
            supernode_neighbors[neighbor] = (
                supernode_neighbors.get(neighbor, 0) + weight
            )

    # Merge s and t
    s = most_connected_vertex
    t, cut_weight = next(iter(supernode_neighbors.items()))

    print(f"Found s-t mincut with weight {cut_weight}")

    # Merge edges of t into s
    for neighbor, weight in t.edges.items():
        if neighbor == s:
            continue
        neighbor.edges[s] = neighbor.edges.get(s, 0) + weight
        del neighbor.edges[t]
        s.edges[neighbor] = s.edges.get(neighbor, 0) + weight

    del s.edges[t]
    del G.nodes[t.name]

    # Rename s to include t
    s.name += t.name
    if len(G.nodes) > 1:
        print(
            f"Merging {s.name} with {t.name} =>",
            " ".join(node.name for node in G.nodes.values()),
        )

    return cut_weight


def get_most_connected_vertex(supernode_neighbors: dict) -> Node:
    return max(supernode_neighbors, key=supernode_neighbors.get)


print(stoer_wagner_min_cut(g))