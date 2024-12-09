import time
import matplotlib.pyplot as plt
import numpy as np
from graph import Node, Graph

def extract_log_log_equation(log_x, log_y):
    # Check for NaNs or infinite values
    if np.any(np.isnan(log_x)) or np.any(np.isnan(log_y)):
        print("Warning: NaN values found in data")
        return np.nan, np.nan
    
    slope, intercept = np.polyfit(log_x, log_y, 1)
    return slope, intercept

def plot_runtime_vs_metric(sizes, metric_values, karp_runtimes, dinic_runtimes, metric_name):
    # replace non positive values with a small value to avoid log(0)
    metric_values = np.array(metric_values)
    karp_runtimes = np.array(karp_runtimes)
    dinic_runtimes = np.array(dinic_runtimes)

    # Avoid taking log of zero or negative values by replacing them with small values
    metric_values = np.where(metric_values <= 0, 1e-10, metric_values)
    karp_runtimes = np.where(karp_runtimes <= 0, 1e-10, karp_runtimes)
    dinic_runtimes = np.where(dinic_runtimes <= 0, 1e-10, dinic_runtimes)

    # Regular plot
    plt.figure(figsize=(10, 6))
    plt.plot(metric_values, karp_runtimes, label="Edmonds-Karp Runtime", marker='o', color='b')
    plt.plot(metric_values, dinic_runtimes, label="Dinic Runtime", marker='x', color='r')
    plt.xlabel(metric_name)
    plt.ylabel("Runtime (seconds)")
    plt.title(f"Runtime vs {metric_name}")
    plt.grid(True)
    plt.legend()
    plt.show()

    # Log-log plot
    plt.figure(figsize=(10, 6))
    log_metric = np.log(metric_values)
    log_karp = np.log(karp_runtimes)
    log_dinic = np.log(dinic_runtimes)

    plt.scatter(log_metric, log_karp, label="Log Edmonds-Karp", color='b', alpha=0.7)
    slope_karp, intercept_karp = extract_log_log_equation(log_metric, log_karp)
    if not np.isnan(slope_karp):
        plt.plot(log_metric, np.poly1d([slope_karp, intercept_karp])(log_metric), color='b', linestyle='--')

    plt.scatter(log_metric, log_dinic, label="Log Dinic", color='r', alpha=0.7)
    slope_dinic, intercept_dinic = extract_log_log_equation(log_metric, log_dinic)
    if not np.isnan(slope_dinic):
        plt.plot(log_metric, np.poly1d([slope_dinic, intercept_dinic])(log_metric), color='r', linestyle='--')

    plt.xlabel(f"Log({metric_name})")
    plt.ylabel("Log(Runtime)")
    plt.title(f"Log-Log Plot: Runtime vs {metric_name}")
    plt.grid(True)
    plt.legend()

    # Print the linear equations
    print(f"Edmonds-Karp equation: log(runtime) = {intercept_karp:.2f} + {slope_karp:.2f} * log({metric_name})")
    print(f"Dinic equation: log(runtime) = {intercept_dinic:.2f} + {slope_dinic:.2f} * log({metric_name})")

    plt.show()

def measure_runtime_vs_maxflow():
    sizes = []
    maxflow_E_values = []
    karp_runtimes = []
    dinic_runtimes = []

    for size in [10, 100, 1000, 10000, 20000, 30000]:
        g = Graph.generate_random_graph(size, size * 2, 10)
        source = next(iter(g.nodes.values()))
        sink = next(reversed(g.nodes.values()))

        def measure_time(fn):
            start_time = time.time()
            max_flow = fn(source, sink)
            end_time = time.time()
            return end_time - start_time, max_flow

        karp_time, karp_flow = measure_time(g.edmonds_karp)
        g.reset_calculated_flows()
        dinic_time, dinic_flow = measure_time(g.dinic)

        assert karp_flow == dinic_flow

        E = size * 2
        maxflow_E = size * E * E
        sizes.append(size)
        maxflow_E_values.append(maxflow_E)
        karp_runtimes.append(karp_time)
        dinic_runtimes.append(dinic_time)

        print(f"Size: {size}, Max Flow: {karp_flow}, Karp Time: {karp_time:.6f} s, Dinic Time: {dinic_time:.6f} s")

    plot_runtime_vs_metric(sizes, maxflow_E_values, karp_runtimes, dinic_runtimes, "V * E^2")


def measure_runtime_vs_maxflow_second():
    sizes = []
    maxflow_E_values = []
    karp_runtimes = []
    dinic_runtimes = []

    for size in [10, 100, 1000, 10000, 20000, 30000]:
        g = Graph.generate_random_graph(size, size * 2, 10)
        source = next(iter(g.nodes.values()))
        sink = next(reversed(g.nodes.values()))

        def measure_time(fn):
            start_time = time.time()
            max_flow = fn(source, sink)
            end_time = time.time()
            return end_time - start_time, max_flow

        karp_time, karp_flow = measure_time(g.edmonds_karp)
        g.reset_calculated_flows()
        dinic_time, dinic_flow = measure_time(g.dinic)

        assert karp_flow == dinic_flow

        E = size * 2
        maxflow_E = (size ** 2) * E
        sizes.append(size)
        maxflow_E_values.append(maxflow_E)
        karp_runtimes.append(karp_time)
        dinic_runtimes.append(dinic_time)

        print(f"Size: {size}, Max Flow: {karp_flow}, Karp Time: {karp_time:.6f} s, Dinic Time: {dinic_time:.6f} s")

    plot_runtime_vs_metric(sizes, maxflow_E_values, karp_runtimes, dinic_runtimes, "V^2 * E")


measure_runtime_vs_maxflow()
measure_runtime_vs_maxflow_second()
