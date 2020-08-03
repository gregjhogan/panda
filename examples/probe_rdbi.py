#!/usr/bin/env python3
import argparse
import time
from tqdm import tqdm
from panda import Panda
from panda.python.uds import UdsClient, MessageTimeoutError, NegativeResponseError, SESSION_TYPE, CONTROL_TYPE, MESSAGE_TYPE

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--can-bus', type=int, default=0, help='CAN bus number (zero based)')
  parser.add_argument('--can-addr', type=int, default=0x7D0, help='CAN address for UDS')
  args = parser.parse_args()

  panda = Panda()
  panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
  uds_client = UdsClient(panda, args.can_addr, bus=args.can_bus, timeout=1, debug=False)
  uds_client.diagnostic_session_control(SESSION_TYPE.DEFAULT)
  time.sleep(0.1)
  uds_client.diagnostic_session_control(SESSION_TYPE.EXTENDED_DIAGNOSTIC)
  # uds_client.diagnostic_session_control(0x7)

  # prev = None
  # while True:
  #   data = uds_client.read_data_by_identifier(0x302)
  #   if prev != data:
  #     print(f"0x{data.hex()}")
  #     prev = data
    

  print("querying ids ...")
  l = list(range(0x10000))
  with tqdm(total=len(l)) as t:
    for i in l:
      try:
        t.set_description(f"{hex(i)}")
        data = uds_client.read_data_by_identifier(i)
        print(f"\n{hex(i)}: 0x{data.hex()}")
      except NegativeResponseError as e:
        if e.error_code != 0x31: # request out of range
          print(f"\n{hex(i)}: {e.error_code} - {e.message}")
      t.update(1)

# session type = 3
##################
# connected
# querying ids ...
# 0x121: 0x4b
# 0x123: 0x0191fff9
# 0x125: 0x01
# 0x127: 0xfe
# 0x128: 0xfa
# 0x131: 0x1428
# 0x140: 0x00
# 0x171: 0x8c
# 0x200: 0x00
# 0x201: 0x14
# 0x202: 0x00
# 0x203: 0xcc
# 0x204: 0x00
# 0x210: 0xff
# 0x220: 0x00
# 0xf100: 0x4c58325f20534343204648435550202020202020312e303020312e30342039393131302d5338313030202020202020202020
# 0xf110: 0x17cf0000
# 0xf18b: 0x20200410
# 0xf18c: 0x0200440100415900000606
# 0xf1a0: 0x312e3034

# session type = 7
##################
# connected
# querying ids ...
# 0x104: 0x000000000000000000000000000000000000
# 0x105: 0x0000000000000000000000000000000000000000010022000200000000
# 0x106: 0x0000000000000000000000000000
# 0x107: 0x00000000000000000000
# 0x108: 0x00000000000000000000000000000000000000000000000000000000
# 0x109: 0xabcd106dabcd100cabcd11e0580d5d0c01e0
# 0x121: 0x4b
# 0x122: 0x
# 0x123: 0x0191fff9
# 0x125: 0x01fefa0000000000000000fa0064
# 0x126: 0x00
# 0x127: 0xfe
# 0x128: 0xfa
# 0x129: 0x00
# 0x131: 0x1428
# 0x140: 0x00
# 0x141: 0x000000
# 0x142: 0x000000010000
# 0x143: 0x00000000000000000000000000000000000000000000
# 0x147: 0x00
# 0x160: 0x0000000100000000
# 0x161: 0x0000000100000000
# 0x162: 0x00000000040000000000000000000000
# 0x163: 0x00000000
# 0x164: 0x00000000
# 0x171: 0x8b
# 0x172: 0x
# 0x173: 0x0517
# 0x174: 0x0d12
# 0x175: 0x130c
# 0x176: 0x
# 0x177: 0x
# 0x178: 0x
# 0x190: 0x0991
# 0x200: 0x00
# 0x201: 0x14
# 0x202: 0x00
# 0x203: 0xcc
# 0x204: 0x00
# 0x210: 0xff
# 0x220: 0x00
# 0x240: 0x8888888f8f8fff02
# 0x241: 0x0103010103038001
# 0x302: 0x0007fff300000050000dffe8000000500005ffee000000000403fffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 
# 0x500: 0x
# 0x501: 0x
# 0x551: 0x0300000000000000
# 0x552: 0x
# 0xf100: 0x4c58325f20534343204648435550202020202020312e303020312e30342039393131302d5338313030190502165620202020
# 0xf110: 0x17cf0000
# 0xf18b: 0x20200410
# 0xf18c: 0x0200440100415900000606
# 0xf1a0: 0x312e3034
# 0xf1f0: 0x254d44523030303230303634a5a5a5a54d5232303030303130322e30312e303130312e30312e585844464c544d52323030303031484b4d4341534b5f
# 0xf1f1: 0x254d4452303030313030333230312e30302e3030464e5f5f00020001010201
# 0xfefe: 0x0206
# 0xff50: 0x0100

