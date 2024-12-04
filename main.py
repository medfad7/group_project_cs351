import time
import matplotlib.pyplot as plt
from graph import Node, Graph
from test_flows import test_complex_graph, test_simple_graph

def measure_runtime_vs_maxflow_E():
    # Lists to store graph sizes, computed max flow * E values, and runtimes
    sizes = []
    maxflow_E_values = []
    karp_runtimes = []
    dinic_runtimes = []

    # Test on various sizes of graphs
    for size in [10, 100, 1000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]:
        # Generate the random graph with `size` nodes and `size*2` edges
        g = Graph.generate_random_graph(size, size * 2, 10)
        source = next(iter(g.nodes.values()))  # Start node
        sink = next(reversed(g.nodes.values()))  # End node
        
        # Measure runtime
        def measure_time(fn):
            start_time = time.time()
            max_flow = fn(source, sink)
            end_time = time.time()
            return end_time - start_time, max_flow
        
        karp_time, karp_flow = measure_time(g.edmonds_karp)
        g.reset_calculated_flows()
        dinic_time, dinic_flow = measure_time(g.dinic)

        assert karp_flow == dinic_flow

        E = size * 2  # Number of edges
        maxflow_E = karp_flow * E * E  # max flow * number of edges
        
        # Store the data
        sizes.append(size)
        maxflow_E_values.append(maxflow_E)
        karp_runtimes.append(karp_time)
        dinic_runtimes.append(dinic_time)
        
        # Print the result for the current graph
        print(f"Size: {size}, Max Flow: {karp_flow}, Karp Time: {karp_time:.16f} s, Dinic Time: {dinic_time:.16f} s")

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(maxflow_E_values, karp_runtimes, label="Runtime vs Max Flow * E^2", marker='o', color='b')
    plt.xlabel("Max Flow * E^2")
    # plt.ylabel("Runtime (seconds)")
    plt.title("Runtime vs Max Flow * E for Edmonds-Karp Algorithm")
    plt.grid(True)
    plt.legend()
    plt.show()

# Run the function to measure runtime and plot
measure_runtime_vs_maxflow_E()

# test_complex_graph()