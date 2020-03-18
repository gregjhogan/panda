#!/usr/bin/env python3
from tqdm import tqdm
from panda import Panda
from panda.python.uds import UdsClient, MessageTimeoutError, NegativeResponseError, SESSION_TYPE, CONTROL_TYPE, MESSAGE_TYPE

ADDR=0x18DA30F1

if __name__ == "__main__":
  panda = Panda()
  panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
  uds_client = UdsClient(panda, ADDR, bus=1 if panda.has_obd() else 0, timeout=0.1, debug=False)
  uds_client.diagnostic_session_control(SESSION_TYPE.EXTENDED_DIAGNOSTIC)

  # messages that work
  #data = uds_client.communication_control(CONTROL_TYPE.DISABLE_RX_DISABLE_TX, MESSAGE_TYPE.NORMAL_AND_NETWORK_MANAGEMENT)
  #data = uds_client.communication_control(CONTROL_TYPE.DISABLE_RX_DISABLE_TX | 0x80, MESSAGE_TYPE.NORMAL_AND_NETWORK_MANAGEMENT)
  #exit(0)

  print("querying addresses ...")
  l = list(range(0x10000))
  with tqdm(total=len(l)) as t:
    for i in l:
      ct = i >> 8
      mt = i & 0xFF
      t.set_description(f"{hex(ct)} - {hex(mt)}")
      try:
        data = uds_client.communication_control(ct, mt)
        print(f"\n{ct} - {mt}: success")
      except NegativeResponseError as e:
        if e.message != "COMMUNICATION_CONTROL - sub-function not supported" and e.message != "COMMUNICATION_CONTROL - request out of range":
          print(f"\n{ct} - {mt}: {e.message}")
      t.update(1)
