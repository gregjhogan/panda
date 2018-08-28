#!/usr/bin/env python
import time
import struct
import threading
from panda import Panda

DEBUG = True
PANDA = Panda()
BUS = 0
DONE = False

def main():
  global PANDA
  global DONE
  
  PANDA.set_safety_mode(Panda.SAFETY_ELM327)

  can_reader_t = threading.Thread(target=can_reader)
  can_reader_t.daemon = True
  can_reader_t.start()

  time.sleep(1)

  msg = "\x02\x3E\x00".ljust(8, "\x00")
  for id in range(0x00, 0x100):
    addr = 0x18DA00F1 | (id << 8)
    # if (DEBUG): print "S:", format(addr,'x'), msg.encode("hex")
    PANDA.can_send(addr, msg, BUS)

  time.sleep(10)

  # exit
  DONE = True
  can_reader_t.join()
  PANDA.close()
  exit(0)

def can_reader():
  global PANDA
  global DONE

  PANDA.can_clear(0)
  while (1):
    if (DONE): return

    msgs = PANDA.can_recv()
    for ids, ts, dat, bus in msgs:
      #print hex(ids)
      if bus == BUS and ids > 0xFFFF:
        if (DEBUG): print "R:", format(ids,'x'), ("".join("%02x" % i for i in dat))
    time.sleep(0.001)

if __name__ == "__main__":
  main()
