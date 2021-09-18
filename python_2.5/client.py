import socket
import sys
import time

# This function returns a list of all the ips that must be used.
def hostsToIps(hosts):
	f = open("hostsToIps.txt", "r")
	dictionary = {}

	for line in f:
		hostName = line.split()[0]
		ip = line.split()[1]
		dictionary[hostName] = ip
	f.close()

	hosts = hosts.replace("[", "")
	hosts = hosts.replace("]", "")
	hosts = hosts.split(",")

	ipTable = []
	for host in hosts:
		ipTable.append(dictionary[host])

	return ipTable


# Main
assert(len(sys.argv) == 2)

TCP_IPS = hostsToIps(sys.argv[1])
TCP_PORT = 7777
socketArray = []
count = len(TCP_IPS)
encodedMessage = sys.argv[1].encode()

for i in range(count):
	socketArray.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
	socketArray[i].connect((TCP_IPS[i], TCP_PORT))
	socketArray[i].send(encodedMessage)
	decodedReceivedMessage = socketArray[i].recv(2048).decode()
	socketArray[i].close()
	print(decodedReceivedMessage)