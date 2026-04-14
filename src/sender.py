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

def run(rate_hz: float = 20.0, drop_every: int = 0):
  s: socket.socket = build_socket()
  interval: float = 1.0 / rate_hz
  seq: int = 0
  
  print(f"Sender: {rate_hz} pkt/s --> {MCAST_GRP}:{MCAST_PORT}")
  while True:
    seq += 1
    if drop_every and seq % drop_every == 0:
      print(f"  [simulated drop] skipping seq={seq}")
      time.sleep(interval)
      continue

    payload = json.dumps({
      "sequence_id": seq,
      "timestamp" : time.time()
    }).encode()

    s.sendto(payload, (MCAST_GRP, MCAST_PORT))
    time.sleep(interval)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--rate", type=float, default=20.0)
  parser.add_argument("--drop-every", type=int, default=0)
  args = parser.parse_args()
  run(args.rate, args.drop_every)
