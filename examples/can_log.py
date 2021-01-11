#!/usr/bin/env python3
from time import time
from panda import Panda

def can_logger():
  p = Panda()
  p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)


  while True:
    can_recv = p.can_recv()

    for address, _, dat, src in can_recv:
      if src == 0 and address == 0x225:
        print(f"{time()},{src},{address},{dat.hex()}")

if __name__ == "__main__":
  can_logger()
