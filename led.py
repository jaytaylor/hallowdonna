#!/usr/bin/env python

#import signal
import sys
import time

import RPi.GPIO as GPIO

#def sig_handler(signum, frame):
#    print('signal caught: %s -- goodbye!' % (signum,))
#    sys.exit(0)
#
#signal.signal(signal.SIGINT, sig_handler)
#signal.signal(signal.SIGTERM, sig_handler)

MIN_INTERVAL_SECS = 10

# n.b. GPIO pinout diagram for RPi4 boards:
#      https://www.tomshardware.com/reviews/raspberry-pi-gpio-pinout,6122.html

LED1_PIN = 2
LED2_PIN = 3
LED3_PIN = 4
LED4_PIN = 17
LED5_PIN = 27

SWITCH_PIN = 26

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

GPIO.setup(LED1_PIN, GPIO.OUT)
GPIO.setup(LED2_PIN, GPIO.OUT)
GPIO.setup(LED3_PIN, GPIO.OUT)
GPIO.setup(LED4_PIN, GPIO.OUT)
GPIO.setup(LED5_PIN, GPIO.OUT)

GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last_run_ts = 0

def my_callback(channel):
    global last_run_ts

    if time.time() - last_run_ts < MIN_INTERVAL_SECS:
        print("It's too soon to run again, sorry charlie!")
        return

    last_run_ts = time.time()

    print("Turning LED1 on")
    GPIO.output(LED1_PIN, GPIO.HIGH)
    time.sleep(1)
    print("Turning LED1 off")
    GPIO.output(LED1_PIN, GPIO.LOW)

    print("Turning LED2 on")
    GPIO.output(LED2_PIN, GPIO.HIGH)
    time.sleep(1)
    print("Turning LED2 off")
    GPIO.output(LED2_PIN, GPIO.LOW)

    print("Turning LED3 on")
    GPIO.output(LED3_PIN, GPIO.HIGH)
    time.sleep(1)
    print("Turning LED3 off")
    GPIO.output(LED3_PIN, GPIO.LOW)

    print("Turning LED4 on")
    GPIO.output(LED4_PIN, GPIO.HIGH)
    time.sleep(1)
    print("Turning LED4 off")
    GPIO.output(LED4_PIN, GPIO.LOW)

    print("Turning LED5 on")
    GPIO.output(LED5_PIN, GPIO.HIGH)
    time.sleep(1)
    print("Turning LED5 off")
    GPIO.output(LED5_PIN, GPIO.LOW)

GPIO.add_event_detect(SWITCH_PIN, GPIO.RISING, callback=my_callback)

try:
    while True:
        time.sleep(60)
        #inp = GPIO.input(SWITCH_PIN)
        #print('inp=%s' % (inp,))
        #while not inp:
        #    pass
        #while not GPIO.input(SWITCH_PIN):
        #    pass
        #GPIO.wait_for_edge(SWITCH_PIN, GPIO.RISING)
        #print("LED on")
        #GPIO.output(LED1_PIN, GPIO.HIGH)
        #time.sleep(1)
        #print("LED off")
        #GPIO.output(LED1_PIN, GPIO.LOW)
        #time.sleep(1)
finally:
    GPIO.cleanup()

