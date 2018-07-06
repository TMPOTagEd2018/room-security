from rx import Observable, Observer
from rx.core import ObservableBase
from rx.subjects import Subject
from rx.linq.observable import window

import numpy as np

from . import Monitor

class GyroMonitor(Monitor):
    def __init__(self, sensitivity = 1):
        super().__init__()

        self.sensitivity = sensitivity

        self.query = self.data \
            .map(int) \
            .buffer_with_count(10, 5) \
            .subscribe(self.handler)

    def input(self, value):
        self.data.on_next(value)

    def handler(self, buffer: [int]):
        # the sensor reports degrees/s

        # observe the last 10 values and check if the box is rotating quickly

        m = np.max(buffer)

        # the box should be stationary and the gyro shouldn't be jittering more
        # than ±2 degrees

        if m > 20:
            self.threats.on_next(3 * self.sensitivity)
        elif m > 10:
            self.threats.on_next(2 * self.sensitivity)
        elif m > 1:
            self.threats.on_next(1 * self.sensitivity)
        else:
            self.threats.on_next(0)

            
