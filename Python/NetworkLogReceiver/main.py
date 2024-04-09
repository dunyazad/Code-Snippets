import socket
import struct  # Import the struct module for packing

# Multicast group (must be a valid multicast group address)
MULTICAST_GROUP = '239.255.0.1'

# Port to listen on
PORT = 1234

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port
sock.bind(('0.0.0.0', PORT))

# Tell the operating system to add the socket to the multicast group
group = socket.inet_aton(MULTICAST_GROUP)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive and process incoming messages
while True:
    data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
    print("Received message:", data.decode())
