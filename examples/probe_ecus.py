#!/usr/bin/env python3
import argparse
from tqdm import tqdm
from panda import Panda
from panda.python.uds import UdsClient, MessageTimeoutError, NegativeResponseError, SESSION_TYPE, CONTROL_TYPE, MESSAGE_TYPE

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--can-bus', type=int, default=0, help='CAN bus number (zero based)')
  args = parser.parse_args()

  panda = Panda()
  panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

  print("querying addrs ...")
  l = list(range(0x700, 0x7E8))
  with tqdm(total=len(l)) as t:
    for i in l:
      t.set_description(f"{hex(i)}")
      uds_client = UdsClient(panda, i, bus=args.can_bus, timeout=0.1, debug=False)
      try:
        # uds_client.diagnostic_session_control(SESSION_TYPE.DEFAULT)
        uds_client.tester_present()
        print(f"\nECU on addr: {hex(i)}")
      except MessageTimeoutError as e:
        pass
      except Exception as e:
        print(f"\nECU error: {hex(i)}\n{e}")
      t.update(1)
