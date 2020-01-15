#!/usr/bin/env python3
from panda import Panda
from pprint import pprint

panda = Panda()
panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

msgs = set()
while True:
  msgs = panda.can_recv()
  for addr, ts, dat, bus in msgs:
    # read also msgs sent by EON on CAN bus 0x80 and filter out the
    # addr with more than 11 bits
    if bus < 4 and addr < 0x800:
      msgs.add(f"{bus}:{addr.rjust(4)}[{len(dat)}]")

  pprint(sorted(msgs))
