#!/usr/bin/env python
import time
import struct
from panda import Panda

messages = {
  0x7e0: {
    '\x01\x3e':     ['\x01\x7e'],
    '\x02\x09':     ['\x06\x49\x00\x55\x40\x00\x00'],
    '\x02\x09\x02': ['\x10\x14\x49\x02\x01''2T3'],
    '\x30':         ['\x21''DFREV4F','\x22''W292720']
  }
}

if __name__ == "__main__":
  panda = Panda()
  panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

  while (1):
    msgs = panda.can_recv()
    for id, ts, dat, bus in msgs:
      print "-->", format(id,'x'), ("".join("%02x" % i for i in dat))

      for resp in messages.get(id, {}).get(str(dat).rstrip('\x00'), []):
        rid = id + 8
        rmsg = resp.ljust(8,'\x00')
        print "<--", format(rid,'x'), rmsg.encode('hex')
        panda.can_send(rid, rmsg, bus)

    time.sleep(0.001)
