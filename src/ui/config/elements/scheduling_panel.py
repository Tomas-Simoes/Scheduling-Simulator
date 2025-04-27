from PyQt6.QtWidgets import QGroupBox, QFormLayout, QDoubleSpinBox, QComboBox

"""
    Initializes the Scheduling configuration panel:
    - adds all necessary configs
    - set constraints for configs 
    - set default values if no configuration is set (if user didn't load config file)

    Also has a method to extract current configurations from the panel
"""
class SchedulingConfigPanel(QGroupBox):
    def __init__(self, schedulingConfig):
        super().__init__("Scheduling Config")
        
        formLayout = QFormLayout()
        self.setLayout(formLayout)
        
        algorithmCombo = QComboBox()
        algorithmCombo.setObjectName("algorithmCombo")
        self.algorithms = [
            "First-Come, First-Served",
            "Shortest Job First",
            "Round Robin",
            "Priority Scheduling (Non-Preemptive)",
            "Priority Scheduling (Preemptive)",
            "Multilevel Queue Scheduling",
            "Earliest Deadline First",
            "Rate Monotonic",
            "Lottery Scheduling"
        ]
        algorithmCombo.addItems(self.algorithms)
        algorithmCombo.setToolTip("Select the scheduling algorithm for the simulation.")

        timeQuantum = QDoubleSpinBox()
        timeQuantum.setToolTip("Time quantum for algorithms like Round Robin.")
        timeQuantum.setRange(0.1, 100.0)  
        timeQuantum.setSingleStep(0.1)
        timeQuantum.setObjectName("timeQuantum")
        
        algorithmCombo.setCurrentText("First-Come, First-Served")
        timeQuantum.setValue(2.0)

        if schedulingConfig:
            algorithm = schedulingConfig.get("schedulingAlgorithm", "First-Come, First-Served")
            algorithmCombo.setCurrentText(algorithm)
            
            timeQuantum.setValue(schedulingConfig.get("timeQuantum", 2.0))

        self.layout().addRow("Algorithm:", algorithmCombo)
        self.layout().addRow("Time Quantum:", timeQuantum)

        self.algorithmCombo = algorithmCombo
        self.timeQuantum = timeQuantum

    def getSchedulingConfig(self):
        algorithm = self.algorithmCombo.currentText()
        timeQuantum = self.timeQuantum.value()
        
        if timeQuantum <= 0:
            raise ValueError("Time Quantum must be greater than zero.")
        
        return {
            "schedulingAlgorithm": algorithm,
            "timeQuantum": timeQuantum
        }
