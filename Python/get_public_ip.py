import socket

public_ip = socket.gethostbyname(socket.gethostname())
print(public_ip)

