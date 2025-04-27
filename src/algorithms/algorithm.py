from abc import ABC, abstractmethod
from processes.process import Process
from typing import List, Optional

class Algorithm(ABC):
    def __init__(self):
        pass 
    
    # Selects the next process to be executed.
    # Returns None if there isn't any process to be executed
    @abstractmethod
    def schedule(self) -> Optional[Process]:
        pass
    
    # Called when a new process arrives
    @abstractmethod
    def process_arrival(self, process: Process) -> None:
        pass
    
    # Called when a process finished his execution
    @abstractmethod
    def process_completion(self, process: Process) -> None:
        pass