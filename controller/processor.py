from rx import Observable
from rx.core import Disposable

import numpy as np
from datetime import datetime as dt

import colorama as cr
cr.init(autoreset=True)

class ThreatProcessor:
    prev_score: float = 0

    def __init__(self, threats, sensitivity):
        self.threats = threats
        self.sensitivity = sensitivity
        self.query = self.threats.buffer_with_count(sensitivity, sensitivity - 1)
        self.subscription = self.query.subscribe(self.on_threat)

    def on_threat(self, buffer: [int]):
        if -1 in buffer:
            prev_score = 0
            buffer = [0]
            print(f"[{dt.now()}] Threat level has been reset.")

        threat_score = (np.sum(buffer) + np.max(buffer)) / (np.std(buffer) + 1) / self.sensitivity * 2

        if threat_score > 3:
            print(cr.Fore.RED + cr.Style.BRIGHT + f"[{dt.now()}] Threat level 3: critical activity detected.")
        elif threat_score > 2:
            print(cr.Fore.YELLOW + cr.Style.BRIGHT + f"[{dt.now()}] Threat level 2: suspicious activity detected.")
        elif threat_score > 1:
            print(cr.Fore.YELLOW + f"[{dt.now()}] Threat level 1: potential activity detected.")

        if self.prev_score > threat_score and threat_score <= 1:
            print(f"[{dt.now()}] Threat level 0: returned to normal.")

        self.prev_score = threat_score