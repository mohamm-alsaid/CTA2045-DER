#! /bin/python3
from pycta2045 import cta2045device as device

dev = device.CTA2045Device(mode=device.DCM,comport='/dev/ttyS7')
dev.run()
