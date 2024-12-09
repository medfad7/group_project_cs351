from __future__ import annotations
from collections import deque
import random
from typing import List, Dict, Optional
import networkx as nx
import matplotlib.pyplot as plt


class Edge:
    def __init__(self, target: Node, capacity: float) -> None:
        self.target = target
        self.capacity = capacity
        self.flow = 0
        self.reverse: Optional[Edge] = None  # Reverse edge reference

    def __repr__(self): return f"Edge to {self.target}: {self.flow} / {self.capacity}"

class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.edges: List[Edge] = []  # List of edges connected to this node

    def add_edge(self, target: Node, capacity: float) -> None:

        forward_edge = Edge(target, capacity)
        reverse_edge = Edge(self, capacity)

        forward_edge.reverse = reverse_edge
        reverse_edge.reverse = forward_edge

        self.edges.append(forward_edge)
        target.edges.append(reverse_edge)

    def __repr__(self): return self.name

class Graph:
    def __init__(self, nodes: Dict[str, Node]) -> None:
        self.nodes = nodes
        self.level = {}  # Stores the level graph for BFS

    def dinic_bfs(self, source: Node, sink: Node) -> bool:
        """
        BFS to construct the level graph and check if a path exists from source to sink.
        """
        self.level = {node: -1 for node in self.nodes.values()}  # Reset levels
        queue = deque([source])
        self.level[source] = 0

        while queue:
            current = queue.popleft()
            for edge in current.edges:
                if self.level[edge.target] == -1 and edge.flow < edge.capacity:  # Not visited and has residual capacity
                    self.level[edge.target] = self.level[current] + 1
                    queue.append(edge.target)

        return self.level[sink] != -1  # True if sink is reachable

    def dinic_dfs(self, current: Node, sink: Node, flow: float) -> float:
        """
        DFS to send flow from source to sink in the level graph.
        """
        if current == sink:
            return flow

        for edge in current.edges:
            residual_capacity = edge.capacity - edge.flow
            if self.level[edge.target] == self.level[current] + 1 and residual_capacity > 0:
                bottleneck_flow = self.dinic_dfs(edge.target, sink, min(flow, residual_capacity))

                if bottleneck_flow > 0:
                    edge.flow += bottleneck_flow
                    edge.reverse.flow -= bottleneck_flow
                    return bottleneck_flow
        return 0
    
    def dinic_dfs_demo(self, current: Node, sink: Node, flow: float) -> tuple[float, List[Node]]:
        """
        DFS to send flow from source to sink in the level graph.
        """
        if current == sink:
            return flow, [current]

        for edge in current.edges:
            residual_capacity = edge.capacity - edge.flow
            if self.level[edge.target] == self.level[current] + 1 and residual_capacity > 0:
                bottleneck_flow, nodes = self.dinic_dfs_demo(edge.target, sink, min(flow, residual_capacity))

                if bottleneck_flow > 0:
                    edge.flow += bottleneck_flow
                    edge.reverse.flow -= bottleneck_flow
                    return bottleneck_flow, [current] + nodes 
        return 0, []

    def dinic(self, source: Node, sink: Node) -> float:
        """
        Dinic's algorithm implementation.
        """
        max_flow = 0

        while self.dinic_bfs(source, sink):  # Construct level graph
            flow = float('inf')
            while flow:
                flow = self.dinic_dfs(source, sink, float('inf'))
                max_flow += flow

        return max_flow
    
    def dinic_demo(self, source: Node, sink: Node) -> float:
        """
        Dinic's algorithm implementation.
        """
        max_flow = 0
        step = 1

        while self.dinic_bfs(source, sink):  # Construct level graph
            print(f"Step {step}")
            print(f"Level Graph", self.level)

            flow = float('inf')
            while flow:
                flow, nodes = self.dinic_dfs_demo(source, sink, float('inf'))
                print(f" Found Flow {flow}", nodes)
                max_flow += flow
            print(f" Stopping Flow reached, new max flow: {max_flow}")

            step += 1

        return max_flow

    def bfs(self, source: Node, sink: Node) -> Optional[Dict[Node, Edge]]:
        """
        Perform BFS to find an augmenting path from source to sink.
        Returns a dictionary mapping each node to the edge used to reach it,
        or None if no path exists.
        """
        parent_map = {}
        queue = deque([source])

        while queue:
            current = queue.popleft()

            for edge in current.edges:
                residual_capacity = edge.capacity - edge.flow
                if edge.target not in parent_map and residual_capacity > 0:
                    parent_map[edge.target] = edge
                    if edge.target == sink:
                        return parent_map
                    queue.append(edge.target)

        return None

    def edmonds_karp(self, source: Node, sink: Node) -> float:
        max_flow = 0

        while True:
            # Find an augmenting path using BFS
            parent_map = self.bfs(source, sink)
            if not parent_map:  # No more augmenting paths
                break

            # Calculate bottleneck capacity (minimum residual capacity on the path)
            path_flow = float('inf')
            current = sink
            while current != source:
                edge = parent_map[current]
                path_flow = min(path_flow, edge.capacity - edge.flow)
                current = edge.reverse.target

            # Augment flow along the path
            current = sink
            while current != source:
                edge = parent_map[current]
                edge.flow += path_flow
                edge.reverse.flow -= path_flow
                current = edge.reverse.target

            # Add path flow to max flow
            max_flow += path_flow

        return max_flow
    
    def plot_graph(self, step: int) -> None:
        """
        Visualizes the graph after each step of augmentation.
        """
        G = nx.DiGraph()  # directed graph

        # Add nodes
        for node in self.nodes.values():
            G.add_node(node.name)

        # Add edges with capacity and flow as labels
        for node in self.nodes.values():
            for edge in node.edges:
                if edge.capacity > 0:
                    flow_label = f"Flow: {-edge.flow}"
                    capacity_label = f"Capacity: {edge.capacity}"
                    G.add_edge(node.name, edge.target.name, label=f"{capacity_label}\n{flow_label}")

        # Draw the graph
        pos = nx.spring_layout(G, seed=1)
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=12, font_weight="bold", arrows=True)
        
        # Edge labels for capacity and flow
        edge_labels = nx.get_edge_attributes(G, "label")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

        plt.title(f"Graph at Step {step}")
        plt.show()

    def edmonds_karp_demo(self, source: Node, sink: Node) -> float:
        max_flow = 0
        step = 1

        while True:
            parent_map = self.bfs(source, sink)
            if not parent_map:
                break

            path_flow = float('inf')
            current = sink
            augmenting_path = []

            while current != source:
                edge = parent_map[current]
                augmenting_path.append((edge.reverse.target.name, current.name))
                path_flow = min(path_flow, edge.capacity - edge.flow)
                current = edge.reverse.target

            augmenting_path.reverse()

            current = sink
            while current != source:
                edge = parent_map[current]
                edge.flow += path_flow
                edge.reverse.flow -= path_flow
                current = edge.reverse.target

            max_flow += path_flow

            print(f"\n=== Augmentation Step {step} ===")
            print(f"Augmenting Path: {' -> '.join(node for node, _ in augmenting_path)} -> {sink.name}")
            print(f"Bottleneck Capacity: {path_flow}")
            print(f"Updated Flows:")

            for node in self.nodes.values():
                for edge in node.edges:
                    if edge.capacity > 0 and edge.flow>0:  # Only print forward edges
                        print(f"  {node.name} -> {edge.target.name} | Capacity: {edge.capacity}, Flow: {edge.flow}")

            self.plot_graph(step)

            step += 1

        return max_flow
    
    def reset_calculated_flows(self):
        #Reset Flows
        for node in self.nodes.values():
            for edge in node.edges:
                edge.flow = 0

    def generate_random_graph(num_nodes: int, num_edges: int, max_edge_capacity: int = 10) -> Graph:
        if num_edges < num_nodes - 1:
            raise ValueError("Number of edges must be at least num_nodes - 1 to ensure connectivity.")

        nodes = {f"Node{i}": Node(f"Node{i}") for i in range(num_nodes)}
        edges = set()
        node_list = list(nodes.values())

        unconnected = set(node_list)
        connected = set()

        current = unconnected.pop()
        connected.add(current)

        while unconnected:
            # Connect a random connected node to an unconnected node
            target = random.choice(list(unconnected))
            capacity = random.randint(1, max_edge_capacity)
            current.add_edge(target, capacity)
            edges.add((current, target))
            unconnected.remove(target)
            connected.add(target)
            current = target  # Move to the newly connected node

        # Step 2: Add additional random edges to meet num_edges
        while len(edges) < num_edges:
            u = random.choice(node_list)
            v = random.choice(node_list)
            if u != v and (u, v) not in edges and (v, u) not in edges:  # Avoid duplicates
                capacity = random.randint(1, max_edge_capacity)
                u.add_edge(v, capacity)
                edges.add((u, v))

        return Graph(nodes)
