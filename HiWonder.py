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
b = bus.read_word_data(CAM_DEFAULT_I2C_ADDRESS, ADC_BAT_ADDR)
print("BAT:", b)

pygame.init()
window = pygame.display.set_mode((300,300))
pygame.display.set_caption("Pygame Demonstration")

mainloop=True
a=10
control = [0, 0, 0, 0]
while mainloop:

    pygame.time.delay(10)
    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            mainloop=False
        
        if event.type==pygame.KEYDOWN:
            print(event.key, " ", a)

            if event.key==264:#UP
                control = [a, a, a, a]
            if event.key==258:#DOWN
                control = [-a, -a, -a, -a]
            if event.key==260:#LEFT
                control = [-a, a, a, -a]
            if event.key==262:#RIGHT
                control = [a, -a, -a, a]
            if event.key==263:#HOME
                control = [0, a, a, 0]
            if event.key==259:#PAGE DOWN
                control = [0, -a, -a, 0]
            if event.key==265:#PAGE UP
                control = [a, 0, 0, a]
            if event.key==257:#END
                control = [-a, 0, 0, -a]
            if event.key==267:#/
                control = [-a, a, -a, a]
            if event.key==268:#*
                control = [a, -a, a, -a]
    
            bus.write_i2c_block_data(CAM_DEFAULT_I2C_ADDRESS, MOTOR_FIXED_SPEED_ADDR, control)


        if event.type==pygame.KEYUP:
            bus.write_i2c_block_data(CAM_DEFAULT_I2C_ADDRESS, MOTOR_FIXED_SPEED_ADDR, [0, 0, 0, 0])
            a=10

pygame.quit()
  

