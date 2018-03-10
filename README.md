# ScreenColor
The ***ScreenColor*** module provides helpful methods for calculating the _average_ color of the screen. 

Intended for use with LIFX Lights.

**Note** This is NOT an API for LIFX LAN communication. For that, check out the extensive [lifxlan](https://github.com/mclarkk/lifxlan) package



## References:
---
[LIFX forums for packet building](https://community.lifx.com/t/building-a-lifx-packet/59/3)

[colorsys package for pixel color data and conversions](https://docs.python.org/2/library/colorsys.html)

## How to use:

To use this module, 
simply instanstantiate the ScreenColor class by providing the screen's pixel width, pixel height, pixel processing interval, duration, and kelvin (0-9000)

```python
"""
Attributes:
    start_x: starting x coordinate  (0)
    end_x: ending x coordinate (1920)
    start_y: staring y coordinate (0)
    end_y: ending y coordinate (1080)
    jump: the interval of pixels to process  (Default is 1: every pixel on the screen is processed)
    duration: the duration of color change
"""
screen_color = ScreenColor(0, 1920, 0, 1080, 100, 500, 4500)
# Get the average color of the screen, returns an HSBKD tuple
# (Hue, Saturation, Brightness, Kelvin, Duration)
screen_color.average_color()
```

After obtaining the HSBKD value, insert the value into your packet's payload (See LIFX forum post above)