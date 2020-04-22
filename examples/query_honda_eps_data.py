#!/usr/bin/env python3
import struct
from tqdm import tqdm
from panda import Panda
from panda.python.uds import UdsClient, MessageTimeoutError, NegativeResponseError, SESSION_TYPE, DATA_IDENTIFIER_TYPE

panda = Panda()
panda.can_clear(0xFFFF)
panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
uds_client = UdsClient(panda, 0x18DA30F1, bus=1 if panda.has_obd() else 0, timeout=1, debug=False)
# uds_client.diagnostic_session_control(SESSION_TYPE.EXTENDED_DIAGNOSTIC)
while True:
  data = uds_client.read_data_by_identifier(0x48A2)
  STEER_TORQUE, flags, fedf30a0, fedf15aa, RATE_LIMITED_TORQUE_4 = struct.unpack('!hbhhh', data[:9])
  print(f"STEER_TORQUE: {hex(STEER_TORQUE)}")
  print(f"FLAGS: {flags}")
  print(f"USER_TORQUE: {fedf30a0}")
  print(f"STEER_RATE: {fedf15aa}")
  print(f"RATE_TORQUE: {hex(RATE_LIMITED_TORQUE_4)}") # max 0x200
  print("")
