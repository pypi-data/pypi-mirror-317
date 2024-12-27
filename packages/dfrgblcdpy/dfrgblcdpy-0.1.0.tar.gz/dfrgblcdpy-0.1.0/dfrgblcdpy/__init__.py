import time
from typing import Any
import smbus


class DFRRGBLCDPY:
    """
    This class provides methods to control a DFRobot LCD with RGB backlight and
    simlar. See example/ to more details.
    """

    # color define
    WHITE = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    REG_MODE1 = 0x00
    REG_MODE2 = 0x01
    REG_OUTPUT = 0x08
    REG_RGB = {
        0x60: [0x04, 0x03, 0x02],
        0x30: [0x06, 0x07, 0x08],
        0x6B: [0x06, 0x05, 0x04],
        0x2D: [0x01, 0x02, 0x03],
    }

    # lcd
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    # flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    def __init__(
        self,
        i2c_line: int = 1,
        rgb_addr: int = 0x2D,
        lcd_addr: int = 0x3E,
        col: int = 16,
        row: int = 2,
    ) -> None:
        """
        Creates an instance of the class.

        :param i2c_line: i2c line
        :param rgb_addr: i2c address of RGB backlight
        :param lcd_addr: ic2 address of LCD
        :param col: number of cols
        :param row: number of rows
        """

        self.rgb_addr = rgb_addr
        self.lcd_addr = lcd_addr
        self.col = col
        self.row = row
        self._show_function = self.LCD_4BITMODE | self.LCD_5x8DOTS
        if row > 1:
            self._show_function |= self.LCD_2LINE
        self._show_control = self.LCD_DISPLAYOFF
        self._show_mode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.bus = smbus.SMBus(i2c_line)
        self._init_device()

    def write(self, data: int) -> None:
        """
        Writes one char.

        :param data: char to write
        """
        self._write_block(self.lcd_addr, 0x40, [data])

    def set_RGB(self, r: int, g: int, b: int) -> None:
        """
        Set backlight colour.

        :param r: red component (0-255)
        :param g: green component (0-255)
        :param b: blue component (0-255)
        """
        if self.rgb_addr == 0x30:
            r = int(r * 192 / 255)
            g = int(g * 192 / 255)
            b = int(b * 192 / 255)

        reg_red, reg_green, reg_blue = self.REG_RGB[self.rgb_addr]

        self._set_reg(reg_red, r)
        self._set_reg(reg_green, g)
        self._set_reg(reg_blue, b)

        if self.rgb_addr == 0x6B:
            self._set_reg(0x07, 0xFF)

    def set_cursor(self, col: int, row: int) -> None:
        """
        Moves cursor to given position.

        :param col: column (0-begin)
        :param row: row (0-first line)
        """
        if row == 0:
            col |= 0x80
        else:
            col |= 0xC0
        self._command(col)

    def clear(self) -> None:
        """
        Clears LCD
        """
        self._command(self.LCD_CLEARDISPLAY)
        time.sleep(0.002)

    def scroll_display_left(self) -> None:
        """
        Scrolls left to display
        """
        self._command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)

    def scroll_display_right(self) -> None:
        """
        Scrolls left to display
        """
        self._command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT)

    def print_out(self, value: Any) -> None:
        """
        Prints values (string or any value which will be converted to string)

        :param value: value to print
        """
        if not isinstance(value, str):
            value = str(value)
        for x in bytearray(value, "utf-8"):
            self.write(x)

    def home(self) -> None:
        """
        Moves cursor to position 0,0.
        (this _command takes a long time)
        """
        self._command(self.LCD_RETURNHOME)
        time.sleep(1)

    def no_display(self) -> None:
        """
        Turns the display off
        """
        self._show_control &= ~self.LCD_DISPLAYON
        self._command(self.LCD_DISPLAYCONTROL | self._show_control)

    def display(self) -> None:
        """
        Turns the display on
        """
        self._show_control |= self.LCD_DISPLAYON
        self._command(self.LCD_DISPLAYCONTROL | self._show_control)

    def stop_blink(self) -> None:
        """
        Stops the blinking cursor.
        """
        self._show_control &= ~self.LCD_BLINKON
        self._command(self.LCD_DISPLAYCONTROL | self._show_control)

    def blink(self) -> None:
        """
        Starts the blinking cursor.
        """
        self._show_control |= self.LCD_BLINKON
        self._command(self.LCD_DISPLAYCONTROL | self._show_control)

    def no_cursor(self) -> None:
        """
        Hides the cursor.
        """
        self._show_control &= ~self.LCD_CURSORON
        self._command(self.LCD_DISPLAYCONTROL | self._show_control)

    def cursor(self) -> None:
        """
        Shows the cursor.
        """
        self._show_control |= self.LCD_CURSORON
        self._command(self.LCD_DISPLAYCONTROL | self._show_control)

    def left_to_right(self) -> None:
        """
        Changes text flow to go from left to right
        """
        self._show_mode |= self.LCD_ENTRYLEFT
        self._command(self.LCD_ENTRYMODESET | self._show_mode)

    def right_to_left(self) -> None:
        """
        Changes text flow to go from right to left
        """
        self._show_mode &= ~self.LCD_ENTRYLEFT
        self._command(self.LCD_ENTRYMODESET | self._show_mode)

    def no_autoscroll(self) -> None:
        """
        Disables autoscroll mode
        """
        self._show_mode &= ~self.LCD_ENTRYSHIFTINCREMENT
        self._command(self.LCD_ENTRYMODESET | self._show_mode)

    def autoscroll(self) -> None:
        """
        Enable autoscroll mode, right justify will be enforced
        """
        self._show_mode |= self.LCD_ENTRYSHIFTINCREMENT
        self._command(self.LCD_ENTRYMODESET | self._show_mode)

    def custom_symbol(self, location: int, charmap: list[int]) -> None:
        """
        Loads custom symbols, see example/symbol.py

        :param location: bank 0-7
        :param charmap: bitmaps for char
        """
        location &= 0x7
        self._command(self.LCD_SETCGRAMADDR | (location << 3))
        for i in range(0, 8):
            self._write_block(self.lcd_addr, 0x40, [charmap[i]])

    def printstr(self, text: str) -> None:
        """
        Prints string

        :param text: text to print
        """
        self.print_out(text)

    def set_pwm(self, color: int, pwm: int) -> None:
        """
        Sets backlight colour using direct addresses.

        :param color: address of colour
        :param pwm: value of the colour
        """
        self._set_reg(color, pwm)
        if self.rgb_addr == 0x6B:
            self._set_reg(0x07, 0xFF)

    def set_color_white(self) -> None:
        """
        Sets whith backlight colour
        """
        self.set_RGB(255, 255, 255)

    def close_backlight(self) -> None:
        """
        Turns off backlight / sets black backlight colour
        """
        self.set_RGB(0, 0, 0)

    def _init_device(self) -> None:
        if self.rgb_addr == 0x60:
            self._set_reg(self.REG_MODE1, 1)

        time.sleep(0.05)
        for _ in range(1, 3):
            time.sleep(0.005)
            self._command(self.LCD_FUNCTIONSET | self._show_function)

        self._show_control = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF
        self.display()
        self.clear()

        self._command(self.LCD_ENTRYMODESET | self._show_mode)
        if self.rgb_addr == 0x60:
            self._set_reg(self.REG_MODE1, 0)
            self._set_reg(self.REG_OUTPUT, 0xFF)
            self._set_reg(self.REG_MODE2, 0x20)
        elif self.rgb_addr == 0x30:
            self._set_reg(0x04, 0x15)
        elif self.rgb_addr == 0x6B:
            self._set_reg(0x2F, 0x00)
            self._set_reg(0x00, 0x20)
            self._set_reg(0x01, 0x00)
            self._set_reg(0x02, 0x01)
            self._set_reg(0x03, 0x04)
        self.set_color_white()

    def _write_block(self, addr: int, reg: int, block: Any) -> None:
        while 1:
            try:
                self.bus.write_i2c_block_data(addr, reg, block)
                return
            except OSError as ex:
                print("I2C / error write block, retry in 1 sec...", ex)
                time.sleep(1)

    def _command(self, cmd: int) -> None:
        self._write_block(self.lcd_addr, 0x80, [cmd])

    def _set_reg(self, reg: int, data: int) -> None:
        self._write_block(self.rgb_addr, reg, [data])
