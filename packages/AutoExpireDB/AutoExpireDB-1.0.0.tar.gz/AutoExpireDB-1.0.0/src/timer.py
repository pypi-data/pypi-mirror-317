from threading import Timer as ThreadTimer

class Timer:
    def __init__(self, minutes, function, args=None):
        self.minutes = minutes
        self.function = function
        self.args = args if args else []

    def start(self):
        t = ThreadTimer(self.minutes * 60, self.function, self.args)
        t.start()
