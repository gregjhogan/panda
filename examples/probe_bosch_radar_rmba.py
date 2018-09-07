#!/usr/bin/env python
import time
import struct
from binascii import hexlify
import threading 
from Queue import Queue
from panda import Panda

DEBUG = True
PANDA = Panda()
QUEUE = Queue()
DONE = False

def main():
  global PANDA
  global QUEUE
  global DONE
  
  PANDA.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

  can_reader_t = threading.Thread(target=can_reader)
  can_reader_t.daemon = True
  can_reader_t.start()

  # send message to change communication control
  print "request part number"
  for id in range(0x00, 0x100):
    addr = 0x18DA00F1 | (id << 8)
    print hex(addr)
    msg = "\x02\x3E\x00".ljust(8, "\x00")
    if DEBUG: print "S:", hex(addr), msg.encode("hex")
    PANDA.can_send(addr, msg, 0)
    try:
      data = QUEUE.get(block=True, timeout=0.1)
      print("[{}] {}".format(hex(addr), hexlify(data)))
    except Exception:
      continue

    # read data by identifier
    msg = "\x03\x22\xf1\x10".ljust(8, "\x00")
    if DEBUG: print "S:", hex(addr), msg.encode("hex")
    PANDA.can_send(addr, msg, 0)
    data = QUEUE.get(block=True, timeout=1)
    # sub function not supported
    if data == "\x7f\x28\x12":
        continue
    print("[{}] {}".format(hex(addr), hexlify(data)))
    #break

  # exit
  DONE = True
  can_reader_t.join()
  PANDA.close()
  exit(0)

def can_reader():
  global PANDA
  global QUEUE
  global DONE

  frame = ""
  size = 0
  PANDA.can_clear(0)
  while (1):
    if (DONE): return

  # exit
  DONE = True
  can_reader_t.join()
  PANDA.close()
  exit(0)

def can_reader():
  global PANDA
  global QUEUE
  global DONE

  frame = ""
  size = 0
  PANDA.can_clear(0)
  while (1):
    if (DONE): return

    msgs = PANDA.can_recv()
    for ids, ts, dat, bus in msgs:
      if ids>>8 != 0x18DAF1:
        continue

      if (DEBUG): print "R:", hex(ids), ("".join("%02x" % i for i in dat))
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
        addr = 0x18DA00F1 | ((ids & 0xFF) << 8)
        msg = "\x30\x00\x00".ljust(8, "\x00")
        if (DEBUG): print "S:", hex(addr), msg.encode("hex")
        PANDA.can_send(0x18DAB0F1, msg, 0)
      # 0x2 == consecutive frame
      elif bus == 0 and ids > 0xFFFF and dat[0] >> 4 == 0x2:
        frame += dat[1:1+size]
        size -= 7
        if size <= 0:
          QUEUE.put(frame)

    time.sleep(0.001)

if __name__ == "__main__":
  main()
