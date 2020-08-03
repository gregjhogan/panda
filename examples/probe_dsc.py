#!/usr/bin/env python3
import argparse
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
  uds_client = UdsClient(panda, args.can_addr, bus=args.can_bus, timeout=0.1, debug=False)

  print("querying ids ...")
  l = list(range(0x80))
  with tqdm(total=len(l)) as t:
    for i in l:
      uds_client.diagnostic_session_control(SESSION_TYPE.DEFAULT)
      try:
        t.set_description(f"{hex(i)}")
        uds_client.diagnostic_session_control(i)
        print(f"\n{hex(i)}: success")
      except NegativeResponseError as e:
        if e.error_code != 0x12: # sub-function not supported
          print(f"\n{hex(i)}: {e.error_code} - {e.message}")
      t.update(1)

# connected
# querying ids ...
# 0x1: success
# 0x2: success
# 0x3: success
# 0x5: success
# 0x7: success
# 0x10: success
