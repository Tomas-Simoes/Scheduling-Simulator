from algorithms.algorithm import Algorithm
from processes.process import Process
from typing import List, Optional

class ShortestJob(Algorithm):
    def __init__(self):
        super().__init__()
        self.ready_queue = []
    
    def schedule(self) -> Optional[Process]:
        if not self.ready_queue:
            return None
        # Get the shortestJob from the queue
        shortestJob = min(self.ready_queue, key=lambda process: process.burstTime)
        return shortestJob
    
    def process_arrival(self, process: Process) -> None:
        self.ready_queue.append(process)
    
    def process_completion(self, process: Process) -> int:
        if process in self.ready_queue:
            self.ready_queue.remove(process)
        return 1