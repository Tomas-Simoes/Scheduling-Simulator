class ArrivalConfig:
    def __init__(self, config_dict):
        self.lam = config_dict["lambda"]  

class BurstConfig:
    def __init__(self, config_dict):
        self.lam = config_dict["lambda"]

class PrioritiesConfig:
    def __init__(self, config_dict):
        self.values = config_dict["values"]
        self.weights = config_dict["weights"]
        
class PeriodsConfig:
    def __init__(self, config_dict):
        self.values = config_dict["values"]
        self.weights = config_dict["weights"]

class ProcessGenerationConfig:
    def __init__(self, config_dict):
        self.useProcessGeneration = config_dict["useProcessGeneration"]
        self.seed = config_dict["seed"]
        self.maxTime = config_dict["maxTime"]
        self.arrival = ArrivalConfig(config_dict["arrival"])
        self.burst = BurstConfig(config_dict["burst"])
        self.priorities = PrioritiesConfig(config_dict["priorities"])
        self.periods = PeriodsConfig(config_dict["periods"])
        self.deadline = self.periods