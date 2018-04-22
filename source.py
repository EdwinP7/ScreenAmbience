import sys
from lights import message
from screen.colors import ScreenColor
from lights.strip import LightStrip
from screen import ratios
from time import process_time
    
def stream_lights(screen_width, screen_height, light):
    width = screen_width / light.zones
    screen_spaces = []
    for zone in range(light.zones):
        screen_color = ScreenColor(zone*width, (zone+1)*width, 0, screen_height, 1, 450, 4500)
        screen_spaces.append(screen_color)

    while True:
        for i, space in enumerate(screen_spaces):
            message.set_color(space.average_color(), i, i+1)

if __name__ == '__main__':
    try:
        light_strip_mac = sys.argv[1]
    except IndexError:
        print('Enter your light strip\'s mac address as an arguement.')
        print('Example: python source.py <MAC_ADDRESS>.')
        exit()
    light = LightStrip(light_strip_mac, 5)
    stream_lights(*ratios.SIXTEEN_BY_NINE, light)