import csv
import os
import statistics
from pathlib import Path
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = PROJECT_DIR / "data" / "automated-network-tests.csv"
RESULTS_DIR = PROJECT_DIR / "results"
GRAPH_PATH = RESULTS_DIR / "latency_comparison.png"

data = {}

with open(FILE_PATH, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        environment = row["environment"]
        destination = row["destination"]
        key = (environment, destination)

        if key not in data:
            data[key] = {
                "averages": [],
                "minimums": [],
                "maximums": [],
                "packet_loss": []
            }

        data[key]["averages"].append(float(row["avg_latency_ms"]))
        data[key]["minimums"].append(float(row["min_latency_ms"]))
        data[key]["maximums"].append(float(row["max_latency_ms"]))
        data[key]["packet_loss"].append(float(row["packet_loss_percent"]))

print("\nNetwork Reliability Analysis")
print("----------------------------")

for (environment, destination), results in data.items():
    average = statistics.mean(results["averages"])
    minimum = min(results["minimums"])
    maximum = max(results["maximums"])
    packet_loss = statistics.mean(results["packet_loss"])

    print(f"\n{environment.upper()} - {destination}")
    print(f"  Average latency: {average:.2f} ms")
    print(f"  Minimum latency: {minimum:.2f} ms")
    print(f"  Maximum latency: {maximum:.2f} ms")
    print(f"  Packet loss: {packet_loss:.2f}%")

RESULTS_DIR.mkdir(exist_ok=True)

destinations = [
    "cloudflare_1.1.1.1",
    "google_8.8.8.8",
    "google.com"
]

environments = ["wsl", "windows"]

x = list(range(len(destinations)))
width = 0.35

plt.figure(figsize=(10, 6))

for i, environment in enumerate(environments):
    averages = []
    lower_errors = []
    upper_errors = []

    for destination in destinations:
        key = (environment, destination)

        if key in data:
            average = statistics.mean(data[key]["averages"])
            minimum = min(data[key]["minimums"])
            maximum = max(data[key]["maximums"])

            averages.append(average)
            lower_errors.append(average - minimum)
            upper_errors.append(maximum - average)
        else:
            averages.append(0)
            lower_errors.append(0)
            upper_errors.append(0)

    positions = [value + (i - 0.5) * width for value in x]

    plt.bar(
        positions,
        averages,
        width,
        yerr=[lower_errors, upper_errors],
        capsize=5,
        label=environment.upper()
    )

plt.xlabel("Destination")
plt.ylabel("Average Latency (ms)")
plt.title("WSL vs Windows Network Latency")
plt.xticks(x, destinations, rotation=15)
plt.legend()
plt.tight_layout()
plt.savefig(GRAPH_PATH, dpi=300)

print("\nGraph saved to:", GRAPH_PATH)
