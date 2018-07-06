from rx.core import Disposable
from rx.subjects import Subject

class Monitor:
    query: Disposable
    data: Subject = Subject()
    threats: Subject = Subject()