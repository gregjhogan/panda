#!/usr/bin/env python3
import os
import sys
import time
import struct
from panda import Panda

DEBUG = os.getenv('DEBUG', False)

def main():
  logfile = sys.argv[1]
  msgs = []
  print(f"open log file {logfile}")
  with open(logfile,'r') as log:
    msg_t, msg_a, msg_d = None, None, None
    log.readline() # skip header
    for line in log:
      line = line.rstrip()
      if not line: continue

      t, analyzer, data = line.split(',', 2)
      if "idf:" in data:
        if msg_t is not None:
          if len(msg_d) == 0:
            print(f"[{msg_t}] {msg_a}: empty!")
          msg = [msg_t, msg_a, msg_d]
          msgs.append(msg)
        msg_t = float(t)
        msg_a = int(data.split(": ")[1], 0)
        msg_d = bytes()
      if data.startswith("Data "):
        msg_d += bytes([int(data.split(": ")[1], 0)])

    print("wait for panda ...")
    p = None
    while not p:
      time.sleep(0.1)
      try:
          p = Panda()
      except:
          pass
    p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

    start_time = time.time()
    print(f"replay log ...")
    for t, addr, dat in msgs:
      t += start_time
      # wait for the correct moment to send the message
      tdiff = time.time() - t
      while (tdiff <= 0):
        tdiff = time.time() - t
      if tdiff > .1: print(f"lagged {tdiff}")

      if addr<<16 > 1<<29 and len(dat) > 8:
        raise Exception(f"addr too high and data too large: {addr_slice} {dat}")
      for i in range(0, len(dat), 8):
        if addr<<16 < 1<<29:
          addr_slice = (addr<<16)+i
          data_slice = dat[i:i+8]
        if DEBUG: print(t, addr_slice, data_slice.hex())
        p.can_send(addr_slice, data_slice, 0)

  print("\nDone!")
  p.close()

if __name__ == "__main__":
  main()
