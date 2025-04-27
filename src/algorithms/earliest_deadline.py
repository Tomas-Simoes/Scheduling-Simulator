from .algorithm import Algorithm
from processes.process import Process
from typing import List, Optional

class EarliestDeadline(Algorithm):
    def __init__(self):
        super().__init__()
        self.ready_queue = []
    
    def schedule(self) -> Optional[Process]:
        if not self.ready_queue:
            return None
        
        earliest_deadline_process = min(self.ready_queue, key=lambda process: process.deadline)
        return earliest_deadline_process  
      
    def process_arrival(self, process: Process) -> None:
        # When a process arrives, calculate its absolute deadline
        self.ready_queue.append(process)
    
    def process_completion(self, process: Process) -> int:
        if process.completionTime > process.deadline:
            self.deadline_miss(process)
            return -1
        else:
            self.ready_queue.remove(process)

            return 1
    
    
    def deadline_miss(self, process: Process) -> None:
        self.ready_queue.remove(process)