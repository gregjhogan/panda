#!/usr/bin/env python
import sys
import time
import struct
import threading
from panda import Panda

def can_cksum(mm):
  s = 0
  for c in mm:
    c = ord(c)
    s += (c>>4)
    s += c & 0xF
  s = 8-s
  s %= 0x10
  return s

def fix(msg, addr):
  msg2 = msg[0:-1] + chr(ord(msg[-1]) | can_cksum(struct.pack("I", addr)+msg))
  return msg2

def make_can_msg(addr, dat, idx, alt):
  if idx is not None:
    dat += chr(idx << 4)
    dat = fix(dat, addr)
  return [addr, 0, dat, alt]

def get_distance(dat):
  dist = (dat[0] << 4) + (dat[1] >> 4)
  return dist * 0.0625 # value is 1/16 meters

if __name__ == "__main__":
  panda = Panda()
  panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

  bus = 0
  radar_send_step = 5 # 20 Hz
  msg_0x301 = "\x00\x00\x56\x02\x58\x00\x00" # honda pilot

  tracks = [0] * 16

  frame = 0
  t = 0
  while (1):
    n = round(time.time(), 2)
    if (n <= t): # 100 Hz clock
      continue
    t = n
    frame += 1

    if frame % radar_send_step == 0: # 20 Hz
      commands = []
      idx = (frame / radar_send_step) % 4
      speed = chr(0)
      msg_0x300 = ("\xf9" + speed + "\x8a\xd0" +\
                  ("\x20" if idx == 0 or idx == 3 else "\x00") +\
                   "\x00\x00")
      commands.append(make_can_msg(0x300, msg_0x300, idx, bus))
      commands.append(make_can_msg(0x301, msg_0x301, idx, bus))
      panda.can_send_many(commands)

    msgs = panda.can_recv()
    for addr, ts, dat, bus in msgs:
      if addr == 0x430:
        tracks[0] = get_distance(dat)
      if addr == 0x431:
        tracks[1] = get_distance(dat)
      if addr == 0x432:
        tracks[2] = get_distance(dat)
      if addr == 0x433:
        tracks[3] = get_distance(dat)
      if addr == 0x434:
        tracks[4] = get_distance(dat)
      if addr == 0x435:
        tracks[5] = get_distance(dat)
      if addr == 0x436:
        tracks[6] = get_distance(dat)
      if addr == 0x437:
        tracks[7] = get_distance(dat)
      if addr == 0x438:
        tracks[8] = get_distance(dat)
      if addr == 0x439:
        tracks[9] = get_distance(dat)
      if addr == 0x440:
        tracks[10] = get_distance(dat)
      if addr == 0x441:
        tracks[11] = get_distance(dat)
      if addr == 0x442:
        tracks[12] = get_distance(dat)
      if addr == 0x443:
        tracks[13] = get_distance(dat)
      if addr == 0x444:
        tracks[14] = get_distance(dat)
      if addr == 0x445:
        tracks[15] = get_distance(dat)

    sys.stdout.write("%06.2f %06.2f %06.2f %06.2f %06.2f %06.2f %06.2f %06.2f %06.2f %06.2f %06.2f %06.2f %06.2f %06.2f %06.2f %06.2f \r" % (tracks[0], tracks[1], tracks[2], tracks[3], tracks[4], tracks[5], tracks[6], tracks[7], tracks[8], tracks[9], tracks[10], tracks[11], tracks[12], tracks[13], tracks[14], tracks[15]))
    sys.stdout.flush()
