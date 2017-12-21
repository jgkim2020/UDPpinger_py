# client_skel.py
import socket
import sys
import getopt
import time

server_ip = "127.0.0.1"
server_port = 5005
timeout = 1000 # ms
message = "Ping"
PING_MAX = 10 # number of pings to send

try:
    options, arguments = getopt.getopt(sys.argv[1:], "c:p:w:") # get options and corresponding arguments
except getopt.GetoptError as errorMsg: # exception handling when error occurs within try block
    print (str(errorMsg)) # print error message
    print ("option error")
    sys.exit(1) # terminate script

try:
    argumentCount = 0 # track whether option -c -p is included
    for option, argument in options: # go through options and corresponding arguments
        if (option == "-c"): # server IP address option
            server_ip = argument
            argumentCount += 1
        elif (option == "-p"): # server port number option
            server_port = int(argument)
            argumentCount += 1
        elif (option == "-w"): # timeout option
            timeout = int(argument)

    if (argumentCount != 2): # if -c, -p options does not exist
        print ("option -c -p both required") # print error message
        sys.exit(1) # terminate script
except: # exception handling when error occurs within try block
    print ("option error")
    sys.exit(1) # terminate script

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # open UDP socket
sock.settimeout(0.0) # non-blocking mode

rrtMean = 0
rrtCount = 0
for sequence in range(PING_MAX): # send PING_MAX pings one at a time
    sock.sendto((message + " " + str(sequence)).encode(), (server_ip, server_port)) # send message
    start = time.time() # record send time
    hasReceived = 0 # flag raised upon receiving ping with appropriate sequence

    # run until timeout or ping with appropriate sequence has been received (polling)
    while (time.time() - start < timeout*0.001 and hasReceived == 0):
        try:
            data, addr = sock.recvfrom(1024) # (non-blocking mode)
            end = time.time() # record receive time
            # if ping with appropriate sequence received (sequence match)
            if (int(data.decode('utf-8')[5:]) == sequence):
                rrt = end - start # find RRT (receive time - send time)
                rrtMean += rrt
                rrtCount += 1
                print ("Client: recv \"" + data.decode('utf-8') + "\", RRT: " + str(round(rrt*1000)) + "ms") # display message
                hasReceived = 1 # raise flag
        except socket.error: # if socket is empty (error occurred at sock.recvfrom)
            pass # do nothing

    if (hasReceived == 0): # if flag has not been raised
        print ("Client: timeout \"" + message + " " + str(sequence) + "\"") # display timeout message

# display ping statistics
print("Ping sent: " + str(PING_MAX) + ", Ping received: " + str(rrtCount) + ", Ping timeout: " + str(PING_MAX - rrtCount))
if (rrtCount != 0):
    print("average RRT: " + str(round(rrtMean/rrtCount*1000)) + "ms")
else: # if all pings are timeout
    print("average RRT: undefined (0 Ping recv)")

sock.close() # close UDP socket
