import random
class Process:
    def __init__(self, pid, arrivalTime, burstTime, priority, period, deadline):
        self.pid = pid
        self.arrivalTime = arrivalTime
        self.firstScheduling = None
        self.burstTime = burstTime
        self.priority = priority
        self.period = period
        randomDeadline = random.randint(25, 175)
        self.deadline = arrivalTime + randomDeadline
        self.remaining_time = burstTime
        self.time_in_current_quantum = 0
        self.waitingTime = 0
        self.turnaroundTime = 0
        self.startTime = None
        self.completionTime = 0
        self.executionsNumber = 0
        self.status = "READY"
        
    def execute(self, time_quantum):
        self.status = "RUNNING"
        time_used = min(time_quantum, self.remaining_time)
        self.remaining_time -= time_used
        
        if self.remaining_time <= 0:
            self.status = "COMPLETED"
            
        return time_used
    
    def is_completed(self):
        return self.remaining_time <= 0
        
    def __str__(self):
        return f"Process {self.pid}: start={self.arrivalTime}, burst={self.burstTime}, priority={self.priority}, period={self.period}, completionTime={self.completionTime}, waitingTime={self.waitingTime}, deadline={self.deadline}"
    