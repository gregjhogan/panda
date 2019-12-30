#!/usr/bin/env python3
import struct
from panda import Panda
from panda.python.uds import UdsClient, MessageTimeoutError, NegativeResponseError

panda = Panda()
panda.set_safety_mode(Panda.SAFETY_ELM327)

uds_client = UdsClient(panda, 0x18DA60F1, bus=1 if panda.has_obd() else 0, timeout=1, debug=False)
uds_client.tester_present()

result = uds_client.read_data_by_identifier(0x7010)
dist_units = "mi" if result[7] == 0 else "km"

result = uds_client.read_data_by_identifier(0x7022)
odometer = struct.unpack('!I', b'\x00'+result[6:9])[0]
print(f"odometer: {odometer} {dist_units}")

result = uds_client.read_data_by_identifier(0x7028)
temp_units = "C" if result[8] == 0 else "F"
state = "off" if result[9] == 0 else "running"
temp = struct.unpack('!h', result[16:18])[0]
print(f"vehicle: {state}")
print(f"temp: {temp} {temp_units}")

result = uds_client.read_data_by_identifier(0x7029)
fuel = struct.unpack('!H', result[12:14])[0]
print(f"fuel: {fuel} gal")

result = uds_client.read_data_by_identifier(0x702A)
range = struct.unpack('!H', result[14:16])[0]
print(f"range: {range} {dist_units}")
