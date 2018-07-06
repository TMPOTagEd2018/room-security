from rx.core import Disposable
from rx.subjects import Subject

class Monitor:
    query: Disposable
    data: Subject = Subject()
    threats: Subject = Subject()

    
    def dispose(self):
        if self.query is not None:
            self.query.dispose()