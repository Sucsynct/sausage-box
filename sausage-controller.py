from unittest import case
import RPi.GPIO as GPIO
import time
import sys
import os
#!/usr/bin/env python3

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

    GPIO.output(FRONT_LED_GPIO, GPIO.LOW)
    GPIO.output(BACK_LED_GPIO,GPIO.LOW)
    GPIO.output(RIGHT_LED_GPIO,GPIO.LOW)
    GPIO.output(LEFT_LED_GPIO,GPIO.LOW)

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
    global front_pressed
    global back_pressed
    global left_pressed
    global right_pressed

    if (channel == FRONT_GPIO):
        front_pressed = True
        # print('front')
    elif (channel == BACK_GPIO):
        back_pressed = True
        # print('back')
    elif (channel == LEFT_GPIO):
        left_pressed = True
        # print('left')
    elif (channel == RIGHT_GPIO):
        right_pressed = True
        # print('right')


millis = current_milli_time()
bottom_pressed = False

def controller_loop():
    global front_pressed
    global back_pressed
    global left_pressed
    global right_pressed
    global millis

    if (current_milli_time() - millis >= 50):
        millis = current_milli_time()
        GPIO.output(FRONT_LED_GPIO, GPIO.LOW)
        GPIO.output(BACK_LED_GPIO,GPIO.LOW)
        GPIO.output(RIGHT_LED_GPIO,GPIO.LOW)
        GPIO.output(LEFT_LED_GPIO,GPIO.LOW)


    # if GPIO.input(BOTTOM_GPIO) and not bottom_pressed:
        # bottom_pressed = True
        # # GPIO.output(FRONT_LED_GPIO, GPIO.HIGH)
        # # GPIO.output(BACK_LED_GPIO, GPIO.HIGH)
        # # GPIO.output(RIGHT_LED_GPIO, GPIO.HIGH)
        # # GPIO.output(LEFT_LED_GPIO, GPIO.HIGH)
        # write_report(J_KEY)
        # write_report(NO_KEY)
    if front_pressed:
        # print(FRONT_LED_GPIO)
        GPIO.output(FRONT_LED_GPIO, GPIO.HIGH)
        write_report(W_KEY)
        write_report(NO_KEY)
        front_pressed = False
    if back_pressed:
        # print(BACK_LED_GPIO)
        GPIO.output(BACK_LED_GPIO, GPIO.HIGH)
        write_report(S_KEY)
        write_report(NO_KEY)
        back_pressed = False
    if left_pressed:
        # print(LEFT_LED_GPIO)
        GPIO.output(LEFT_LED_GPIO, GPIO.HIGH)
        write_report(A_KEY)
        write_report(NO_KEY)
        left_pressed = False
    if right_pressed:
        # print(RIGHT_LED_GPIO)
        GPIO.output(RIGHT_LED_GPIO, GPIO.HIGH)
        write_report(D_KEY)
        write_report(NO_KEY)
        right_pressed = False

if __name__ == "__main__":
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

    NULL_CHAR = chr(0)

    NO_KEY = NULL_CHAR * 2 + chr(0) + NULL_CHAR*5
    W_KEY = NULL_CHAR * 2 + chr(26) + NULL_CHAR*5
    A_KEY = NULL_CHAR * 2 + chr(4) + NULL_CHAR*5
    S_KEY = NULL_CHAR * 2 + chr(22) + NULL_CHAR*5
    D_KEY = NULL_CHAR * 2 + chr(7) + NULL_CHAR*5
    J_KEY = NULL_CHAR * 2 + chr(13) + NULL_CHAR*5

    # Flags
    front_pressed = False
    back_pressed = False
    left_pressed = False
    right_pressed = False


    try:
        gpio_setup()
        millis = current_milli_time()
        while True:
            controller_loop()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    finally:
        GPIO.cleanup()
