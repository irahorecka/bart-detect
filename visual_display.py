"""
A .py file to select various options
of visual displays. A child script of
bart_detect.py
"""
import RPi.GPIO as gpio
import smbus
import time

class LED:
    def __init__(self, compass):
        self.compass = compass
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)

    def led_lights(self):
        """
        A function to start LED sequence.
        The function takes a str cardinal direction
        as its argument.
        """
        led_dir = [27, 23, 17, 18]
        led_dir = led_dir if self.compass.lower() == 'south' else led_dir[::-1]
        for i in led_dir:
            gpio.setup(i, gpio.OUT)
        for i in range(35): # number of flashes
            for index, j in enumerate(led_dir):
                gpio.output(j, True)
                if index == 3:
                    gpio.output(led_dir[0], False)
                time.sleep(.1)
            for index, k in enumerate(led_dir):
                if index == 0:
                    continue
                gpio.output(k, False)
                time.sleep(.1)
        gpio.cleanup()


class LCD:
    # Define some device parameters
    I2C_ADDR  = 0x27 # I2C device address
    LCD_WIDTH = 16   # Maximum characters per line
    # Define some device constants
    LCD_CHR = 1 # Mode - Sending data
    LCD_CMD = 0 # Mode - Sending command
    LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
    LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
    LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line
    LCD_BACKLIGHT  = 0x08  # On
    #LCD_BACKLIGHT = 0x00  # Off
    ENABLE = 0b00000100 # Enable bit
    # Timing constants
    E_PULSE = 0.0005
    E_DELAY = 0.0005
    #Open I2C interface
    #bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
    bus = smbus.SMBus(1) # Rev 2 Pi uses 1

    def __init__(self, stations, repetition):
        self.stations = stations
        if not isinstance(repetition, int):
            raise TypeError("repetition must be set to an integer")
        else:
            self.rep = repetition
        self.lcd_init()

    def lcd_init(self):
        # Initialise display
        self.lcd_byte(0x33,self.LCD_CMD) # 110011 Initialise
        self.lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
        self.lcd_byte(0x28,self.LCD_CMD) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display
        time.sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command
        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits<<4) & 0xF0) | self.LCD_BACKLIGHT
        # High bits
        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)
        # Low bits
        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        # Toggle enable
        time.sleep(self.E_DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(self.E_PULSE)
        self.bus.write_byte(self.I2C_ADDR,(bits & ~self.ENABLE))
        time.sleep(self.E_DELAY)

    def lcd_string(self, message, line):
        # Send string to display
        message = message.center(self.LCD_WIDTH," ")
        self.lcd_byte(line, self.LCD_CMD)
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]),self.LCD_CHR)

    def train_detail(self, line, no_cars):
        try:
            no_cars = int(no_cars)
            for i in range(self.rep):
                self.lcd_string("Approaching from", self.LCD_LINE_2)
                self.lcd_string("{}".format(self.stations), self.LCD_LINE_1)
                time.sleep(2)

                self.lcd_string("{}".format(line.title()), self.LCD_LINE_1)
                self.lcd_string("{} car train".format(no_cars), self.LCD_LINE_2)
                time.sleep(2)
        except Exception as error:
            print(error)
        finally:
            self.lcd_byte(0x01, self.LCD_CMD)