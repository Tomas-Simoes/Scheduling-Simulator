from algorithms.fcfs import FCFS
from algorithms.shortest_job import ShortestJob
from algorithms.priority import PriorityNonPreemptive, PriorityPreemptive
from algorithms.round_robin import RoundRobin
from algorithms.rate_monotonic import RateMonotonic
from algorithms.earliest_deadline import EarliestDeadline

from config.types.scheduling import SchedulingConfig

def create_algorithm(config: SchedulingConfig):
    algorithmName = config.scheduleAlgorithm.upper()
    
    match algorithmName:
        case "FIRST-COME, FIRST-SERVED":
            return FCFS()
        case "SHORTEST JOB FIRST":
            return ShortestJob()
        case "PRIORITY SCHEDULING (NON-PREEMPTIVE)":
            return PriorityNonPreemptive()
        case "PRIORITY SCHEDULING (PREEMPTIVE)":
            return PriorityPreemptive()
        case "ROUND ROBIN":
            if config and config.timeQuantum:
                return RoundRobin(time_quantum=config.timeQuantum)
            else:
                raise ValueError("Time quantum must be specified for Round Robin scheduling")
        case "RATE MONOTONIC":
            return RateMonotonic()
        case "EARLIEST DEADLINE FIRST":
            return EarliestDeadline()
        case _:
            raise ValueError(f"Unknown scheduling algorithm: {algorithmName}")