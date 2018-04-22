from ctypes import windll

def get_screen_resolution():
    return (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))

def get_transformed_ratio(x, y):
    width, height = get_screen_resolution()
    
    if width/height == 

TWENTY_ONE_BY_NINE = (168, 72)
SIXTEEN_BY_NINE = (128, 72)

