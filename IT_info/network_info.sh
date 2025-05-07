#!/bin/bash

echo "===== Local IP Address Information ====="
ip a || ifconfig

echo
echo "===== Target IP Address and DNS Resolution ====="
read -p "Enter the hostname or URL to analyze (e.g., www.example.com): " hostname
echo "Pinging $hostname..."
ping -c 4 $hostname

echo
echo "Resolving DNS details for $hostname..."
nslookup $hostname || dig $hostname

echo
echo "===== Data Packets and Frames (tcpdump for 5 seconds) ====="
echo "Capturing network traffic for 5 seconds on default interface..."
sudo tcpdump -i any -c 50 > tcpdump_output.txt
cat tcpdump_output.txt

echo
echo "===== Traceroute to Target ====="
echo "Tracing route to $hostname..."
traceroute $hostname || tracert $hostname

echo
echo "===== Protocols and Active Connections ====="
echo "Active network connections (TCP/UDP):"
netstat -tuln || ss -tuln

echo
echo "===== Data Link and Physical Layer Information ====="
echo "Data link type and interface details:"
ip link show
echo
echo "For wireless interfaces (if applicable):"
iwconfig || echo "No wireless interfaces found."

echo
echo "===== Physical Transmission Method ====="
echo "Checking physical transmission (Wi-Fi or Ethernet)..."
ethtool $(ip route get 1.1.1.1 | awk '{print $5}') 2>/dev/null || echo "Could not determine physical link details."

echo
echo "===== Hops and Latency ====="
echo "Traceroute summary:"
traceroute $hostname || tracert $hostname

