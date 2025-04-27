from PyQt6.QtWidgets import QGroupBox, QFormLayout, QCheckBox, QDoubleSpinBox

"""
    Initializes the Clock configuration panel:
    - adds all necessary configs
    - set constraints for configs 
    - set default values if no configuration is set (if user didn't load config file)

    Also has a method to extract current configurations from the panel
"""
class ClockConfigPanel(QGroupBox):
    def __init__(self, clockConfig):
        super().__init__("Clock Config")
        
        formLayout = QFormLayout()
        self.setLayout(formLayout)

        tickDuration = QDoubleSpinBox()
        tickDuration.setToolTip("Duration of each simulation tick or time unit.")
        tickDuration.setRange(0.001, 10.0)  
        tickDuration.setSingleStep(0.1)
        tickDuration.setDecimals(3)
        tickDuration.setObjectName("tickDuration")
        
        tickDuration.setValue(1)

        if clockConfig:
            tickDuration.setValue(clockConfig.get("tick", 0.1))

        self.layout().addRow("Tick:", tickDuration)

        self.tickDuration = tickDuration

    def getClockConfig(self):
        tickDuration = self.tickDuration.value()
        
        if tickDuration <= 0:
            raise ValueError("Tick duration must be greater than zero.")
        
        return {
            "tick": tickDuration
        }