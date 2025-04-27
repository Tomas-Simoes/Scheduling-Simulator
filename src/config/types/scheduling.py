class SchedulingConfig:
    def __init__(self, config_dict):
        self.scheduleAlgorithm = config_dict["schedulingAlgorithm"]
        self.timeQuantum = config_dict["timeQuantum"]