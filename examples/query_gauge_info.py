#!/usr/bin/env python3
from panda import Panda
from panda.python.uds import UdsClient, MessageTimeoutError, NegativeResponseError

panda = Panda()
panda.set_safety_mode(Panda.SAFETY_ELM327)

uds_client = UdsClient(panda, 0x18DA60F1, bus=1 if panda.has_obd() else 0, timeout=0.1, debug=False)
uds_client.tester_present()

result = uds_client.read_data_by_identifier(0x7022)
odometer = result[5:9]
print(f"odometer: {odometer} mi")

result = uds_client.read_data_by_identifier(0x7028)
temp = result[16:18]
print(f"temp: {temp} F")

result = uds_client.read_data_by_identifier(0x7029)
fuel = result[12:14]
print(f"fuel: {fuel} gal")

