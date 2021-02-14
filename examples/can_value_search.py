#!/usr/bin/env python

import binascii
import csv
import sys

class Message():
  """Details about a specific message ID."""
  def __init__(self, message_id, mask_len):
    self.message_id = message_id
    self.mask_len = mask_len
    self.matches = [0] * 64 # 1 = always matches desired value
    self.min = [0] * 64
    self.max = [0] * 64

  def printMatches(self):
    """Prints bits that transition from always zero to always 1 and vice versa."""
    for i in range(len(self.matches)):
      if self.matches[i]:
        print(f'id {self.message_id} matches bits {i}-{i+self.mask_len} (starts in byte {int(i/8)}) ({self.min[i]}-{self.max[i]})')

class Info():
  """A collection of Messages."""

  def __init__(self):
    self.messages = {}  # keyed by MessageID

  def load(self, filename, value, tolerance, start, end):
    """Given a CSV file, adds information about message IDs and their values."""
    with open(filename, 'r') as f:
      v = value
      mask = 0
      mask_len = 0
      while v > 0:
        v >>= 1
        mask_len += 1
      mask = (1 << mask_len) - 1

      reader = csv.reader(f)
      next(reader, None)  # skip the CSV header
      for row in reader:
        if not len(row): continue
        time = float(row[0])
        if not row[2].isdigit():
          continue
        bus = int(row[2])
        if time < start or bus > 127:
          continue
        elif time > end:
          break
        if row[1].startswith('0x'):
          message_id = row[1][2:]  # remove leading '0x'
        else:
          message_id = hex(int(row[1]))[2:]  # old message IDs are in decimal
        message_id = f'{bus}:{message_id}'

        # HACK: filter addrs
        #if message_id not in ['0:222', '0:223', '0:224', '0:225']:
        #  continue

        if row[3].startswith('0x'):
          data = row[3][2:]  # remove leading '0x'
        else:
          data = row[3]
        new_message = False
        if message_id not in self.messages:
          self.messages[message_id] = Message(message_id, mask_len)
          new_message = True
        message = self.messages[message_id]

        v = 0
        # assumes little endian
        d = bytearray.fromhex(data)
        # assumes big endian
        #d.reverse()
        for i in range(len(d)):
          v += int(d[i]) << (i * 8)
        i = 0
        while v > 0:
          b = v & mask
          # if new_message:
          #   message.matches[i] = abs(b - value) <= tolerance
          #   message.min[i] = b
          #   message.max[i] = b
          # else:
          #   if message.min[i] > b: message.min[i] = b
          #   if message.max[i] < b: message.max[i] = b
          #   if message.matches[i] == 1 and abs(b - value) > tolerance:
          #     message.matches[i] = 0
          # HACK: find all places a value occurs
          #if message_id == '0:224' and b == value: print(b, value, i)
          if new_message:
            message.matches[i] = abs(b - value) <= tolerance
            message.min[i] = b
            message.max[i] = b
          else:
            if message.min[i] > b: message.min[i] = b
            if message.max[i] < b: message.max[i] = b
            if message.matches[i] == 0 and abs(b - value) <= tolerance:
              message.matches[i] = 1
          v >>= 1
          i += 1

def PrintMatchingValues(log_file, value, tolerance, time_range):
  value = int(value)
  tolerance = int(tolerance)
  start, end = map(float, time_range.split('-'))
  info = Info()
  info.load(log_file, value, tolerance, start, end)
  for message_id in sorted(info.messages):
    info.messages[message_id].printMatches()

if __name__ == "__main__":
  if len(sys.argv) < 5:
    print(f'Usage:\n{sys.argv[0]} log.csv <value> <tolerance> <start>-<end>')
    sys.exit(0)
  PrintMatchingValues(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
