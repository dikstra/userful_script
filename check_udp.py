import socket
import threading
import time
import struct
import sys

def udp_sender(ip,port):
    try:
        ADDR = (ip,port)
        sock_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        msg="abcd"
        sock_udp.sendto(msg.encode(),ADDR)
        sock_udp.close()
        print "connect"
    except socket.error as e:
        print("Error creating socket: %s" % e)
        sys.exit(1)

def checker_udp(ip,port):
    thread_udp = threading.Thread(target=udp_sender,args=(ip,port))
    thread_udp.daemon= True
    thread_udp.start()
    thread_udp.join()
 
 
if __name__ == '__main__':
    ips = ['172.19.31.31','172.19.31.32','172.19.31.33','172.19.31.34']
    port = r'5683'
    for ip in ips:
        checker_udp(ip,int(port))
    #checker_udp(ip,int(port))
    #print ip
    #udp_sender(ip,port)
