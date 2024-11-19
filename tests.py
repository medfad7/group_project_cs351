from .graph import Node, Graph
import pytest

def test_simple_graph():
    # Simple graph with a single source-sink path
    nodes = {name: Node(name) for name in ["S", "A", "B", "T"]}
    nodes["S"].add_edge(nodes["A"], 10)
    nodes["A"].add_edge(nodes["B"], 5)
    nodes["B"].add_edge(nodes["T"], 10)

    graph = Graph(nodes)
    max_flow = graph.edmonds_karp(nodes["S"], nodes["T"])
    assert max_flow == 5, "Simple graph maximum flow should be 5"

def test_disconnected_graph():
    # Graph where source and sink are not connected
    nodes = {name: Node(name) for name in ["S", "A", "B", "T"]}
    nodes["S"].add_edge(nodes["A"], 10)
    nodes["B"].add_edge(nodes["T"], 10)

    graph = Graph(nodes)
    max_flow = graph.edmonds_karp(nodes["S"], nodes["T"])
    assert max_flow == 0, "Disconnected graph maximum flow should be 0"

def test_graph_with_cycles():
    # Graph with cycles
    nodes = {name: Node(name) for name in ["S", "A", "B", "C", "T"]}
    nodes["S"].add_edge(nodes["A"], 10)
    nodes["A"].add_edge(nodes["B"], 5)
    nodes["B"].add_edge(nodes["C"], 10)
    nodes["C"].add_edge(nodes["A"], 15)
    nodes["C"].add_edge(nodes["T"], 10)

    graph = Graph(nodes)
    max_flow = graph.edmonds_karp(nodes["S"], nodes["T"])
    assert max_flow == 5, "This Graph with cycles maximum flow should be 5"

def test_multiple_augmenting_paths():
    # Graph with multiple parallel paths
    nodes = {name: Node(name) for name in ["S", "A", "B", "T"]}
    nodes["S"].add_edge(nodes["A"], 10)
    nodes["S"].add_edge(nodes["B"], 5)
    nodes["A"].add_edge(nodes["T"], 10)
    nodes["B"].add_edge(nodes["T"], 10)

    graph = Graph(nodes)
    max_flow = graph.edmonds_karp(nodes["S"], nodes["T"])
    assert max_flow == 15, "Multiple augmenting paths maximum flow should be 15"

def test_zero_capacity_edges():
    # Graph with zero capacity edges
    nodes = {name: Node(name) for name in ["S", "A", "B", "T"]}
    nodes["S"].add_edge(nodes["A"], 10)
    nodes["A"].add_edge(nodes["B"], 0)
    nodes["B"].add_edge(nodes["T"], 10)

    graph = Graph(nodes)
    max_flow = graph.edmonds_karp(nodes["S"], nodes["T"])
    assert max_flow == 0, "Graph with zero capacity edges maximum flow should be 0"

def test_uneven_capacities():
    # Graph with uneven capacities on the same path
    nodes = {name: Node(name) for name in ["S", "A", "B", "T"]}
    nodes["S"].add_edge(nodes["A"], 10000)
    nodes["A"].add_edge(nodes["B"], 1)
    nodes["B"].add_edge(nodes["T"], 10000)

    graph = Graph(nodes)
    max_flow = graph.edmonds_karp(nodes["S"], nodes["T"])
    assert max_flow == 1, "Uneven capacities maximum flow should be 1"
