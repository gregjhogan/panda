#!/usr/bin/env python3
import datetime
from binascii import hexlify

from python import Panda
from python.uds import UdsClient, NegativeResponseError
from python.uds import SESSION_TYPE, DTC_GROUP_TYPE

panda = Panda()
address = 0x7D4 # Hyundai EPS
uds_client = UdsClient(panda, address, debug=False)
print("tester present ...")
uds_client.tester_present()
print("extended diagnostic session ...")
uds_client.diagnostic_session_control(SESSION_TYPE.EXTENDED_DIAGNOSTIC)
print("clear diagnostic info ...")
uds_client.clear_diagnostic_information(DTC_GROUP_TYPE.ALL)
