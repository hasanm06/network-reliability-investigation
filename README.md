# Network Reliability Investigation

## Overview

This project investigates network performance from two environments: Windows and Windows Subsystem for Linux (WSL).

The goal is to determine whether differences in network performance can be observed between Windows and WSL, and to identify where delays may occur across the network.

## Research Question

Does the virtualization and networking layer between Windows and WSL introduce measurable differences in network performance?

To investigate this, the project compares:

- Latency to the home network gateway
- Latency to an external DNS/public network service
- Connectivity to public IP addresses
- DNS lookup performance
- The network path from WSL to Google using traceroute

## Methodology

The investigation used command-line networking tools in both Windows and WSL.

The following measurements were collected:

- Ping tests to measure latency and packet loss
- DNS lookups to measure name-resolution performance
- IP and routing information to identify network interfaces and gateways
- Traceroute to examine the path from WSL to Google
- Repeated tests to make the measurements more reliable

## Tools Used

- Linux / WSL
- Bash
- Windows PowerShell
- ping
- nslookup
- traceroute
- ip
- Git
- CSV data collection

## Network Configuration

The investigation identified two network gateways:

- WSL virtual gateway: `wsl_virtual_gateway`
- Home network gateway: `home_gateway`

WSL was assigned the IP address `wsl_ip`.

The WSL DNS configuration used `wsl_dns_proxy` as its DNS server/proxy, while Windows used the home network gateway `home_gateway` for DNS resolution.

## Results

### Network Latency

| Environment | Destination | Average Latency | Packet Loss |
|---|---|---:|---:|
| WSL | Home network gateway | 8.743 ms | 0% |
| Windows | Home network gateway | 5 ms | 0% |
| WSL | Cloudflare (1.1.1.1) | 8.223 ms | 0% |
| Windows | Cloudflare (1.1.1.1) | 7 ms | 0% |
| WSL | Google (8.8.8.8) | 8.824 ms | 0% |
| WSL | Google.com | 9.939 ms | 0% |

All recorded ping tests successfully received responses with 0% packet loss.

### DNS Performance

WSL DNS lookup times for Google ranged from 32 ms to 50 ms, while Microsoft ranged from 31 ms to 60 ms.

A Windows DNS lookup for Google took 83.5233 ms.

The Windows DNS measurement was only performed once, so it should not be treated as a direct statistical comparison with the repeated WSL measurements.

### Traceroute Findings

The traceroute from WSL to Google reached the destination in 11 hops.

The first hop was the WSL virtual gateway, followed by the home network gateway. The remaining hops represented network infrastructure between the local network and Google.

Two intermediate hops did not respond to the traceroute probes and appeared as `* * *`. However, the traceroute continued successfully and reached Google, so these responses alone do not indicate a network failure.

The measured latency increased from approximately 1 ms at the WSL gateway to approximately 9 ms at the destination.

## Conclusion

The measurements show that both Windows and WSL had stable connectivity during the investigation, with 0% packet loss in the recorded ping tests.

WSL generally showed slightly higher latency than Windows when testing the home network gateway and Cloudflare. However, the differences were small, suggesting that the WSL networking layer introduced some measurable overhead but did not significantly affect connectivity during these tests.

The DNS results also show that DNS resolution was working correctly in WSL. However, because the Windows and WSL DNS measurements used different DNS servers and different numbers of tests, the results cannot be considered a perfectly controlled comparison.

Overall, the investigation demonstrates how basic Linux and networking tools can be used to collect evidence, identify network components, and analyze network performance rather than relying only on how fast the internet feels.

## Project Structure

```text
network-reliability-investigation/
├── data/
│   ├── dns-tests.csv
│   ├── network-tests.csv
│   └── traceroute-google.txt
├── notes/
└── README.md
```

