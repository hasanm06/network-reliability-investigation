import csv
import os
import statistics
import matplotlib.pyplot as plt

FILE_PATH = "../data/automated-network-tests.csv"
RESULTS_DIR = "../results"
GRAPH_PATH = os.path.join(RESULTS_DIR, "latency_comparison.png")

data = {}

with open(FILE_PATH, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        destination = row["destination"]
        latency = float(row["avg_latency_ms"])

        if destination not in data:
            data[destination] = []

        data[destination].append(latency)

print("\nNetwork Reliability Analysis")
print("----------------------------")

for destination, latencies in data.items():
    average = statistics.mean(latencies)
    minimum = min(latencies)
    maximum = max(latencies)

    print(f"\n{destination}")
    print(f"  Average latency: {average:.2f} ms")
    print(f"  Minimum latency: {minimum:.2f} ms")
    print(f"  Maximum latency: {maximum:.2f} ms")

os.makedirs(RESULTS_DIR, exist_ok=True)

destinations = list(data.keys())
averages = [statistics.mean(data[d]) for d in destinations]

plt.figure(figsize=(9, 5))
plt.bar(destinations, averages)
plt.xlabel("Destination")
plt.ylabel("Average Latency (ms)")
plt.title("Average Network Latency by Destination")
plt.xticks(rotation=15)
plt.tight_layout()

plt.savefig(GRAPH_PATH, dpi=300)

print("\nGraph saved to:", GRAPH_PATH)
