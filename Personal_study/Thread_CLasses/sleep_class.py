import threading
import time

class Sleepy_Timey(threading.Thread):
    
    def __init__(self, seconds):
        super(Sleepy_Timey, self).__init__()
        self._seconds = seconds
        self.start()
        
    def _time_sleep(self):
        time.sleep(self._seconds)
        
    def run(self):
        self._time_sleep()