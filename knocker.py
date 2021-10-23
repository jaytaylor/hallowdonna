#!/usr/bin/env python

import time

import RPi.GPIO as GPIO

POWER_ON_DURATION = 50
MIN_INTERVAL_SECS = 10

# n.b. GPIO pinout diagram for RPi4 boards:
#      https://www.tomshardware.com/reviews/raspberry-pi-gpio-pinout,6122.html

LIGHTORAMA_PIN = 17

DOORBELL_PIN = 26

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

GPIO.setup(LIGHTORAMA_PIN, GPIO.OUT)

GPIO.setup(DOORBELL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last_start_ts = 0
#last_end_ts = 0

def my_callback(channel):
    global last_start_ts #, last_end_ts

    if time.time() - last_start_ts < POWER_ON_DURATION + MIN_INTERVAL_SECS:
        print("It's too soon to run again, sorry charlie!")
        return

    last_start_ts = time.time()

    print("Doorbell press detected, activating light-o-rama")
    GPIO.output(LIGHTORAMA_PIN, GPIO.LOW)
    time.sleep(50)
    print("Deactivating light-o-rama")
    GPIO.output(LIGHTORAMA_PIN, GPIO.HIGH)

    last_end_ts = time.time()

GPIO.output(LIGHTORAMA_PIN, GPIO.HIGH)
GPIO.add_event_detect(DOORBELL_PIN, GPIO.RISING, callback=my_callback)

try:
    while True:
        time.sleep(60)
finally:
    GPIO.cleanup()

