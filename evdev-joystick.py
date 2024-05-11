# python -m evdev.evtest
import evdev
import math
import numpy as np
import time
from evdev import categorize, ecodes, KeyEvent
from numpy import interp
from smbus2 import SMBus

CAM_DEFAULT_I2C_ADDRESS = 0x34
MOTOR_TYPE_ADDR = 20
MOTOR_FIXED_SPEED_ADDR = 51
MOTOR_ENCODER_POLARITY_ADDR = 21
MOTOR_FIXED_PWM_ADDR = 31
MOTOR_ENCODER_TOTAL_ADDR = 60
ADC_BAT_ADDR = 0
MOTOR_TYPE_JGB37_520_12V_110RPM = 3

bus = SMBus(1)
bus.write_byte_data(CAM_DEFAULT_I2C_ADDRESS, MOTOR_TYPE_ADDR, MOTOR_TYPE_JGB37_520_12V_110RPM)
bus.write_byte_data(CAM_DEFAULT_I2C_ADDRESS, MOTOR_ENCODER_POLARITY_ADDR, 0)
bat = bus.read_word_data(CAM_DEFAULT_I2C_ADDRESS, ADC_BAT_ADDR)
print("BAT:", bat)

def process(event, x):
    if event.type == ecodes.EV_ABS:
        e = categorize(event)
        print(x, e.event.code, e.event.value)

        if x%3 == 0:
            bus.write_i2c_block_data(CAM_DEFAULT_I2C_ADDRESS, MOTOR_FIXED_SPEED_ADDR, [0, -0, -0, 0])
        else:
            bus.write_i2c_block_data(CAM_DEFAULT_I2C_ADDRESS, MOTOR_FIXED_SPEED_ADDR, [10, -10, -10, 10])

def main():
    x=0
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.path, device.name, device.phys)
        if 'Xbox Wireless Controller' != device.name:
            continue
        for event in device.read_loop():
            process(event, x)
            time.sleep(1)
            x+=1

if __name__ == "__main__":
    main()
