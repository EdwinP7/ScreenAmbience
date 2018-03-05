import colorsys
from PIL import ImageGrab
from random import randint

RGB_SCALE = 255


class ScreenColor(object):

    """
    Contains information about the screen and pixels to be processed
    
    This class has information about which pixels will
    be processed from the screen as well as methods for data
    about the colors on the screen.

    Attributes:
        width:  the width if the screen in pixels  (Default is 1920)
        height: the height of the screen in pixels (Default is 1080)
        jump:   the interval of pixels to process  (Default is 1: every pixel on the screen is processed)
        pixels: the total number of pixels to be processed
    """

    def __init__(self, width=1920, height=1080, jump=1, duration=500, kelvin=4500):
        self.width = width
        self.height = height
        self.jump = jump
        self.pixels = self.pixel_count()
        self.duration = duration
        self.kelvin = kelvin

    def pixel_count(self):
        return (self.height/self.jump) * (self.width/self.jump)

    def average_color(self):
        """
        Returns the 'average' HSBK Value from the screen as a tuple
        ready to be inserted into a LIFX packet's payload
        
        The average screen color is converted from 
        average RGB (Average Red, Average Green, Average Blue) to HSBK (With a Kelvin value of 50%)
        """
        red = 0
        green = 0
        blue = 0
        image = ImageGrab.grab()

        # Get average RGB Values
        for y in range(0, self.height, self.jump):
            for x in range(0, self.width, self.jump):
                r, g, b = image.getpixel((x,y))
                red += r
                green += g
                blue += b

        red /= self.pixels
        green /= self.pixels
        blue /= self.pixels
        # Convert values from the range 0-255 to 0-1
        rgb_color = self.scale_rgb_values((red, green, blue))
        
        hue, saturation, brightness, kelvin = self.convert_rgb_to_hsbk(rgb_color)
        return (hue, saturation, brightness, kelvin, self.duration)

    def convert_rgb_to_hsbk(self, rgb_color):
        # Converts HSL to HSBK (Kelvin is set to 50% as there is no appropriate conversion)
        h, l, s = colorsys.rgb_to_hls(*rgb_color)

        h = int(float(h) * 65535)
        s = int(float(s) * 65535)
        b = int(float(l) * 65535)
        k = int(self.kelvin)
        return (h, s, b, k)

    def scale_rgb_values(self, rgb_color):
        # Set max RGB values
        red, green, blue = rgb_color

        if red > RGB_SCALE:
            red = RGB_SCALE
        if green > RGB_SCALE:
            green = RGB_SCALE
        if blue > RGB_SCALE:
            blue = RGB_SCALE

        return (red/RGB_SCALE, green/RGB_SCALE, blue/RGB_SCALE)