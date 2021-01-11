#!/usr/bin/env python3

import os
import sys
import time
import binascii

from tools.lib.logreader import MultiLogIterator
from tools.lib.route import Route

def replay_drive(lr, f):
  f.write("time,addr,bus,data\n")
  start_t = None

  for msg in lr:
    if start_t is None and msg.which() != 'initData':
      start_t = msg.logMonoTime

    if msg.which() == 'can':
      tdelta = (msg.logMonoTime - start_t) / 1e9
      for canmsg in msg.can:
        # TODO: adjust time of each message appropriately (whole group is not at the same time)
        f.write(f"{tdelta},{canmsg.address},{canmsg.src},{canmsg.dat.hex()}\n")

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("usage: can_log_to_csv.py path/to/rlog.bz2")
    sys.exit(1)
  route = sys.argv[1]
  r = Route(route)
  lr = MultiLogIterator(r.log_paths(), wraparound=False)
  f = open(f"{route}.csv", "w")
  replay_drive(lr, f)
