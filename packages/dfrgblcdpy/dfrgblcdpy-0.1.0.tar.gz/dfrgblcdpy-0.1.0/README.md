# DFRGBLCDpy

![Build status](https://github.com/tomplus/DFRGBLCDpy/workflows/Tests/badge.svg)
![PyPI version](https://img.shields.io/pypi/v/dfrgblcdpy)

Python library to control DFRobot Gravity I2C LCD1602 with RGB Backlight Display or similar.

## About

This library is based on official library [DFRobot_RGBLCD1602](https://github.com/DFRobot/DFRobot_RGBLCD1602)
to control [DFRobot Gravity I2C LCD1602](https://www.dfrobot.com/product-1609.html). The offical library uses
deprecated _wiringpi_, but this uses _smbus_ and it's released as a standalone library.

Feel free to use and enjoy your LCD.

## Getting Started

### Requirements

1. Connect your LCD to RPi via I2C pinouts, it accepts 5V. 

2. Enable I2C on your RPi (using _raspi-config_)

3. Install (_apt-get install i2c-tools_) and use _i2cdetect_ to check addresses.
   
   Example:
   ```
    $ i2cdetect -y 1

        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- 2d -- -- 
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- 3e -- 
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    70: -- -- -- -- -- -- -- --   
    ```
    (the module uses 2 addresses)
    
    Alternatively you can assume that the LCD has an address **0x3e**
    and RGB's address depends on the hardware version: **0x2d** (RGB V2.0), 
    0x60 (RGB V1.0), 0x6b (V1.1), 0x30 (V1.0).

## Installation

```
pip install dfrgblcdpy
```

## Examples

```python
from dfrgblcdpy import DFRRGBLCDPY

# default addresses
lcd = DFRRGBLCDPY()

# set white backlight
lcd.set_color_white()

# first line
lcd.print_out("Hello!")

# second line
lcd.set_cursor(0, 1)
lcd.print_out("World!")
```

## Documentation

See `docs/dfrgblcdpy.html`

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.
