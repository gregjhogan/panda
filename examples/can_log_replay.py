#!/usr/bin/env python3

import os
import sys
import time
from collections import defaultdict
import binascii

from panda import Panda
from tools.lib.logreader import LogReader

# replay a drive to check for safety violations
def replay_drive(lr, p):
  start = time.time()
  start_t = None

  for msg in lr:
    if start_t is None:
      start_t = msg.logMonoTime

    # if msg.which() == 'sendcan':
    #   for canmsg in msg.sendcan:
    #     if canmsg.src == 2:
    #       continue
    #     p.can_send(canmsg.address, canmsg.dat, canmsg.src)
    if msg.which() == 'can':
      msgs = []
      for canmsg in msg.can:
        # no camera
        if canmsg.src == 2 or canmsg.src == 130:
          continue
        # radar tx addrs
        if canmsg.address in (0x389, 0x38D, 0x420, 0x421, 0x483, 0x4A2, 0x50A, 0x5ED, 0x5EE, 0x5EF):
          continue
        # radar tracks (hopefully)
        if canmsg.address >= 0x600 and canmsg.address <= 0x6FF:
          continue
        # convert sent messages to appropriate bus
        bus = canmsg.src if canmsg.src < 128 else canmsg.src - 128
        msgs.append([canmsg.address, None, canmsg.dat, bus])
      tdelta = (msg.logMonoTime - start_t) / 1e9
      tdiff = time.time() - start
      while tdelta > tdiff:
        tdiff = time.time() - start
      p.can_send_many(msgs)
      tlag = tdiff - tdelta
      if tlag >= .0005:
        print(f"lag: {tlag}")

if __name__ == "__main__":
  print("wait for panda ...")
  p = None
  while not p:
    time.sleep(0.1)
    try:
        p = Panda()
        p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
    except:
        pass
      
  lr = LogReader(sys.argv[1])
  replay_drive(lr, p)
