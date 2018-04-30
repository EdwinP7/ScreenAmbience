import sys
from ScreenAmbience.colors import ScreenRegion
from ScreenAmbience.strip import LightStrip
from ScreenAmbience.ratios import get_transformed_ratio
    
def get_color_regions(zones, screen_width, screen_height):
    width = screen_width / zones
    screen_spaces = []
    for zone in range(zones):
        screen_color = ScreenRegion(zone*width, (zone+1)*width, 0, screen_height, (screen_width, screen_height))
        screen_spaces.append(screen_color)
    return screen_spaces

def stream_lights(light):
    color_regions = get_color_regions(light.zones, *get_transformed_ratio())
    while True:
        for i, region in enumerate(color_regions):
            light.set_light_color(region.get_average_color(), 200, i, i)

if __name__ == '__main__':
    try:
        light_strip_mac = sys.argv[1]
        light_strip_zones = int(sys.argv[2])
    except IndexError:
        print('Enter your light strip\'s mac address and number of zones. \nExample: python source.py "MA:CA:DD:RE:SS" 8')
        exit() 
    light = LightStrip(light_strip_mac, light_strip_zones)
    stream_lights(light)