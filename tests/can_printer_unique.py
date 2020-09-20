#!/usr/bin/env python3

import os
import sys
import time
from collections import defaultdict
import binascii

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from panda import Panda  # noqa: E402

# fake
def sec_since_boot():
  return time.time()

def can_printer():
  p = Panda()
  p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

  start = sec_since_boot()
  lp = sec_since_boot()
  msgs = defaultdict(lambda: defaultdict(lambda: 0))
  umsgs = defaultdict(list)
  canbus = int(os.getenv("CAN", "0"))
  while True:
    can_recv = p.can_recv()
    for address, _, dat, src in can_recv:
      if src == canbus:
        h = dat.hex()
        if h not in msgs[address] and lp - start > 1.0:
          umsgs[address].append(h)
        msgs[address][h] = 1

    if sec_since_boot() - lp > 0.1:
      dd = chr(27) + "[2J"
      dd += "%5.2f\n" % (sec_since_boot() - start)
      for k in sorted(umsgs.keys()):
        for v in umsgs[k]:
          dd += f"{k:X}({k:6d}) {v}\n"
      print(dd)
      lp = sec_since_boot()

if __name__ == "__main__":
  can_printer()
