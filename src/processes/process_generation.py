# process_generator.py
import numpy as np
import random
import json 

from .process import Process
from config.types.process_generation import ProcessGenerationConfig

class ProcessGenerator:
    def __init__(self, config: ProcessGenerationConfig):
        self.config = config
        self.last_PID = 0
    
    def generate_random_processes(self):
        processList = []

        arrivalTimes = self.generate_arrivalTimes(self.config.arrival.lam, self.config.maxTime)
        numProcesses = len(arrivalTimes) - 1

        burstTimes = self.generate_burstTimes(self.config.burst.lam, numProcesses)
        priorityList = self.generate_priorities(self.config.priorities.values, self.config.priorities.weights, numProcesses)
        periodList = self.generate_periods(self.config.periods.values, self.config.periods.weights, numProcesses)
        deadlineList = self.generate_deadline(self.config.deadline.values, self.config.deadline.weights, numProcesses)


        for i in range(numProcesses):
            process = Process(self.generate_pid(), arrivalTimes[i], burstTimes[i], priorityList[i], periodList[i], deadlineList[i])
            processList.append(process)
        
        return processList

    def get_static_processes(self):
        JSONProcesses = []

        with open("./staticProcesses.json", 'r') as file:
            JSONProcesses = json.load(file)

        processList = []

        for jsonProcess in JSONProcesses:
            process = Process(jsonProcess["pid"], jsonProcess["arrivalTime"], jsonProcess["burstTime"], jsonProcess["priority"])
            processList.append(process)

        return processList


    """
        Simulates arrival times over a time frame (0 to maxTime).

        The time between two consecutive arrivals (inter-arrival time) is an exponencial distribution 
        with parameter lambda (lam).

        The arrival time of a process is the lastArrivalTime + inter-arrival time
    """    
    def generate_arrivalTimes(self, lam, maxTime):
        t_max = maxTime 
        scale = 1 / lam 
        rng = np.random.default_rng(seed=self.config.seed)
        
        arrivalTimes = []
        lastArrival = 0

        while lastArrival < t_max:
            dt = rng.exponential(scale=scale)
            lastArrival += dt 
            arrivalTimes.append(lastArrival)

        return arrivalTimes
    
    """
        Generates burst times for "numProcesses" processes
        
        Burst times follow an exponencial distribution where most processes having 
        short burst and some with longer bursts
    """    
    def generate_burstTimes(self, lam, numProcesses):
        scale = 1 / lam
        rng = np.random.default_rng(seed=self.config.seed)
        burstTimes = rng.exponential(scale=scale, size=numProcesses)

        return burstTimes  
    
    """
        Generates a weighted random sampling for priorities where 

        priorites: a list of possible priorities e.g [0,1,2,3,4,5]
        weight: corresponding weights for the priorieties e.g [0.4, 0.3, 0.15, 0.1, 0.04, 0.01]

        that way, lower priorities are more likely
    """
    def generate_priorities(self, priorities, weights, numProcesses):
        return random.choices(priorities, weights=weights, k=numProcesses)
    
    def generate_periods(self, periods, weights, numProcesses):
        return random.choices(periods, weights=weights, k=numProcesses)
    
    def generate_deadline(self, deadlines, weights, numProcesses):
        return random.choices(deadlines, weights=weights, k=numProcesses)

    """
        Generates an PID (Process ID) from the previous ID
    """
    def generate_pid(self):
        self.last_PID += 1
        return self.last_PID