#!/usr/bin/env python
import time
import struct
import threading 
from panda import Panda

DEBUG = True
PANDA = Panda()
ADDR = 0
VIN = ""
DONE = False

def main():
  global PANDA
  global ADDR
  global VIN
  global DONE
  
  PANDA.set_safety_mode(Panda.SAFETY_ELM327)

  can_reader_t = threading.Thread(target=can_reader)
  can_reader_t.daemon = True
  can_reader_t.start()

  tester_present_t = threading.Thread(target=tester_present)
  tester_present_t.daemon = True
  tester_present_t.start()

  # wait for ECU address to be identified
  print "searching for ECU"
  while (1):
    if (ADDR != 0):
      break
    time.sleep(0.1)

  # send message to read VIN
  print "request VIN"
  msg = "\x02\x09\x02".ljust(8, "\x00")
  print "S:", format(ADDR,'x'), msg.encode("hex")
  PANDA.can_send(ADDR, msg, 0)

  # wait for VIN to be read
  print "read response"
  while (1):
    if (len(VIN) == 17):
      print VIN
      break
    time.sleep(0.1)

  # exit
  DONE = True
  tester_present_t.join()
  can_reader_t.join()
  PANDA.close()
  exit(0)

def tester_present():
  global PANDA
  global DONE

  while(1):
    if (DONE): return

    msg = "\x02\x3E\x00".ljust(8, "\x00")

    # 11 bit address message
    addr = 0x7DF
    if (DEBUG): print "S:", format(addr,'x'), msg.encode("hex")
    PANDA.can_send(addr, msg, 0)

    # 29 bit address message
    addr = 0x18DB33F1
    if (DEBUG): print "S:", format(addr,'x'), msg.encode("hex")
    PANDA.can_send(addr, msg, 0)

    time.sleep(2.0)

def can_reader():
  global PANDA
  global ADDR
  global VIN
  global DONE

  PANDA.can_clear(0)
  while (1):
    if (DONE): return

    msgs = PANDA.can_recv()
    for ids, ts, dat, bus in msgs:
      # 0x0 == single frame and 0x7E == tester present response
      if bus == 0 and len(dat) > 1 and dat[0] >> 4 == 0x0 and dat[1] == 0x7E:
        if (DEBUG): print "R:", format(ids,'x'), ("".join("%02x" % i for i in dat))
        # wait for ECU to respond
        if (ids == 0x18DAF110): ADDR = 0x18DA10F1
        if (ids == 0x7E8): ADDR = 0x7E0

      # 0x1 == first frame
      elif bus == 0 and ids > 0xFFFF and dat[0] >> 4 == 0x1:
        if (DEBUG): print "R:", format(ids,'x'), ("".join("%02x" % i for i in dat))
        VIN += dat[5:]
        # send flow control message to get the rest of the VIN
        msg = "\x30\x00\x00".ljust(8, "\x00")
        if (DEBUG): print "S:", format(ADDR,'x'), msg.encode("hex")
        PANDA.can_send(ADDR, msg, 0)

      # 0x2 == consecutive frame
      elif bus == 0 and ids > 0xFFFF and dat[0] >> 4 == 0x2:
        if (DEBUG): print "R:", format(ids,'x'), ("".join("%02x" % i for i in dat))
        VIN += dat[1:]

    time.sleep(0.001)

if __name__ == "__main__":
  main()
