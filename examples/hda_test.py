#!/usr/bin/env python3

import sys
from time import sleep
from panda import Panda

ADDR = 0x225
BUS = 2

def start(idx):
  #msg = [ADDR, b"\x00\x00\x00\x00\x80\x12\x00\x1c", BUS]
  msg = [ADDR, b"\x00\x00" + bytes([idx]) + b"\x00\xa0\x12\x00\x1c", BUS]
  print(*msg)
  p.can_send(*msg)
  sleep(0.04)
  p.can_send(*msg)
  sleep(0.04)
  p.can_send(*msg)
  idx += 1
  sleep(1)

  # msg = [ADDR, b"\x00\x00" + bytes([idx]) + b"\x00\xa0\x10\x00\x20", BUS]
  # print(*msg)
  # p.can_send(*msg)
  # sleep(0.04)
  # p.can_send(*msg)
  # sleep(0.04)
  # p.can_send(*msg)
  # idx += 1

  return idx

def stop(idx):
  msg = [ADDR, b"\x00\x00" + bytes([idx]) + b"\x00\x00\x02\x00\x1c", BUS]
  print(*msg)
  p.can_send(*msg)
  sleep(0.04)
  p.can_send(*msg)
  sleep(0.04)
  p.can_send(*msg)
  idx += 1
  sleep(1)

  return idx

def speed_limit_55_mph(idx):
  # #msg = [ADDR, b"\x00\x00" + bytes([idx]) + b"\x40\x20\x32\x00\x1c", BUS]
  # msg = [ADDR, b"\x00\x00" + bytes([idx]) + b"\x40\x20\x52\x00\x1c", BUS]
  # print(*msg)
  # p.can_send(*msg)
  # sleep(0.04)
  # p.can_send(*msg)
  # sleep(0.04)
  # p.can_send(*msg)
  # idx += 1
  # sleep(2)

  # msg = [ADDR, b"\x00\x00" + bytes([idx]) + b"\x00\x20\x30\x11\x20", BUS]
  # print(*msg)
  # p.can_send(*msg)
  # sleep(0.04)
  # p.can_send(*msg)
  # sleep(0.04)
  # p.can_send(*msg)
  # idx += 1
  # sleep(1)

  msg = [ADDR, b"\x00\x00" + bytes([idx]) + b"\x00\x00\x30\x12\x6c", BUS]
  print(*msg)
  p.can_send(*msg)
  sleep(0.04)
  p.can_send(*msg)
  sleep(0.04)
  p.can_send(*msg)
  idx += 1

  return idx

def speed_limit_65_mph(idx):
  # msg = [ADDR, b"\x00\x00" + bytes([idx]) + b"\x40\x20\x52\x00\x1c", BUS]
  # print(*msg)
  # p.can_send(*msg)
  # sleep(0.04)
  # p.can_send(*msg)
  # sleep(0.04)
  # p.can_send(*msg)
  # idx += 1
  # sleep(2)

  # msg = [ADDR, b"\x00\x00" + bytes([idx]) + b"\x00\x20\x50\x15\x30", BUS]
  # print(*msg)
  # p.can_send(*msg)
  # sleep(0.04)
  # p.can_send(*msg)
  # sleep(0.04)
  # p.can_send(*msg)
  # idx += 1
  # sleep(1)

  msg = [ADDR, b"\x00\x00" + bytes([idx]) + b"\x00\x20\x10\x15\x90", BUS]
  print(*msg)
  p.can_send(*msg)
  sleep(0.04)
  p.can_send(*msg)
  sleep(0.04)
  p.can_send(*msg)
  idx += 1

  return idx

def switch(idx):
  msg = [ADDR, b"\x00\x00" + bytes([idx]) + b"\x00\x20\x10\x15\x88", BUS]
  print(*msg)
  p.can_send(*msg)
  sleep(0.04)
  p.can_send(*msg)
  sleep(0.04)
  p.can_send(*msg)
  idx += 1

  return idx 

if __name__ == "__main__":
  p = Panda()
  p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

  idx = start(0)
  idx = speed_limit_65_mph(idx)
  while 1:
    cmd = input("> ").strip()
    if cmd == "start":
      idx = start(idx)
    elif cmd == "stop":
      idx = stop(idx)
    elif cmd == "55":
      idx = speed_limit_55_mph(idx)
    elif cmd == "65":
      idx = speed_limit_65_mph(idx)
    elif cmd == "switch":
      idx = switch(idx)
    elif cmd == "exit":
      break
