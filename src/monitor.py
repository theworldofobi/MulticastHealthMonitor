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
    self.last_seq: int | None = None
    self.total_gaps: int = 0

  def process(self, seq_num: int) -> int:
    gap = 0
    if self.last_seq is not None:
      gap = seq_num - self.last_seq - 1
      if gap < 0:
        # out of order or duplicate, will handle later but for now will ignore
        return 0
      self.total_gaps += gap
    
    self.last_seq = seq_num
    return gap
    

def join_multicast():
  pass

def run():
  pass

if __name__ == "__main__":
  run()