#!/usr/bin/env python

import binascii
import csv
import sys

class Message():
  """Details about a specific message ID."""
  def __init__(self, message_id, min_count):
    self.message_id = message_id
    self.count = 0
    self.matches = [0] * 8 # count of matches of desired value
    self.min_count = min_count

  def printMatches(self):
    """Prints bits that transition from always zero to always 1 and vice versa."""
    for i in xrange(len(self.matches)):
      if self.matches[i] >= self.min_count:
        print 'id %s matches at byte %d (%d of %d)' % (self.message_id, i, self.matches[i], self.count)

class Info():
  """A collection of Messages."""

  def __init__(self):
    self.messages = {}  # keyed by MessageID

  def load(self, filename, value, min_count, start, end):
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
        if message_id not in self.messages:
          self.messages[message_id] = Message(message_id, min_count)
        message = self.messages[message_id]
        message.count += 1
        bytes = bytearray.fromhex(data)
        for i in xrange(len(bytes)):
          byte = int(bytes[i])
          if byte == value:
            message.matches[i] += 1

def PrintMatchingValues(log_file, value, min_count, time_range):
  value = int(value)
  min_count = int(min_count)
  start, end = map(float, time_range.split('-'))
  info = Info()
  info.load(log_file, value, min_count, start, end)
  for message_id in sorted(info.messages):
    info.messages[message_id].printMatches()

if __name__ == "__main__":
  if len(sys.argv) < 5:
    print 'Usage:\n%s log.csv <value> <min-count> <start>-<end>' % sys.argv[0]
    sys.exit(0)
  PrintMatchingValues(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
