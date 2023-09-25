import netifaces
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

s.bind(('', 0))

def broadcast_discovery(addr):
#    print(addr)
    s.sendto(b"HELLO SD-WiFi", (addr, 1729))


for iface in  netifaces.interfaces():
#    print(iface)
#    print(netifaces.ifaddresses(iface))
    items = netifaces.ifaddresses(iface)
    for key in netifaces.ifaddresses(iface):
        addresses = items[key]
        for address in addresses:
#            print(address)
            if "broadcast" in address:
                target = address["broadcast"]
                if ":" not in target:
                    broadcast_discovery(target)


while True:
    data, address = s.recvfrom(1024)
#    print(data)
    if b"SD-WiFi" in data:
        ip = address[0]
        print("http://%s/ %s" % (ip, data.decode()))