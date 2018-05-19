import time

class Stopper:
    def __init__(self):
        self.timeSpent = 0
        self.__lastRun = time.time()
    
    def reset(self):
        self.timeSpent = 0
        self.__lastRun = time.time()
    
    def progress(self):
        self.timeSpent += time.time() - self.__lastRun
        self.__lastRun = time.time()


