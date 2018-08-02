#!/usr/bin/env python
import time
import datetime
import struct
from binascii import hexlify
import threading
from Queue import Queue
from panda import Panda

DEBUG = True
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

  #msg = ("\x03\x23\x00\x00\x00\x00").ljust(8, "\x00")
  #PANDA.can_send(ADDR, msg, 0)
  #data = QUEUE.get(block=True, timeout=1)
  #print(hexlify(data))
  #exit(0)

  dids = [
    0x48af, # 6248af0c33363830595456434132353000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    0x48f5, # 6248f50154564341320000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    0xa800, # 62a800331800003000c011
    0xa801, # 62a801405640b440aa4080408000000000000000000000960000000000000000000000
    0xa802, # 62a802000000000000
    0xa803, # 62a80342aa0400040000000000000000000000
    0xa806, # 62a8060ad2b700c047f1c04700c42368c029f1258354405154aa6054d38755f00055
    0xa807, # 62a8070a6d6d6d6d6d6d6d6d6d6d
    0xa808, # 62a8080000000000000000000000002600000000930000000000000000000000000000
    0xa80a, # 62a80a00000000000000000000
    0xa80b, # 62a80b0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    0xa815, # 62a81500000000000000000000
    0xa81b, # 62a81b140a0000000000000000
    0xa830, # 62a830000020
    0xa832, # 62a8322000000000000000000000000000000000000000000000000000000000000000
    0xa833, # 62a83300f6ff6f
    0xa840, # 62a840210002000000
    0xa841, # 62a8410004
    0xa842, # 62a84200020000000002022e102e192dc82dd1
    0xa843, # 62a843ffffffffffffffffffffffffffffffff
    0xa845, # 62a84500000960705400390000000020c100900000000000000000000000feff100030200006cc604c00250000000020d900410000000000000000000000feff1009a040000082784c000700000000108888304848480000000000000000feff50092160000a63604c003a0000000020c4c5410000000000000000000000fdf72000c1
    0xa850, # 62a8500f00000000000000000000000000000000000000000000000000000000000000
    0xa851, # 62a851ffe2ffe300000000
    0xa852, # 62a85201019b02f2000000000000
    0xa853, # 62a8530e343134303137313232303033343700000000000000000000000000000000
    0xa854, # 62a854b5000a82000000000000fe0500dd24e000000091110000ff8878000000000000
    0xa855, # 62a8552000098d07060606060000ff00000000009021952e0000ff8878000000000000
    0xa856, # 62a856ffffffffff
    0xa857, # 62a857ffffffffff
    0xa860, # 7f2222
    0xa861, # 7f2222
    0xa8c1, # 62a8c1120000000000000080000000000000000000003f001c00000000331c000000001d00000000331d000000000000000100000001d400000004d400000000000000010000000000a101000000c1000348310000000000000000000000000000000000000000
    0xb000, # 62b0000000000000000000
    0xb001, # 62b0010a04
    0xb002, # 62b002090000
    0xe600, # 62e6003846
    0xe602, # 62e602000000
    0xf100, # 62f10000000000
    0xf110, # 62f1100e3336383031545641413136304d312020
    0xf112, # 62f1120e303433383138303131363033444100000000000000000000000000000000
    0xf116, # 62f11608424d4256434132300000000000000000
    0xf181, # 62f18133363830322d5456412d413136300000
    0xf186, # 62f18601
  ]
  while 1:
    for did in dids:
      did = 0xA8C1
      msg = "\x03\x22{}{}".format(chr(did >> 8), chr(did & 0xFF)).ljust(8, "\x00")
      if DEBUG: print "S:", format(ADDR,'x'), msg.encode("hex")
      PANDA.can_send(ADDR, msg, 0)
      data = QUEUE.get(block=True, timeout=1)
      # print("{}:{}:{}".format(str(datetime.datetime.now()), hex(did), hexlify(data)))
      while data == "\x00" or data == "\x7f\x22\x78":
        data = QUEUE.get(block=True, timeout=1)
      print("{}:{}:{}".format(str(datetime.datetime.now()), hex(did), hexlify(data)))
  exit(0)
  # send message to read data by id
  print "request data"
  for byte1 in range(237, 0x100):
    print byte1
    for byte2 in range(0x100):
      #if byte1 != 0xf1:
      #  continue

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
      while data == "\x00" or data == "\x7f\x22\x78":
        data = QUEUE.get(block=True, timeout=1)
      if len(data) > 0:
        if data != "\x7f\x22\x31":
          #print("{}: {}".format(hex((byte1 << 8)+byte2), data))
          print("{}: {}".format(hex((byte1 << 8)+byte2), hexlify(data)))
        else:
          #print("{}: INVALID {}".format(hex((byte1 << 8)+byte2), hexlify(data)))
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
        # send flow control message
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
