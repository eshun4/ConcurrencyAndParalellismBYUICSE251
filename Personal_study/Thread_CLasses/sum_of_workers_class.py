import threading


class Sum_of_Squares(threading.Thread):
    def __init__(self, n):
        super(Sum_of_Squares, self).__init__()
        self._n = n
        self.start()
        
    def _sum_of_squares(self):
        number = 0
        for i in range(self._n):
            number += i**2
        print(number)
        return number 
    
    def run(self):
        self._sum_of_squares()