#!/usr/bin/env python3
from time import sleep

from panda import Panda
from panda.python.uds import UdsClient, MessageTimeoutError, NegativeResponseError, SESSION_TYPE, CONTROL_PARAMETER_TYPE

if __name__ == "__main__":
  panda = Panda()
  panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

  # 0xB008 = wipers_front_low
  # 0xB009 = wipers_front_high
  # 0xB00A = wipers_rear
  # 0xB038 = front passenger seatbelt flash
  # 0xB039 = 2nd row left seatbelt flash
  # 0xB03b = 2nd row right seatbelt flash
  # 0xB065 = 3nd row left seatbelt flash
  # 0xB07F = 3nd row middle seatbelt flash
  # 0xB066 = 3nd row right seatbelt flash

  # uds_client = UdsClient(panda, 0x7a0, bus=0, timeout=0.1, debug=True)
  uds_client = UdsClient(panda, 0x700, 0x720, bus=0, timeout=0.1, debug=False)
  print('extended diagnostic session')
  uds_client.diagnostic_session_control(SESSION_TYPE.EXTENDED_DIAGNOSTIC)
  print('i/o control by id')
  # uds_client.input_output_control_by_identifier(0xB008, 0x03, b"")
  import tqdm
  for i in tqdm.tqdm(range(0x0000, 0x10000, 0x1000)):
    uds_client.tester_present()
    try:
      uds_client.input_output_control_by_identifier(i, 0x03, b"")
      print(f"\n\n======== {i} ========\n\n")
    except Exception as e:
      pass
    # sleep(0.01)
  exit()


  addr = 0x793
  # addr = 0x7A0
  uds_client = UdsClient(panda, addr, bus=0, timeout=0.1, debug=False)
  # uds_client.tester_present()
  # exit()
  uds_client.diagnostic_session_control(SESSION_TYPE.EXTENDED_DIAGNOSTIC)

  for i in range(0x27, 0x28):
    id = 0xF000+i
    print(hex(id))
    try:
      for j in range(0x100, 0x1000):
        a = j>>8
        b = bytes([j&0xff])
        # print(a,b)
        try:
          uds_client.input_output_control_by_identifier(id, a, b)
          print(f"works: {a} {b}")
          sleep(1)
          uds_client.input_output_control_by_identifier(id, 0x00, b'\x00')
        except Exception as e:
          if e.error_code != 0x31: # request out of range
            print(f"ERROR_CODE: {e.error_code}")
    except Exception:
      pass
  exit()

  print("0xF012")
  uds_client.input_output_control_by_identifier(0xF012, 0x07, b'\xff')
  sleep(2)
  uds_client.input_output_control_by_identifier(0xF012, 0x00, b'\x00')
  sleep(1)

  print("0xF013")
  uds_client.input_output_control_by_identifier(0xF013, 0x07, b'\xff')
  sleep(2)
  uds_client.input_output_control_by_identifier(0xF013, 0x00, b'\x00')
  sleep(1)

  print("0xF020")
  uds_client.input_output_control_by_identifier(0xF020, 0x07, b'\xff')
  sleep(2)
  uds_client.input_output_control_by_identifier(0xF020, 0x00, b'\x00')
  sleep(1)

  print("0xF021")
  uds_client.input_output_control_by_identifier(0xF021, 0x07, b'\xff')
  sleep(2)
  uds_client.input_output_control_by_identifier(0xF021, 0x00, b'\x00')
  sleep(1)

  print("0xF024")
  uds_client.input_output_control_by_identifier(0xF024, 0x07, b'\xff')
  sleep(2)
  uds_client.input_output_control_by_identifier(0xF024, 0x00, b'\x00')
  sleep(1)

  print("0xF025")
  uds_client.input_output_control_by_identifier(0xF025, 0x07, b'\xff')
  sleep(2)
  uds_client.input_output_control_by_identifier(0xF025, 0x00, b'\x00')
  sleep(1)

  print("0xF027")
  uds_client.input_output_control_by_identifier(0xF027, 0x07, b'\xff')
  sleep(2)
  uds_client.input_output_control_by_identifier(0xF027, 0x00, b'\x00')
  sleep(1)
