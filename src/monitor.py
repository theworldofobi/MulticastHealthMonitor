import socket
import struct
import json
import argparse

from prometheus_client import start_wsgi_server
from src.exporter import packets_received, gaps_detected, last_sequence_id

MCAST_GRP = "239.255.0.1"
MCAST_PORT = 9806

class GapDetector:

  def __init__(self):
    pass

  def process(self):
    pass

def join_multicast():
  pass

def run():
  pass

if __name__ == "__main__":
  run()