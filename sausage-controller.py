from unittest import case
import RPi.GPIO as GPIO
import time
import sys
import os
#!/usr/bin/env python3

# Macro definitions (but in python)
FRONT_GPIO = 4
LEFT_GPIO = 17
RIGHT_GPIO = 27
BOTTOM_GPIO = 22
BACK_GPIO = 10

FRONT_LED_GPIO = 5
LEFT_LED_GPIO = 6
RIGHT_LED_GPIO = 13
BACK_LED_GPIO = 19

# BOTTOM_LED_GPIO = 26

NO_KEY = 0x00
W_KEY = 0x1a
A_KEY = 0x04
S_KEY = 0x16
D_KEY = 0x07
J_KEY = 0x0d

# Flags
front_pressed = False
back_pressed = False
left_pressed = False
right_pressed = False


def gpio_setup():
    # GPIO setup
    GPIO.setmode(GPIO.BCM)

    # inputs
    GPIO.setup(FRONT_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
    GPIO.setup(LEFT_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
    GPIO.setup(RIGHT_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
    GPIO.setup(BOTTOM_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
    GPIO.setup(BACK_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

    # outputs
    GPIO.setup(FRONT_LED_GPIO , GPIO.OUT)
    GPIO.setup(LEFT_LED_GPIO , GPIO.OUT)
    GPIO.setup(RIGHT_LED_GPIO , GPIO.OUT) 
    # GPIO.setup(BOTTOM_LED_GPIO , GPIO.OUT)
    GPIO.setup(BACK_LED_GPIO , GPIO.OUT)

    #Events
    GPIO.add_event_detect(FRONT_GPIO, GPIO.RISING, callback=callback_sides)
    GPIO.add_event_detect(LEFT_GPIO, GPIO.RISING, callback=callback_sides)
    GPIO.add_event_detect(RIGHT_GPIO, GPIO.RISING, callback=callback_sides)
    GPIO.add_event_detect(BACK_GPIO, GPIO.RISING, callback=callback_sides)


def current_milli_time():
    return round(time.time() * 1000)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())


# Callbacks
def callback_sides(channel):
    if (channel == FRONT_GPIO):
        front_pressed = True
    elif (channel == BACK_GPIO):
        back_pressed = True
    elif (channel == LEFT_GPIO):
        left_pressed = True
    elif (channel == RIGHT_GPIO):
        right_pressed = True


millis = current_milli_time()

def controller_loop():
    if (current_milli_time-millis >= 50):
        millis = current_milli_time()
        front_pressed = False
        back_pressed = False
        right_pressed = False
        left_pressed = False
        GPIO.output(FRONT_LED_GPIO, GPIO.LOW)
        GPIO.output(BACK_LED_GPIO,GPIO.LOW)
        GPIO.output(RIGHT_LED_GPIO,GPIO.LOW)
        GPIO.output(LEFT_LED_GPIO,GPIO.LOW)

    if GPIO.input(BOTTOM_GPIO):
        # GPIO.output(FRONT_LED_GPIO, GPIO.HIGH)
        # GPIO.output(BACK_LED_GPIO, GPIO.HIGH)
        # GPIO.output(RIGHT_LED_GPIO, GPIO.HIGH)
        # GPIO.output(LEFT_LED_GPIO, GPIO.HIGH)
        write_report(J_KEY)
        write_report(NO_KEY)
    if front_pressed:
        GPIO.output(FRONT_LED_GPIO, GPIO.HIGH)
        write_report(W_KEY)
        write_report(NO_KEY)
    if back_pressed:
        GPIO.output(BACK_LED_GPIO, GPIO.HIGH)
        write_report(S_KEY)
        write_report(NO_KEY)
    if left_pressed:
        GPIO.output(LEFT_LED_GPIO, GPIO.HIGH)
        write_report(A_KEY)
        write_report(NO_KEY)
    if right_pressed:
        GPIO.output(RIGHT_LED_GPIO, GPIO.HIGH)
        write_report(D_KEY)
        write_report(NO_KEY)

if __name__ == "__main__":
    try:
        gpio_setup()
        while True:
            print("I'm here")
            controller_loop()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    finally:
        GPIO.cleanup()
