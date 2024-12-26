import datetime
import time

class ZTimer:

    @classmethod
    def str2msecond(cls):
        """年_月_日_时_分_秒_毫秒"""
        return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')

    @classmethod
    def str2second(cls):
        """年_月_日_时_分_秒"""
        return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    @classmethod
    def str2day(cls):
        """年_月_日"""
        return datetime.datetime.now().strftime('%Y_%m_%d')
    
    @classmethod
    def str_hms(cls):
        """时_分_秒"""
        return datetime.datetime.now().strftime('%H_%M_%S')

    @classmethod
    def str_hmsms(cls):
        """时_分_秒_毫秒"""
        return datetime.datetime.now().strftime('%H_%M_%S_%f')
    
    @classmethod
    def stamp(cls):
        return datetime.datetime.now().timestamp()

    @classmethod
    def timing(self, f, n=1):
        t0 = time.time()
        for i in range(n):
            f()
        return time.time() - t0


    