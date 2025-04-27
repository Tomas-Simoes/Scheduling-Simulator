import json

from config.types.process_generation import ProcessGenerationConfig
from config.types.clock import ClockConfig
from config.types.scheduling import SchedulingConfig

class Config:
    def __init__(self, config):
        self.config = config

        self.processGenerationConfig = ProcessGenerationConfig(self.config["processGeneration"])
        self.clockConfig = ClockConfig(self.config["clock"])
        self.schedulingConfig = SchedulingConfig(self.config["scheduling"])

