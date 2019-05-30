#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TheMakerspaceProject
This program searches for the valid fingerprint and runs the servo if found a valid one
"""
import RPi.GPIO as GPIO
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from time import sleep

########################################
# the servo initialization part

GPIO.setmode(GPIO.BOARD) # setting  naming mode to GPIO pin configuration

GPIO.setup(03,GPIO.OUT) # initializing pin 3 to PWM signals

pwm = GPIO.PWM(03 , 50) # pwm on pin3 at 50 Hertz
pwm.start(0) # start it with 0 duty cycles so it doesn't set any angles

# we have a little bit of math to calculate angle which I will put it up below

# function here is called AngleCalc
def AngleCalc(angle):
        duty = angle / 18 + 2 # to convert the angle to duty cycles for PWM
        GPIO.output(03,True) # to power up the servo
        pwm.ChangeDutyCycle(duty) # duty cycle fed to change PWM accordingly
        sleep(1) # good night for a sec
        pwm.ChangeDutyCycle(2) # bring back to closing the lid
        sleep(1)
        GPIO.output(03 , False) # stop the PWM
## Search for a finger
##

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
#print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to search the finger and calculate hash
try:
    print('Waiting for finger...')

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    ## Searchs template
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to search the finger and calculate hash
try:
    print('Waiting for finger...')

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    ## Searchs template
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if ( positionNumber == -1 ):
        print('No match found!')
        print(" Access DENIED !!")
        exit(0)
    else:
        AngleCalc(90)
        print("Access GRANTED")
        pwm.stop()
        GPIO.cleanup()

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    print("Access Denied")
    exit(1)


