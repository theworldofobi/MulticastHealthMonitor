import socket
import struct
import json
import argparse

from prometheus_client import start_http_server
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
    

def join_multicast() -> socket.socket:
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(("", MCAST_PORT))
  mreq = struct.pack("4sL", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
  s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
  return s

def run(metrics_port: int = 8000):
  start_http_server(metrics_port)
  print(f"Metrics can be found at http://localhost:{metrics_port}/metrics")

  s: socket.socket = join_multicast()
  detector = GapDetector()

  print(f"Monitor joined {MCAST_GRP}:{MCAST_PORT}")
  while True:
    data, _ = s.recvfrom(1024)
    message = json.loads(data.decode())
    sequence = message["sequence_id"]

    gap = detector.process(sequence)

    packets_received.inc()
    last_sequence_id.set(sequence)

    if gap > 0:
      gaps_detected.inc(gap)
      print(f"[GAP DETECTED] received {sequence} (missing {gap})")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--port", type=int, default=8000)
  args = parser.parse_args()
  run(args.port)
  