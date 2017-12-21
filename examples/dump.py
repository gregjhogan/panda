#!/usr/bin/env python
import time
import struct
from panda import Panda

if __name__ == "__main__":
  panda = Panda()
  # panda.set_safety_mode(Panda.SAFETY_ELM327)

  # panda.can_clear(0)
  # time.sleep(1.0)
  for z in range(0,3):
    addr = 0x18DBEFF1
    msg = "\x02\x3E\x00".ljust(8, "\x00")
    #print "S:", format(addr,'x'), msg.encode("hex")
    #panda.can_send(addr, msg, 0)
    while (1):
      msgs = panda.can_recv()
      for ids, ts, dat, bus in msgs:
        #if bus == 0 and ids == ((addr >> 16 << 16) | (addr << 8 & 0xFFFF) | (addr >> 8 & 0xFF)):
        if bus == 0 and ids > 0xFFFF:
          print "R:", format(ids,'x'), ("".join("%02x" % i for i in dat))
      time.sleep(0.01)

  print "done"
