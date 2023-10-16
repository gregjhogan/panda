#!/usr/bin/env python3
import time
from panda import Panda

p = Panda()
p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

# send on B-CAN
ADDR = 0x89

# flash blinkers (blinks until door is opened)
# 0.00 0 0x89 0003000000000000
# 0.03 0 0x89 0001000000000000
# 0.04 0 0x89 0001000000000000
# 0.04 0 0x89 0001000000000000
# 0.89 0 0x89 1001000000000000
# 0.04 0 0x89 1001000000000000
# 0.04 0 0x89 1001000000000000
# 0.42 0 0x89 0001000000000000
# 0.03 0 0x89 0001000000000000
# 0.04 0 0x89 0001000000000000
p.can_send(ADDR, b'\x00\x03\x00\x00\x00\x00\x00\x00', 0, 0)
for _ in range(3):
  time.sleep(0.03)
  p.can_send(ADDR, b'\x00\x01\x00\x00\x00\x00\x00\x00', 0, 0)
time.sleep(0.85)
for _ in range(3):
  time.sleep(0.03)
  p.can_send(ADDR, b'\x10\x01\x00\x00\x00\x00\x00\x00', 0, 0)
time.sleep(0.35)
for _ in range(3):
  time.sleep(0.03)
  p.can_send(ADDR, b'\x00\x01\x00\x00\x00\x00\x00\x00', 0, 0)

# # unlock doors (two blinks, doesn't unlock when sent on B-CAN)
# # 0.00 0 0x89 0003000000000000
# # 0.03 0 0x89 0001000000000000
# # 0.04 0 0x89 0001000000000000
# # 0.03 0 0x89 0001000000000000
# # 0.89 0 0x89 4001000000000000
# # 0.04 0 0x89 4001000000000000
# # 0.04 0 0x89 4001000000000000
# # 0.41 0 0x89 0001000000000000
# # 0.04 0 0x89 0001000000000000
# # 0.04 0 0x89 0001000000000000
# p.can_send(ADDR, b'\x00\x03\x00\x00\x00\x00\x00\x00', 0, 0)
# for _ in range(3):
#   time.sleep(0.03)
#   p.can_send(ADDR, b'\x00\x01\x00\x00\x00\x00\x00\x00', 0, 0)
# time.sleep(0.85)
# for _ in range(3):
#   time.sleep(0.03)
#   p.can_send(ADDR, b'\x40\x01\x00\x00\x00\x00\x00\x00', 0, 0)
# time.sleep(0.35)
# for _ in range(3):
#   time.sleep(0.03)
#   p.can_send(ADDR, b'\x00\x01\x00\x00\x00\x00\x00\x00', 0, 0)

# # lock doors (one blink, doesn't lock when sent on B-CAN)
# # 0.00 0 0x89 0003000000000000
# # 0.03 0 0x89 0001000000000000
# # 0.03 0 0x89 0001000000000000
# # 0.04 0 0x89 0001000000000000
# # 0.89 0 0x89 8001000000000000
# # 0.04 0 0x89 8001000000000000
# # 0.03 0 0x89 8001000000000000
# # 0.44 0 0x89 0001000000000000
# # 0.04 0 0x89 0001000000000000
# # 0.03 0 0x89 0001000000000000
# p.can_send(ADDR, b'\x00\x03\x00\x00\x00\x00\x00\x00', 0, 0)
# for _ in range(3):
#   time.sleep(0.03)
#   p.can_send(ADDR, b'\x00\x01\x00\x00\x00\x00\x00\x00', 0, 0)
# time.sleep(0.85)
# for _ in range(3):
#   time.sleep(0.03)
#   p.can_send(ADDR, b'\x80\x01\x00\x00\x00\x00\x00\x00', 0, 0)
# time.sleep(0.35)
# for _ in range(3):
#   time.sleep(0.03)
#   p.can_send(ADDR, b'\x00\x01\x00\x00\x00\x00\x00\x00', 0, 0)
