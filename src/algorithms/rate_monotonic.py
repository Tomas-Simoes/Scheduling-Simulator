from .algorithm import Algorithm
from processes.process import Process
from typing import List, Optional
from collections import deque

class RateMonotonic(Algorithm):
    def __init__(self):
        super().__init__()
        self.ready_queue = []
    
    def schedule(self) -> Optional[Process]:
        if not self.ready_queue:
            return None
        # verificar a priopriodade por periodo
        
        highest_priority = min(self.ready_queue, key=lambda process: process.period)
        return highest_priority
    
    def process_arrival(self, process: Process) -> None:
        self.ready_queue.append(process)
    
    def process_completion(self, process: Process) -> int:
        if (process.executionsNumber > process.period):
            self.deadline_miss(process)
            return -1
        elif (process.executionsNumber < process.period):
            process.executionsNumber += 1
            return 0
        else:
            if process in self.ready_queue:
                self.ready_queue.remove(process)
            return 1
        
    def deadline_miss(self, process: Process) -> None:
        if process in self.ready_queue:
                self.ready_queue.remove(process)
            
            