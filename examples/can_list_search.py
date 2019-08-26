#!/usr/bin/env python

import binascii
import csv
import sys

class Message():
  """Details about a specific message ID."""
  def __init__(self, message_id, min_unique_count):
    self.message_id = message_id
    self.min_unique_count = min_unique_count
    self.matches = [0] * 8 # 1 = contains all desired values
    self.unique = [set() for i in range(8)] # contains unique values matched

  def printMatches(self):
    """Prints bits that transition from always zero to always 1 and vice versa."""
    for i in xrange(len(self.matches)):
      if self.matches[i] and len(self.unique[i]) >= self.min_unique_count:
        print('id {} matches at byte {} {}'.format(self.message_id, i, self.unique[i]))

class Info():
  """A collection of Messages."""

  def __init__(self):
    self.messages = {}  # keyed by MessageID

  def load(self, filename, values, min_unique_count, start, end):
    """Given a CSV file, adds information about message IDs and their values."""
    with open(filename, 'rb') as input:
      reader = csv.reader(input)
      next(reader, None)  # skip the CSV header
      for row in reader:
        if not len(row): continue
        time = float(row[0])
        bus = int(row[2])
        if time < start or bus > 127:
          continue
        elif time > end:
          break
        if row[1].startswith('0x'):
          message_id = row[1][2:]  # remove leading '0x'
        else:
          message_id = hex(int(row[1]))[2:]  # old message IDs are in decimal
        message_id = '%s:%s' % (bus, message_id)
        if row[3].startswith('0x'):
          data = row[3][2:]  # remove leading '0x'
        else:
          data = row[3]
        new_message = False
        if message_id not in self.messages:
          self.messages[message_id] = Message(message_id, min_unique_count)
          new_message = True
        message = self.messages[message_id]
        bytes = bytearray.fromhex(data)
        for i in xrange(len(bytes)):
          byte = int(bytes[i])
          if new_message:
            message.matches[i] = byte in values
          elif message.matches[i] == 1 and byte not in values:
              message.matches[i] = 0
          message.unique[i].add(byte)

def PrintMatchingValues(log_file, values, min_unique_count, time_range):
  values = map(int, values.split(','))
  min_unique_count = int(min_unique_count)
  start, end = map(float, time_range.split('-'))
  info = Info()
  info.load(log_file, values, min_unique_count, start, end)
  for message_id in sorted(info.messages):
    info.messages[message_id].printMatches()

if __name__ == "__main__":
  if len(sys.argv) < 5:
    print 'Usage:\n%s log.csv <value1,value2,value3> <min-unique-match-count> <start>-<end>' % sys.argv[0]
    sys.exit(0)
  PrintMatchingValues(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
