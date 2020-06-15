#!/usr/bin/env python3

import os
import sys
import time
from collections import defaultdict
import binascii

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from panda import Panda  # noqa: E402

def kline_test(bus=2):
  # flash panda firmware (with mods) from commit 9cffa74e04a9c46d728162834b80df818dde0375
  p = Panda()
  #p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
  p.set_safety_mode(0x1337)
  p.set_uart_baud(bus, 10400)
  print('wakeup')
  p.kline_wakeup()
  print('start comm')
  p.kline_send(b'\x81\x46\xf0\x81\x38', bus=bus, checksum=False)
  resp = p.kline_ll_recv(8, bus=bus)
  assert resp == b'\x80\xf0\x46\x03\xc1\xda\x8f\xe3'

  # blinker on - left
  print('blinker on - left')
  p.kline_send(b'\x80\x18\xf0\x08\x30\x0a\x05\x00\x00\x00\x00\x00\xcf', bus=bus, checksum=False)
  resp = p.kline_ll_recv(7, bus=bus)
  assert resp == b'\x80\xf0\x18\x02\x70\x0a\x04'
  print("sleep ...")
  time.sleep(1)
  # blinker off
  print('blinker off')
  p.kline_send(b'\x80\x18\xf0\x01\x20\xa9', bus=bus, checksum=False)
  resp = p.kline_ll_recv(6, bus=bus)
  assert resp == b'\x80\xf0\x18\x01\x60\xe9'
  time.sleep(1)
  # blinker on - right
  print('blinker on - right')
  p.kline_send(b'\x80\x18\xf0\x08\x30\x0b\x05\x00\x00\x00\x00\x00\xd0', bus=bus, checksum=False)
  resp = p.kline_ll_recv(7, bus=bus)
  assert resp == b'\x80\xf0\x18\x02\x70\x0b\x05'
  print("sleep ...")
  time.sleep(1)
  # blinker off
  print('blinker off')
  p.kline_send(b'\x80\x18\xf0\x01\x20\xa9', bus=bus, checksum=False)
  resp = p.kline_ll_recv(6, bus=bus)
  assert resp == b'\x80\xf0\x18\x01\x60\xe9'

  # stop comm
  print('stop comm')
  p.kline_send(b'\x80\x18\xf0\x01\x82\x0b', bus=bus, checksum=False)
  resp = p.kline_ll_recv(6, bus=bus)
  assert resp == b'\x80\xf0\x18\x01\xc2\x4b'
  print('done!')

  # 80 18 f0 08 - 30 0a 05 00 00 00 00 00 - cf <- left blinker start
  # 80 18 f0 08 - 30 0b 05 00 00 00 00 00 - d0 <- right blinker start
  # 80 18 f0 01 - 20 - a9 <- blinker stop

  # start communication (fast init format)
  # 81 46 f0 81 38
  # start communication response (extended timing, source and target addr, length byte)
  # 80 f0 46 03 c1 da 8f e3

  # i/o control by local id (blink on - left)
  # 80 18 f0 08 30 0a 05 00 00 00 00 00 cf - write
  # 80 f0 18 02 70 0a 04 - read

  # tester present (no response)
  # 80 18 f0 02 3e 02 ca - write

  # stop diagnostic session (blinker off)
  # 80 18 f0 01 20 a9 - write
  # 80 f0 18 01 60 e9 - read

  # tester present (no response)
  # 80 18 f0 02 3e 02 ca
  # 80 18 f0 02 3e 02 ca

  # stop communication
  # 80 18 f0 01 82 0b - write
  # 80 f0 18 01 c2 4b - read

if __name__ == "__main__":
  kline_test()
