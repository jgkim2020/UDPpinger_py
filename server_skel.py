# server_skel.py
import socket
import time
import threading
import random

server_ip = "127.0.0.1"
server_port = 5005

# class for thread
class serverThread (threading.Thread):
	AVERAGE_DELAY = 100 # ms

	# constructor
	def __init__(self, data, addr):
		threading.Thread.__init__(self)
		self.data = data
		self.addr = addr

	# method for handling incoming packets
	def run(self):
		print ("Server: recv \"" + data.decode('utf-8') + "\"") # receive message
		dropRate = random.uniform(0, 0.4) # unifrom distribution with an average of 0.2
		if (random.random() < dropRate): # drop packet with probability dropRate
			print ("Server: drop \"" + data.decode('utf-8') + "\"") # drop message
		else:
			delay = random.uniform(0, 2*self.AVERAGE_DELAY) # uniform distribution with an average of AVERAGE_DELAY
			time.sleep(delay*0.001) # sleep for delay ms
			sock.sendto(self.data, self.addr) # send datagram to client
			print ("Server: reply \"" + self.data.decode('utf-8') + "\"") # reply message

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # open UDP socket
sock.bind((server_ip, server_port)) # bind socket

while True:
	data, addr = sock.recvfrom(1024) # receive incoming packets
	serverThread(data, addr).start() # create and start new thread
