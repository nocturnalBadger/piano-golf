import ctypes

MOUSEEVENTF_MOVE = 0x0001 # mouse move 
MOUSEEVENTF_LEFTDOWN = 0x0002 # left button down 
MOUSEEVENTF_LEFTUP = 0x0004 # left button up 
MOUSEEVENTF_RIGHTDOWN = 0x0008 # right button down 
MOUSEEVENTF_RIGHTUP = 0x0010 # right button up 
MOUSEEVENTF_MIDDLEDOWN = 0x0020 # middle button down 
MOUSEEVENTF_MIDDLEUP = 0x0040 # middle button up 
MOUSEEVENTF_WHEEL = 0x0800 # wheel button rolled 
MOUSEEVENTF_ABSOLUTE = 0x8000 # absolute move 

class WindowsMouse:

    def __init__(self):
        pass

    def move_x(self, distance):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, ctypes.c_long(distance), 0, 0, 0)

    def move_y(self, distance):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, 0, ctypes.c_long(distance), 0, 0)

    def click_down(self):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    def click_up(self):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def right_click_down(self):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)

    def right_click_up(self):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

mouse = WindowsMouse()
