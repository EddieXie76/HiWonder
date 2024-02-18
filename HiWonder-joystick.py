import math
from numpy import interp
from smbus2 import SMBus
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
bat = bus.read_word_data(CAM_DEFAULT_I2C_ADDRESS, ADC_BAT_ADDR)
print("BAT:", bat)

pygame.init()

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

deadZone=0.2
def map_motor(input):
    if input > deadZone:
        return round(interp(input, [deadZone, 1], [0, 100]))
    if input < -deadZone:
        return round(interp(input, [-1, -deadZone], [-100, 0]))
    return 0

def main():
    # Set the width and height of the screen (width, height), and name the window.
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Joystick example")

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Get ready to print.
    text_print = TextPrint()

    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(f"Rumble effect played on joystick {event.instance_id}")

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        text_print.reset()

        joystick_count = pygame.joystick.get_count()

        if joystick_count == 0:
            continue
        joystick = joysticks[0]
        
        x = joystick.get_axis(0) * 0.8
        y = -joystick.get_axis(1)
        turn = joystick.get_axis(2) * 0.7
        
        theta = math.atan2(y, x)
        power = math.hypot(x, y)
        
        sin = math.sin(theta - math.pi/4)
        cos = math.cos(theta - math.pi/4)
        maximum = max(abs(sin), abs(cos))
        
        leftFront = power * cos / maximum + turn
        rightFront = power * sin / maximum - turn
        leftRear = power * sin / maximum + turn
        rightRear = power * cos / maximum - turn
        
        if power + abs(turn) > 1:
            leftFront /= power + turn
            rightFront /= power - turn
            leftRear /= power + turn
            rightRear /= power - turn
            
            
        motor = [map_motor(leftFront), map_motor(rightFront), map_motor(leftRear), map_motor(rightRear)]

        screen.fill((round(interp(x, [-100, 100], [50, 255])), round(interp(y, [-100, 100], [50, 255])), round(interp(turn, [-100, 100], [50, 255]))))
        
        text_print.tprint(screen, f"X: {x}")
        text_print.tprint(screen, f"Y: {y}")
        text_print.tprint(screen, f"Turn: {turn}")
        text_print.tprint(screen, f"Theta: {theta}")
        text_print.tprint(screen, f"Power: {power}")
        text_print.tprint(screen, f"Sin: {sin}")
        text_print.tprint(screen, f"Cos: {cos}")
        text_print.tprint(screen, f"LeftFront: {leftFront}")
        text_print.tprint(screen, f"RightFront: {rightFront}")
        text_print.tprint(screen, f"LeftRear: {leftRear}")
        text_print.tprint(screen, f"LeftRear: {rightRear}")
        text_print.tprint(screen, f"Motor: {motor}")

        pygame.draw.circle(screen, [0, 0, 200], [400, 400], 300, width = 5)
        pygame.draw.circle(screen, [200, 0, 0], [400 + math.cos(theta) * power * 200, 400 - math.sin(theta) * power * 200], 50)
        #pygame.draw.circle(screen, [200, 0, 0], [math.theta, 400], power * 100)
        

        bus.write_i2c_block_data(CAM_DEFAULT_I2C_ADDRESS, MOTOR_FIXED_SPEED_ADDR, motor)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 30 frames per second.
        clock.tick(30)


if __name__ == "__main__":
    main()
    pygame.quit()