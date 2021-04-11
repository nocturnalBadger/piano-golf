import uinput

class LinuxMouse:
    def __init__(self):
        self.device = uinput.Device([uinput.REL_X, uinput.REL_Y, uinput.BTN_LEFT, uinput.BTN_RIGHT])

    def move_x(self, distance):
        self.device.emit(uinput.REL_X, distance)

    def move_y(self, distance):
        self.device.emit(uinput.REL_Y, distance)

    def click_down(self):
        self.device.emit(uinput.BTN_LEFT, 1)

    def click_up(self):
        self.device.emit(uinput.BTN_LEFT, 0)

mouse = LinuxMouse()
