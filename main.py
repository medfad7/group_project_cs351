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