#!/usr/bin/env python3
import os
import time
from collections import defaultdict
import binascii

from panda import Panda

from opendbc.car.tesla.teslacan import TeslaCAN
tc = TeslaCAN(None)

# fake
def sec_since_boot():
  return time.time()

def can_printer():
  p = Panda()
  print(f"Connected to id: {p.get_serial()[0]}: {p.get_version()}")
  time.sleep(1)

  p.can_clear(0xFFFF)
  p.set_power_save(0)
  p.set_safety_mode(Panda.SAFETY_TESLA)

  start = sec_since_boot()
  lp = sec_since_boot()
  msgs = defaultdict(list)
  canbus = os.getenv("CAN")
  while True:
    can_recv = p.can_recv()
    for address, dat, src in can_recv:
      if canbus is None or str(src) == canbus:
        msgs[address].append((dat, src))

    if sec_since_boot() - lp > 0.1:
      p.send_heartbeat()
      dd = chr(27) + "[2J"
      dd += "%5.2f\n" % (sec_since_boot() - start)
      for k, v in sorted(msgs.items()):
        last_msg, last_src = v[-1]
        dd += "%d: %s(%6d): %s\n" % (last_src, "%04X(%4d)" % (k, k), len(v), binascii.hexlify(last_msg).decode())
      print(dd)
      lp = sec_since_boot()

    i = int(sec_since_boot() * 100) % 100
    if i % 5 == 0:
      p.can_send_many(tc.create_radar_commands(0, i // 5 % 4))

if __name__ == "__main__":
  can_printer()
