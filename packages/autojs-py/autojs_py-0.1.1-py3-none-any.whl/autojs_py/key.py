class Keys:

    def __init__(self, driver):
        self.driver = driver
    def keycode(self, code):
        self.driver.keyevent(code)
    def home(self):
        pass
    def back(self):
        pass
    def power(self):
        pass
    def volume_up(self):
        pass
    def volume_down(self):
        pass
    def menu(self):
        pass
    