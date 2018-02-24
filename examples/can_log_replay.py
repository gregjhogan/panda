#!/usr/bin/env python
import sys
import time
import struct
from panda import Panda

DEBUG = False

def main():
  logfile = sys.argv[1]

  print "open log file {}".format(logfile)
  with open(logfile,'r') as log:

    print "wait for panda ..."
    p = None
    while not p:
      time.sleep(0.1)
      try:
          p = Panda()
      except:
          pass

    start_time = time.time()

    print "replay log ..."
    log.readline() # skip header
    for line in log:
      line = line.rstrip()
      if not line: continue

      # parse the log line
      t, addr, bus, data = line.split(',')
      bus = int(bus)
      if (bus >= 100): continue # skip forwarded messages
      t = float(t) + start_time
      addr = int(addr)
      data = data.rstrip().decode("hex")

      # wait for the correct moment to send the message
      tdiff = time.time() - t
      while (tdiff <= 0):
          tdiff = time.time() - t
      if tdiff > .1: print "lagged {}".format(tdiff)

      p.can_send(addr, data, bus)
      if DEBUG: print line

  print "\nDone!"
  p.close()

if __name__ == "__main__":
  main()
