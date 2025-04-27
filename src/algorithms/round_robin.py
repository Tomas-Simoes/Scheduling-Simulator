from algorithms.algorithm import Algorithm
from processes.process import Process
from typing import List, Optional
from collections import deque


class RoundRobin(Algorithm):
    def __init__(self, time_quantum: float):
        super().__init__()
        self.ready_queue = deque()
        self.time_quantum = time_quantum
    
    def schedule(self) -> Optional[Process]:
        if not self.ready_queue:
            return None
        
        current_process = self.ready_queue.popleft()
        return current_process
    
    def process_arrival(self, process: Process) -> None:
        self.ready_queue.append(process)
    
    def process_completion(self, process: Process) -> int:
        if process in self.ready_queue:
            self.ready_queue.remove(process)
        return 1
            