import colorsys
from PIL import ImageGrab, Image
from random import randint

RGB_SCALE = 255


class ScreenColor(object):

    """
    Contains information about the screen and pixels to be processed
    
    This class has information about which pixels will
    be processed from the screen as well as methods for data
    about the colors on the screen.

    Attributes (Default):
        start_x: starting x coordinate  (0)
        end_x: ending x coordinate (1920)
        start_y: staring y coordinate (0)
        end_y: ending y coordinate (1080)
        jump: the interval of pixels to process (1: every pixel on the screen is processed)
        duration: the duration of color change (100)
        kelvin: the warmth-coolness of the color (0-9000)
    """

    def __init__(self, start_x=0, end_x=1920, start_y=0, end_y=1080, jump=1, duration=100, kelvin=4500):
        self.start_x = int(start_x)
        self.end_x = int(end_x)
        self.start_y = int(start_y)
        self.end_y = int(end_y)
        self.width = self.get_width()
        self.height = self.get_height()
        self.jump = jump
        self.pixels = self.pixel_count()
        self.duration = duration
        self.kelvin = kelvin

    def pixel_count(self):
        return (self.height/self.jump) * (self.width/self.jump)
    
    def get_width(self):
        return (self.end_x - self.start_x)
    
    def get_height(self):
        return (self.end_y - self.start_y)


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
        # Resize to 128x72 pixels image. Lower
        image = image.resize((128,72))

        # Get average RGB Values
        for y in range(self.start_y, self.end_y, self.jump):
            for x in range(self.start_x, self.end_x, self.jump):
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
        # Converts HSV to HSBK (Kelvin is set to 50% as there is no appropriate conversion)
        h, s, v = colorsys.rgb_to_hsv(*rgb_color)
        #print(h, s, v)
        h = int(float(h) * 65535)
        s = int(float(s) * 65535)
        b = int(float(v) * 65535)
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