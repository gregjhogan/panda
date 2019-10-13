#!/usr/bin/env python
import datetime
from binascii import hexlify

from python import Panda
from python.uds import UdsClient, NegativeResponseError
from python.uds import SESSION_TYPE, DATA_IDENTIFIER_TYPE

# 0x0:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x1:SUCCESS
# 0x2:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported in active session
# 0x3:SUCCESS
# 0x4:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x5:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x6:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x7:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x8:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x9:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0xa:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0xb:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0xc:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0xd:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0xe:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0xf:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x10:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x11:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x12:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x13:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x14:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x15:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x16:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x17:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x18:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x19:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x1a:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x1b:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x1c:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x1d:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x1e:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x1f:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x20:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x21:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x22:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x23:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x24:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x25:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x26:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x27:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x28:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x29:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x2a:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x2b:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x2c:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x2d:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x2e:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x2f:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x30:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x31:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x32:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x33:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x34:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x35:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x36:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x37:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x38:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x39:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x3a:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x3b:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x3c:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x3d:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x3e:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x3f:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x40:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x41:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x42:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x43:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x44:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x45:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x46:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x47:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x48:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x49:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x4a:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x4b:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x4c:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x4d:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x4e:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x4f:DIAGNOSTIC_SESSION_CONTROL - security access denied
# 0x50:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x51:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x52:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x53:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x54:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x55:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x56:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x57:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x58:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x59:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x5a:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x5b:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x5c:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x5d:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x5e:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x5f:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x60:SUCCESS
# 0x61:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x62:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x63:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x64:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x65:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x66:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x67:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x68:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x69:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x6a:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x6b:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x6c:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x6d:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x6e:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x6f:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x70:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x71:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x72:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x73:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x74:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x75:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x76:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x77:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x78:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x79:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x7a:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x7b:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x7c:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x7d:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x7e:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported
# 0x7f:DIAGNOSTIC_SESSION_CONTROL - sub-function not supported

def main():
  panda = Panda()
  address = 0x18DAB0F1 # radar
  uds_client = UdsClient(panda, address, debug=False)
  print("tester present ...")
  uds_client.tester_present()
  print("extended diagnostic session ...")
  for st in range(0x80):
    #uds_client.diagnostic_session_control(SESSION_TYPE.DEFAULT)
    uds_client.diagnostic_session_control(SESSION_TYPE.EXTENDED_DIAGNOSTIC)
    try:
      uds_client.diagnostic_session_control(st)
      print("{}:{}".format(hex(st), 'SUCCESS'))
    except NegativeResponseError as e:
      print("{}:{}".format(hex(st), e))

if __name__ == "__main__":
  main()
