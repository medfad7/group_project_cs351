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
