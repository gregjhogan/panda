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

  for s in tqdm([1, 2, 3, 5, 7, 16]): # session types
    uds_client.diagnostic_session_control(SESSION_TYPE.DEFAULT)
    time.sleep(.1)
    uds_client.diagnostic_session_control(s)
    time.sleep(.1)
    for addr in (0, 0x2000, 0x20000): # addrs to check
      try:
        uds_client.read_memory_by_address(addr, 8)
      except NegativeResponseError as e:
        if e.error_code != 0x11: # service not supported
          print(f"\n{hex(addr)}: {e.error_code} - {e.message}")
