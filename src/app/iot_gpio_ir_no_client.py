import time
from gpiozero import LED, MotionSensor, Buzzer
motion_sensor = MotionSensor(4)
led = LED(2)
buzzer = Buzzer(17)

try:
    while True:
        motion_sensor.wait_for_active()
        buzzer.on()
        led.blink(n=5)
        print("Motion detected")
        time.sleep(.5)
        buzzer.off()
        time.sleep(2)
finally:
    buzzer.off()
    led.off()

