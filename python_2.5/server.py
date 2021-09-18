import socket
import sys
import os
import subprocess

# 
def getIps(hosts):
	f = open("hostsToIps.txt", "r")
	ownIp = sys.argv[1]
	dictionary = {}

	for line in f:
		hostName = line.split()[0]
		ip = line.split()[1]
		dictionary[hostName] = ip
	f.close()


	hosts = hosts.replace("[", "")
	hosts = hosts.replace("]", "")
	hosts = hosts.split(",")

	ipString = ""
	print(hosts)
	for host in hosts:
		ipString += dictionary[host]
		ipString += ","
	ipTable = ipString.split(",")
	ipTable.remove(ownIp)
	ipTable.remove('')
	print(ipTable)
	return ipTable

def calculateLatency(ipTable):
	latencyTable = []
	for currIp in ipTable:
		pingOutput = subprocess.check_output("ping -w 1 " + currIp, shell=True).decode()
		pingOutput = pingOutput.split("\n")
		start = pingOutput[1].find("time=") + 5
		end = pingOutput[1].find("ms") - 1
		latencyTable.append(pingOutput[1][start:end])
	return latencyTable

def calculateHops(ipTable):
	hopTable = []
	for currIp in ipTable:
		tracerouteOutput = subprocess.check_output("traceroute " + currIp, shell=True).decode()
		if "!H" in tracerouteOutput:
			hopTable.append("Destination unreachable")
		elif tracerouteOutput.count("*") > 8:
			hopTable.append("Destination unresponsive")
		else:
			hops = len(tracerouteOutput.split("\n")) - 1
			hopTable.append(str(hops))

	return hopTable

def prepareOutput(latencyTable, hopTable, ipTable):
	f = open("hostsToIps.txt", "r")
	dictionary = {}
	for line in f:
		hostName = line.split()[0]
		ip = line.split()[1]
		dictionary[ip] = hostName
	f.close()
	output = ""
	assert(len(latencyTable) == len(hopTable))
	resultCount = len(latencyTable)
	for i in range(resultCount):
		output += dictionary[sys.argv[1]] + " --> " + dictionary[ipTable[i]] + "\n\t" \
		"Latency: " + latencyTable[i] + " ms, Hops: " + hopTable[i] +  ".\n"
	return output

# This is the tool that will produce the results of all the pings and traceroutes.
def trackHosts(hosts):
	ownIp = sys.argv[1]
	ipTable = getIps(hosts)

	latencyTable = calculateLatency(ipTable)
	hopTable = calculateHops(ipTable)

	return prepareOutput(latencyTable, hopTable, ipTable)


# Main
assert(len(sys.argv) == 2)
TCP_IP = sys.argv[1]
TCP_PORT = 7777

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)

conn, addr = sock.accept()

hosts = conn.recv(2048)
hosts = hosts.decode()
output = trackHosts(hosts).encode()

conn.send(output)
sock.close()
print("Tool finished")