from prometheus_client import Counter, Gauge

packets_received = Counter(
  "multicast_packets_received_total",
  "total number of multicast packets received"
)

gaps_detected = Counter(
  "multicast_sequence_gaps_total",
  "total number of missing sequence IDs detected"
)

last_sequence_id = Gauge(
  "multicast_last_sequence_id",
  "the most recently received sequence ID"
)
