from config.config import Config

from clock import ClockWorker
from scheduler import SchedulerWorker
from processes.process_generation import ProcessGenerator

class Simulation:
    def __init__(self, config):
        # Initializes our simulation configuration
        config = Config(config)
        processGenConfig = config.processGenerationConfig
        clockConfig = config.clockConfig
        schedulingConfig = config.schedulingConfig

        # Responsible for generate processes using probabilistics distributions
        processGenerator = ProcessGenerator(processGenConfig)

        processList = (processGenerator.generate_random_processes()
                       if processGenConfig.useProcessGeneration
                       else processGenerator.get_static_processes())

        # Responsible to decide which process to execute
        self.schedulerWorker = SchedulerWorker(schedulingConfig, clockConfig)

        # Responsible for feading the Scheduler with a process when it arrives
        self.clockWorker = ClockWorker(clockConfig, self.schedulerWorker, processList)