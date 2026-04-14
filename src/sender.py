import socket
import json
import time
import argparse

MCAST_GRP = "239.255.0.1"
MCAST_PORT = 9806

def build_socket() -> socket.socket:
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, value=2)
  
  return s

def run():
  pass

if __name__ == "__main__":
  run()