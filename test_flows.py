from graph import Node, Graph
import pytest

def assert_both(graph, nodes, expected, message):
    max_flow_ek = graph.edmonds_karp(nodes["S"], nodes["T"])
    assert max_flow_ek == expected, "Edmonds-Karp " + message
    max_flow_d = graph.dinic(nodes["S"], nodes["T"])
    assert max_flow_d == expected, "Dinic " + message

def test_simple_graph():
    # Simple graph with a single source-sink path
    nodes = {name: Node(name) for name in ["S", "A", "B", "T"]}
    nodes["S"].add_edge(nodes["A"], 10)
    nodes["A"].add_edge(nodes["B"], 5)
    nodes["B"].add_edge(nodes["T"], 10)

    graph = Graph(nodes)
    assert_both(graph, nodes, 5, "Simple graph maximum flow should be 5")

def test_disconnected_graph():
    # Graph where source and sink are not connected
    nodes = {name: Node(name) for name in ["S", "A", "B", "T"]}
    nodes["S"].add_edge(nodes["A"], 10)
    nodes["B"].add_edge(nodes["T"], 10)

    graph = Graph(nodes)
    assert_both(graph, nodes, 0, "Disconnected graph maximum flow should be 0")

def test_graph_with_cycles():
    # Graph with cycles
    nodes = {name: Node(name) for name in ["S", "A", "B", "C", "T"]}
    nodes["S"].add_edge(nodes["A"], 10)
    nodes["A"].add_edge(nodes["B"], 5)
    nodes["B"].add_edge(nodes["C"], 10)
    nodes["C"].add_edge(nodes["A"], 15)
    nodes["C"].add_edge(nodes["T"], 10)

    graph = Graph(nodes)
    assert_both(graph, nodes, 10, "This Graph with cycles maximum flow should be 10")

def test_multiple_augmenting_paths():
    # Graph with multiple parallel paths
    nodes = {name: Node(name) for name in ["S", "A", "B", "T"]}
    nodes["S"].add_edge(nodes["A"], 10)
    nodes["S"].add_edge(nodes["B"], 5)
    nodes["A"].add_edge(nodes["T"], 10)
    nodes["B"].add_edge(nodes["T"], 10)

    graph = Graph(nodes)
    assert_both(graph, nodes, 15, "Multiple augmenting paths maximum flow should be 15")

def test_zero_capacity_edges():
    # Graph with zero capacity edges
    nodes = {name: Node(name) for name in ["S", "A", "B", "T"]}
    nodes["S"].add_edge(nodes["A"], 10)
    nodes["A"].add_edge(nodes["B"], 0)
    nodes["B"].add_edge(nodes["T"], 10)

    graph = Graph(nodes)
    assert_both(graph, nodes, 0, "Graph with zero capacity edges maximum flow should be 0")

def test_uneven_capacities():
    # Graph with uneven capacities on the same path
    nodes = {name: Node(name) for name in ["S", "A", "B", "T"]}
    nodes["S"].add_edge(nodes["A"], 10000)
    nodes["A"].add_edge(nodes["B"], 1)
    nodes["B"].add_edge(nodes["T"], 10000)

    graph = Graph(nodes)
    assert_both(graph, nodes, 1, "Uneven capacities maximum flow should be 1")

def test_complex_graph():
    # Create nodes for the graph
    nodes = {str(i): Node(str(i)) for i in range(9)}
    nodes["S"] = Node("S")
    nodes["T"] = Node("T")

    # Initialize the graph
    graph = Graph(nodes)

    # Define the source and sink nodes
    source = nodes[str("S")]  # Source is node "10"
    sink = nodes[str("T")]    # Sink is node "9"

    # Add edges as per the example
    # Source edges
    nodes["S"].add_edge(nodes["0"], 5)
    nodes["S"].add_edge(nodes["1"], 10)
    nodes["S"].add_edge(nodes["2"], 15)

    # Middle edges
    nodes["0"].add_edge(nodes["3"], 10)
    nodes["1"].add_edge(nodes["0"], 15)
    nodes["1"].add_edge(nodes["4"], 20)
    nodes["2"].add_edge(nodes["5"], 25)
    nodes["3"].add_edge(nodes["4"], 25)
    nodes["3"].add_edge(nodes["6"], 10)
    nodes["4"].add_edge(nodes["2"], 5)
    nodes["4"].add_edge(nodes["7"], 30)
    nodes["5"].add_edge(nodes["7"], 20)
    nodes["5"].add_edge(nodes["8"], 10)
    nodes["7"].add_edge(nodes["8"], 15)

    # Sink edges
    nodes["6"].add_edge(nodes["T"], 5)
    nodes["7"].add_edge(nodes["T"], 15)
    nodes["8"].add_edge(nodes["T"], 10)

    # Compute and print the max flow using Dinic's algorithm
    # max_flow = graph.dinic(source, sink)
    # print(f"Maximum flow: {max_flow}")
    assert_both(graph, nodes, 30, "Complex Graph maximum flow should be 30")