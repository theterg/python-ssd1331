''' Python interface to an SSD1331 OLED display controller

Based heavily on work from ADAFRUIT:
https://github.com/adafruit/Adafruit-SSD1331-OLED-Driver-Library-for-Arduino/
'''
import spidev
import sys
import time
import RPi.GPIO as gpio


def color656(r, g, b):
    c = 0
    c = r >> 3;
    c <<= 6;
    c |= g >> 2;
    c <<= 5;
    c |= b >> 3;
    return c
    

class SSD1331:
    INIT_SEQUENCE = [
        0xAE, 0xA0, 0x72, 0xA1, 0x00, 0xA2, 0x00, 0xA4, 0xA8, 0x3F, 0xAD, 0x8E,
        0xB0, 0x0B, 0xB1, 0x31, 0xB3, 0xF0, 0x8A, 0x64, 0x8B, 0x78, 0x8C, 0x64,
        0xBB, 0x3A, 0xBE, 0x3E, 0x87, 0x06, 0x81, 0x91, 0x82, 0x50, 0x83, 0x7D,
        0xAF
    ]
    COMMAND = gpio.LOW
    DATA = gpio.HIGH

    def __init__(self, dc=17, rst=18, cs=0):
        self.rst = rst
        self.dc = dc
        self.cs = cs
        # Setup GPIO
        gpio.setmode(gpio.BCM)
        gpio.setup(self.dc, gpio.OUT)
        gpio.output(self.dc, gpio.LOW)
        gpio.setup(self.rst, gpio.OUT)
        gpio.output(self.rst, gpio.HIGH)
        # Setup SPI
        self.open_spi() 
        # init self
        self.init()
        # Blank the screen
        self.fillScreen(0, 0, 0)

    def open_spi(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 3
        self.spi.max_speed_hz = 16000000
        self.spi.cshigh = False

    def write_command(self, data):
        gpio.output(self.dc, self.COMMAND)
        if isinstance(data, list) or isinstance(data, tuple):
            self.spi.xfer(data)
        else:
            self.spi.xfer([data])

    def write_data(self, data):
        gpio.output(self.dc, self.DATA)
        if isinstance(data, list) or isinstance(data, tuple):
            self.spi.xfer(data)
        else:
            self.spi.xfer([data])
    
    def init(self):
        # Toggle RST
        # HACK - using the gpio driver unsets the CS pin's alternate function
        # Instead of sorting out how to re-set it (not possible using RPi.GPIO),
        # we'll use the SPI driver to hackily toggle the CS pin
        # Set CS pin low
        self.spi.cshigh = True
        self.spi.xfer([0])
        time.sleep(0.1)
        gpio.output(self.rst, gpio.LOW)
        time.sleep(0.5)
        gpio.output(self.rst, gpio.HIGH)
        time.sleep(0.5)
        # Set CS pin high
        self.spi.cshigh = False
        self.spi.xfer([0])
        time.sleep(0.1) 
        # Send init sequence
        # need to do it 1 byte at a time otherwise CS isn't actually toggled
        for byte in self.INIT_SEQUENCE:
            self.write_command(byte)

    def goTo(self, x, y):
        self.write_command([0x15, x, 95, 0x75, y, 63])

    def drawPixel(self, x, y, r, g, b):
        self.goTo(x, y)
        c = color656(r, g, b)
        self.write_data([(c >> 8) & 0xFF, c & 0xFF])

    def drawLine(self, x0, x1, y0, y1, r, g, b):
        c = color656(r, g, b)
        self.write_command([0x21, x0 & 0xFF, y0 & 0xFF, x1 & 0xFF, (y1 & 0xFF)])
        self.write_command([(c >> 11) << 1, (c >> 5) & 0x3F, (c << 1) & 0x3F])

    def fillScreen(self, r, g, b):
        for y in range(64):
            self.drawLine(0, 96, y, y, r, g, b)

    def clearAll(self):
        self.fillScreen(0, 0, 0)

    def test(self):
        self.fillScreen(0,0,0)
        self.fillScreen(255,0,0)
        self.fillScreen(0,255,0)
        self.fillScreen(0,0,255)
        self.fillScreen(255,255,255)
