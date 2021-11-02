#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""bare_bones_fancy.py - Solves the problem nicely!"""

import argparse
import logging
import sys
import time

import RPi.GPIO as GPIO

# Module-level logger.
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s [%(filename)s:%(lineno)d]', datefmt='%Y-%m-%dT%H:%M:%S%z')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# <Config>
MIN_INTERVAL_SECS = 10

POWER_ON_DURATION = 50

DOUBLE_TAP_RANGE_MIN_DURATION = 0.5
DOUBLE_TAP_RANGE_MAX_DURATION = 10.0
# </Config>

# n.b. GPIO pinout diagram for RPi4 boards:
#      https://www.tomshardware.com/reviews/raspberry-pi-gpio-pinout,6122.html

LIGHTORAMA_PIN = 17

DOORBELL_PIN = 26

def parse_flags(args):
    """
    Parse command-line arguments.

    :param args: List of command-line arguments to parse.

    :return: object containing argparse result.
    """
    # n.b. Description is automatically pulled from module top docstring comment.
    parser = argparse.ArgumentParser(description=__doc__, argument_default=False)
    parser.add_argument('-q', '--quiet', help='Reduce log output to only display errors.', action='store_true')
    parser.add_argument('-v', '--verbose', help='Activate verbose logging output for debugging.', action='store_true')
    flags = parser.parse_args(args)

    if flags.quiet and flags.verbose:
        raise Exception('Invalid flag combination, select one of -q/--quiet, -v/--verbose')
    elif flags.quiet:
        logger.setLevel(logging.ERROR)
    elif flags.verbose:
        logger.setLevel(logging.DEBUG)

    return flags

last_start_ts = 0
#last_end_ts = 0
last_press_ts = 0
press_count = 0

def my_callback(channel):
    global last_start_ts, last_press_ts, press_count #, last_end_ts
#    logger.info('my_callback invoked')
#
    if time.time() - last_start_ts < POWER_ON_DURATION + MIN_INTERVAL_SECS:
        logger.info("It's too soon to run again, sorry charlie!")
        last_press_ts = time.time()
        return
#
#    duration_since_last_press = time.time() - last_press_ts
#    if press_count != 0 and duration_since_last_press > DOUBLE_TAP_RANGE_MAX_DURATION:
#        logger.info('Resetting press coun to 0')
#        press_count = 0
#
#    if duration_since_last_press < DOUBLE_TAP_RANGE_MIN_DURATION:
#        logger.info('Ignoring faulty press (%ss is suspiciously soon since the last event) press_count=%s', duration_since_last_press, press_count)
#        return
#
#    if duration_since_last_press >= DOUBLE_TAP_RANGE_MIN_DURATION:
#        press_count += 1
#        logger.info('Press detected press_count=%s', press_count)
#        last_press_ts = time.time()
#
#    #if duration_since_last_press < DOUBLE_TAP_RANGE_MAX_DURATION:
#    #    logger.info('Second press detected')
#    #    return
#    if press_count == 2:
    if 1 == 1:
        logger.info('Triggering because press_count=%s', press_count)
        #press_count = 0

        last_start_ts = time.time()

        logger.info("Doorbell press detected, activating light-o-rama for the next %ss", POWER_ON_DURATION)
        GPIO.output(LIGHTORAMA_PIN, GPIO.LOW)
        time.sleep(POWER_ON_DURATION)
        logger.info("Deactivating light-o-rama")
        GPIO.output(LIGHTORAMA_PIN, GPIO.HIGH)

        #last_end_ts = time.time()

def main(args):
    flags = parse_flags(args)

    logger.info('%s starting up', __name__)

    try:
        GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)

        GPIO.setup(LIGHTORAMA_PIN, GPIO.OUT)

        GPIO.setup(DOORBELL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.output(LIGHTORAMA_PIN, GPIO.HIGH)
        GPIO.add_event_detect(DOORBELL_PIN, GPIO.RISING, callback=my_callback, bouncetime = 20)

        while True:
            time.sleep(60)
    except BaseException:
        logging.exception('Caught exception in main')
        return 1
    finally:
        GPIO.cleanup()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
