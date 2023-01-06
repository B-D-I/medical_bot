import json
import requests
import datetime
import random
import time
import statistics
from time import sleep
from typing import Union

# Arduino
import serial
USB_PORT = "/dev/ttyACM0"
usb = serial.Serial(USB_PORT, 9600, timeout=2)
usb.flush()         # avoids receiving or sending not useful / complete data




