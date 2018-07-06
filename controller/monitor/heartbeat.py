from rx import Observable, Observer
from rx.core import ObservableBase
from rx.subjects import Subject
from rx.linq.observable import window

from datetime import datetime
from threading import Timer

import numpy as np

from . import Monitor

class HeartbeatMonitor(Monitor):
    timer1: Timer
    timer2: Timer
    timer3: Timer

    def __init__(self):
        super().__init__()
        timer1 = None
        timer2 = None
        timer3 = None

    def input(self, value):
        self.threats.on_next(0)

        timer1.cancel()
        timer2.cancel()
        timer3.cancel()

        timer1 = Timer(3, lambda _: self.threats.on_next(1))
        timer2 = Timer(7, lambda _: self.threats.on_next(2))
        timer3 = Timer(10, lambda _: self.threats.on_next(3))

            

            
