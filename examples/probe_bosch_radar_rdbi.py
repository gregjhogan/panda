#!/usr/bin/env python
import time
import struct
from binascii import hexlify
import threading 
from Queue import Queue
from panda import Panda

DEBUG = False
PANDA = Panda()
#ADDR = 0x18DA10F1
ADDR = 0x18DAB0F1
#ADDR = 0x18DAB5F1
QUEUE = Queue()
DONE = False

def main():
  global PANDA
  global ADDR
  global QUEUE
  global DONE
  
  PANDA.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

  can_reader_t = threading.Thread(target=can_reader)
  can_reader_t.daemon = True
  can_reader_t.start()

  # send message to read VIN
  print "request data"
  for byte1 in range(0x100):
    for byte2 in range(0x100):
      #if byte1 != 0xf1:
      #  continue
      # tester present
      
      # tester present
      #msg = "\x02\x3E\x00".ljust(8, "\x00")
      #if DEBUG: print "S:", format(ADDR,'x'), msg.encode("hex")
      #PANDA.can_send(ADDR, msg, 0)
      #QUEUE.get(block=True, timeout=1)
      
      # get data by identifier
      msg = ("\x03\x22{}{}".format(chr(byte1), chr(byte2))).ljust(8, "\x00")
      if DEBUG: print "S:", format(ADDR,'x'), msg.encode("hex")
      PANDA.can_send(ADDR, msg, 0)
      data = QUEUE.get(block=True, timeout=1)
      if len(data) > 0:
        if data != "\x7f\x22\x31":
          #print("{}: {}".format(hex((byte1 << 8)+byte2), data))
          print("{}: {}".format(hex((byte1 << 8)+byte2), hexlify(data)))
        else:
          #print("{}: INVALID".format(hex((byte1 << 8)+byte2)))
          pass

  # exit
  DONE = True
  can_reader_t.join()
  PANDA.close()
  exit(0)

def can_reader():
  global PANDA
  global ADDR
  global QUEUE
  global DONE

  frame = ""
  size = 0
  PANDA.can_clear(0)
  while (1):
    if (DONE): return

    msgs = PANDA.can_recv()
    for ids, ts, dat, bus in msgs:
      if ids != 0x18DAF1B0:
        continue

      if (DEBUG): print "R:", format(ids,'x'), ("".join("%02x" % i for i in dat))
      # 0x0 == single frame and 0x7E == tester present response
      if bus == 0 and len(dat) > 1 and dat[0] >> 4 == 0x0:
        size = (dat[0] & 0xFF)
        frame = dat[1:1+size]
        QUEUE.put(frame)
      # 0x1 == first frame
      elif bus == 0 and ids > 0xFFFF and dat[0] >> 4 == 0x1:
        size = ((dat[0] & 0x0F) << 8) + dat[1]
        frame = dat[2:]
        size -= 6
        # send flow control message to get the rest of the VIN
        msg = "\x30\x00\x00".ljust(8, "\x00")
        if (DEBUG): print "S:", format(ADDR,'x'), msg.encode("hex")
        PANDA.can_send(ADDR, msg, 0)

      # 0x2 == consecutive frame
      elif bus == 0 and ids > 0xFFFF and dat[0] >> 4 == 0x2:
        frame += dat[1:1+size]
        size -= 7
        if size <= 0:
          QUEUE.put(frame)

    time.sleep(0.001)

if __name__ == "__main__":
  main()
