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
  panda.set_safety_mode(Panda.SAFETY_ELM327)
  uds_client = UdsClient(panda, args.can_addr, bus=args.can_bus, timeout=0.1, debug=False)
  uds_client.diagnostic_session_control(SESSION_TYPE.DEFAULT)
  time.sleep(0.1)
  uds_client.diagnostic_session_control(SESSION_TYPE.EXTENDED_DIAGNOSTIC)
  # uds_client.diagnostic_session_control(0x5)

  # from panda.python.uds import DYNAMIC_DEFINITION_TYPE, DynamicSourceDefinition
  # di = {"data_identifier": 0xF200, "position": 0, "memory_size": 4, "memory_address": 0}
  # uds_client.dynamically_define_data_identifier(DYNAMIC_DEFINITION_TYPE.DEFINE_BY_MEMORY_ADDRESS, 0xF201, [di])
  # exit(0)

  print("querying ids ...")
  l = list(range(0x100))
  with tqdm(total=len(l)) as t:
    for i in l:
      for m in range(1,4):
        try:
          t.set_description(f"{hex(i)} - {m}")
          uds_client.read_data_by_periodic_identifier(m, i)
          print(f"\n{i} - {m}: success")
        except NegativeResponseError as e:
          if e.error_code != 0x31: # request out of range
            print(f"\n{hex(i)} - {m}: {e.error_code} - {e.message}")
      t.update(1)
