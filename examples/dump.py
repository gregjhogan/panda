#!/usr/bin/env python
import time
import struct
from panda import Panda

if __name__ == "__main__":
  panda = Panda()
  panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

  while (1):
    msgs = panda.can_recv()
    for ids, ts, dat, bus in msgs:
      print "R:", format(ids,'x'), ("".join("%02x" % i for i in dat))
      
      #if bus == 0 and ids == ((addr >> 16 << 16) | (addr << 8 & 0xFFFF) | (addr >> 8 & 0xFF)):
      #if bus == 0 and ids > 0xFFFF
      #if ids == 0xE4 or ids == 0x1DF or ids == 0x1EF or ids == 0x30C or ids == 0x33D or ids == 0x39F:
      #if bus == 129 or bus == 130:
      #  print "R:", bus, "-", format(ids,'x')
    time.sleep(0.001)
