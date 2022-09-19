#!/usr/bin/env python3

import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from panda import Panda  # noqa: E402

print("[INIT]")
p = Panda()
p.set_safety_mode(Panda.SAFETY_ALLOUTPUT, param=1)

print("[SEND WAKEUP]")
# some ECUs (e.g. BSM radar) quickly go to sleep after powering up
# these ECUs wake back up if they notice that the ignition is on
# (sending just one message doesn't work)
msg_addr = 0x541
msg_dat = b"\x00\x00\x00\x00\x00\x00\x00\x04"
msg_bus = 0
for i in range(10):
  # CGW1.CF_Gway_Ign1 = 1
  p.can_send(msg_addr, msg_dat, msg_bus)
  print(hex(msg_addr), f"0x{msg_dat.hex()}")
  time.sleep(.1)

print("[DONE]")
