#!/usr/bin/env python
import time
import struct
from panda import Panda
from hexdump import hexdump
from isotp import isotp_send, isotp_recv

# 0x7e0 = Toyota
# 0x18DB33F1 for Honda?

def get_current_data_for_pid(pid):
  # 01 xx = Show current data
  isotp_send(panda, "\x01"+chr(pid), 0x18DA10F1)
  return isotp_recv(panda, 0x18DAF110)

def get_supported_pids():
  ret = []
  pid = 0
  while 1:
    supported = struct.unpack(">I", get_current_data_for_pid(pid)[2:])[0]
    for i in range(1+pid, 0x21+pid):
      if supported & 0x80000000:
        ret.append(i)
      supported <<= 1
    pid += 0x20
    if pid not in ret:
      break
  return ret

if __name__ == "__main__":
  panda = Panda()
  panda.set_safety_mode(Panda.SAFETY_ELM327)

  # panda.can_clear(0)
  # time.sleep(0.1)

  for z in range(0,3):
    addr = 0x18DA10F1
    msg = "\x02\x09\x02".ljust(8, "\x00")
    print "S:", format(addr,'x'), msg.encode("hex")
    panda.can_send(addr, msg, 0)
    more = False
    for x in range(0, 100):
      msgs = panda.can_recv()
      for ids, ts, dat, bus in msgs:
        if bus == 0 and ids == ((addr >> 16 << 16) | (addr << 8 & 0xFFFF) | (addr >> 8 & 0xFF)):
          print "R:", format(ids,'x'), ("".join("%02x" % i for i in dat))
          print dat[5:]
          msg = "\x30\x00\x00".ljust(8, "\x00")
          panda.can_send(addr, msg, 0)
          print "S:", format(addr,'x'), msg.encode("hex")
          more = True
          break

      if more:
        break

    if more:
      for x in range(0, 100):
        msgs = panda.can_recv()
        for ids, ts, dat, bus in msgs:
          #if bus == 0 and ids == ((addr >> 16 << 16) | (addr << 8 & 0xFFFF) | (addr >> 8 & 0xFF)):
          if bus == 0 and ids>>16 == addr>>16:
            print "R:", format(ids,'x'), ("".join("%02x" % i for i in dat))
            print dat[1:]
    else:
      print "failed!"

  print "done"

  # 09 02 = Get VIN
  # isotp_send(panda, "\x01\x00", 0x18DA10F1)
  # ret = isotp_recv(panda, 0x18DAF110)
  # hexdump(ret)
  # print "VIN: %s" % ret[2:]

  # # 03 = get DTCS
  # isotp_send(panda, "\x03", 0x18DA10F1)
  # dtcs = isotp_recv(panda, 0x18DAF110)
  # print "DTCs:", dtcs[2:].encode("hex")

  # supported_pids = get_supported_pids()
  # print "Supported PIDs:",supported_pids

  # while 1:
  #   speed = struct.unpack(">B", get_current_data_for_pid(13)[2:])[0]                  # kph
  #   rpm = struct.unpack(">H", get_current_data_for_pid(12)[2:])[0]/4.0                # revs
  #   throttle = struct.unpack(">B", get_current_data_for_pid(17)[2:])[0]/255.0 * 100   # percent
  #   temp = struct.unpack(">B", get_current_data_for_pid(5)[2:])[0] - 40               # degrees C
  #   load = struct.unpack(">B", get_current_data_for_pid(4)[2:])[0]/255.0 * 100        # percent
  #   print "%d KPH, %d RPM, %.1f%% Throttle, %d deg C, %.1f%% load" % (speed, rpm, throttle, temp, load)
  #   time.sleep(0.2)



