import subprocess
import re
import csv
import os
import time

ENVIRONMENT = "wsl"

DESTINATIONS = {
    "cloudflare_1.1.1.1": "1.1.1.1",
    "google_8.8.8.8": "8.8.8.8",
    "google.com": "google.com"
}

TEST_ROUNDS = 5
FILE_PATH = "../data/automated-network-tests.csv"


def run_ping(destination):
    result = subprocess.run(
        ["ping", "-c", "4", destination],
        capture_output=True,
        text=True
    )

    output = result.stdout

    packet_loss_match = re.search(r"(\d+)% packet loss", output)

    latency_match = re.search(
        r"rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)",
        output
    )

    if packet_loss_match and latency_match:
        return {
            "packet_loss": float(packet_loss_match.group(1)),
            "min_latency": float(latency_match.group(1)),
            "avg_latency": float(latency_match.group(2)),
            "max_latency": float(latency_match.group(3))
        }

    return None


def save_result(destination_name, result, test_number):
    file_exists = os.path.exists(FILE_PATH)

    with open(FILE_PATH, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "environment",
                "test",
                "destination",
                "avg_latency_ms",
                "min_latency_ms",
                "max_latency_ms",
                "packet_loss_percent"
            ])

        writer.writerow([
            ENVIRONMENT,
            test_number,
            destination_name,
            result["avg_latency"],
            result["min_latency"],
            result["max_latency"],
            result["packet_loss"]
        ])


for test_number in range(1, TEST_ROUNDS + 1):
    print(f"\n--- Test round {test_number}/{TEST_ROUNDS} ---")

    for destination_name, destination in DESTINATIONS.items():
        print("Testing", destination_name + "...")

        result = run_ping(destination)

        if result:
            save_result(destination_name, result, test_number)

            print("  Average latency:", result["avg_latency"], "ms")
            print("  Packet loss:", result["packet_loss"], "%")
        else:
            print("  Test failed.")

    if test_number < TEST_ROUNDS:
        time.sleep(2)

print("\nAll test rounds completed.")
print("Results saved to:", FILE_PATH)
