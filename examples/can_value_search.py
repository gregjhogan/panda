#!/usr/bin/env python

import binascii
import csv
import sys

class Message():
  """Details about a specific message ID."""
  def __init__(self, message_id):
    self.message_id = message_id
    self.matches = [0] * 8 # 1 = always matches desired value
    self.min = [0] * 8
    self.max = [0] * 8

  def printMatches(self):
    """Prints bits that transition from always zero to always 1 and vice versa."""
    for i in range(len(self.matches)):
      if self.matches[i]:
        print(f'id {self.message_id} matches at byte {i} ({self.min[i]}-{self.max[i]})')

class Info():
  """A collection of Messages."""

  def __init__(self):
    self.messages = {}  # keyed by MessageID

  def load(self, filename, value, tolerance, start, end):
    """Given a CSV file, adds information about message IDs and their values."""
    with open(filename, 'r') as f:
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
        if row[3].startswith('0x'):
          data = row[3][2:]  # remove leading '0x'
        else:
          data = row[3]
        new_message = False
        if message_id not in self.messages:
          self.messages[message_id] = Message(message_id)
          new_message = True
        message = self.messages[message_id]
        d = bytearray.fromhex(data)
        for i in range(len(d)):
          b = int(d[i])
          if new_message:
            message.matches[i] = abs(b - value) <= tolerance
            message.min[i] = b
            message.max[i] = b
          else:
            if message.min[i] > b: message.min[i] = b
            if message.max[i] < b: message.max[i] = b
            if message.matches[i] == 1 and abs(b - value) > tolerance:
              message.matches[i] = 0

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
