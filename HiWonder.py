from smbus2 import SMBus
import time
import pygame

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

pygame.init()
window = pygame.display.set_mode((300,300))
pygame.display.set_caption("Pygame Demonstration")

mainloop=True
MIN=20
MAX=100
s=MIN
a=s
control = [0, 0, 0, 0]
while mainloop:

    pygame.time.delay(10)
    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            mainloop=False
        
        if event.type==pygame.KEYDOWN:
            control = [0, 0, 0, 0]
            if event.key==264 or event.key==119:#UP w
                control = [a, a, a, a]
            if event.key==258 or event.key==120 or event.key==115:#DOWN x s
                control = [-a, -a, -a, -a]
            if event.key==260 or event.key==97:#LEFT a
                control = [-a, a, a, -a]
            if event.key==262 or event.key==100:#RIGHT d
                control = [a, -a, -a, a]
            if event.key==263 or event.key==113:#HOME q
                control = [0, a, a, 0]
            if event.key==259 or event.key==99:#PAGE DOWN c
                control = [0, -a, -a, 0]
            if event.key==265 or event.key==101:#PAGE UP e
                control = [a, 0, 0, a]
            if event.key==257 or event.key==122:#END z
                control = [-a, 0, 0, -a]
            if event.key==267 or event.key==91:#/ [
                control = [-a, a, -a, a]
            if event.key==268 or event.key==93:#* ]
                control = [a, -a, a, -a]            
            if event.key==270 or event.key==61:#+
                s += 5
                s = min(s, MAX)
            if event.key==269 or event.key==45:#-
                s -= 5
                s = max(s, MIN)
            print(event.key, ", ", a, ", ", s, ", ", control)
            bus.write_i2c_block_data(CAM_DEFAULT_I2C_ADDRESS, MOTOR_FIXED_SPEED_ADDR, control)
                    
        if event.type==pygame.KEYUP:
            control = [0, 0, 0, 0]
            a=s
            print(event.key, ", ", a, ", ", s, ", ", control)
            bus.write_i2c_block_data(CAM_DEFAULT_I2C_ADDRESS, MOTOR_FIXED_SPEED_ADDR, control)
            
        

pygame.quit()
  

