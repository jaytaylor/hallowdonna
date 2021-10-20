#!/usr/bin/env python

import signal
import sys
import time

import RPi.GPIO as GPIO

def sig_handler(signum, frame):
    print('signal caught: %s -- goodbye!' % (signum,))
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)

LED_PIN = 17
SWITCH_PIN = 26

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        #inp = GPIO.input(SWITCH_PIN)
        #print('inp=%s' % (inp,))
        #while not inp:
        #    pass
        #while not GPIO.input(SWITCH_PIN):
        #    pass
        GPIO.wait_for_edge(SWITCH_PIN, GPIO.RISING)
        print("LED on")
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
        print("LED off")
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
finally:
    GPIO.cleanup()

