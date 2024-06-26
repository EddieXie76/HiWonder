from smbus2 import SMBus
import time

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
b = bus.read_word_data(CAM_DEFAULT_I2C_ADDRESS, ADC_BAT_ADDR)
print("BAT:", b)

def loop():
    bus.write_i2c_block_data(CAM_DEFAULT_I2C_ADDRESS, MOTOR_FIXED_SPEED_ADDR, [5, -5, -5, 5])
    time.sleep(0.1)
    bus.write_i2c_block_data(CAM_DEFAULT_I2C_ADDRESS, MOTOR_FIXED_SPEED_ADDR, [0, 0, 0, 0])
    time.sleep(0.1)

while(True):
    try:
        loop()
    except OSError as e:
        print(e)
