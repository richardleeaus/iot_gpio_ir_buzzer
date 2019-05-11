import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)  # IR
GPIO.setup(3, GPIO.OUT)  # LED
GPIO.setup(11, GPIO.OUT)  # BUZZER

try:
    while True:
        i = GPIO.input(7)
        if i==0:
            GPIO.output(3,0)
            print("No one here")
        else:
            GPIO.output(11, True)
            GPIO.output(3,1)
            print("Motion detected")
            time.sleep(.5)
            GPIO.output(11, False)
        time.sleep(2)
finally:
    GPIO.output(11, False)

