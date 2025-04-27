from PyQt6.QtWidgets import QGroupBox, QFormLayout, QCheckBox, QSpinBox, QDoubleSpinBox

"""
    Initializes the Process Generation configuration panel:
    - adds all necessary configs
    - set constraints for configs 
    - set default values if no configuration is set (if user didn't load config file)

    Also has a method to extract current configurations from the panel
"""
class PGConfigPanel(QGroupBox):
    def __init__(self, pgConfigurations):
        super().__init__("Process Generation Config")
        formLayout = QFormLayout()
        self.setLayout(formLayout)
        
        useRandomGen = QCheckBox("Use Random Generation")
        useRandomGen.setToolTip("Enable to generate processes with random attributes.")
        useRandomGen.setObjectName("useRandomGen")
        
        maxTime = QSpinBox()
        maxTime.setToolTip("Set the maximum duration for the simulation.")
        maxTime.setRange(1, 9999)  
        maxTime.setObjectName("maxTime")
        
        arrivalLambda = QDoubleSpinBox()
        arrivalLambda.setToolTip("Lambda (λ) parameter for the arrival time distribution.")
        arrivalLambda.setRange(0.1, 1000.0) 
        arrivalLambda.setSingleStep(0.1)
        arrivalLambda.setObjectName("arrivalLambda")
        
        burstLambda = QDoubleSpinBox()
        burstLambda.setToolTip("Lambda (λ) parameter for the burst time distribution.")
        burstLambda.setRange(0.1, 1000.0)  
        burstLambda.setSingleStep(0.1)
        burstLambda.setObjectName("burstLambda")
        
        seed = QSpinBox()
        seed.setToolTip("Seed value for random number generation to ensure reproducibility.")
        seed.setRange(1, 9999)  
        seed.setObjectName("seed")
        
        useRandomGen.setChecked(True)
        maxTime.setValue(30)
        arrivalLambda.setValue(4.0)
        burstLambda.setValue(0.5)
        seed.setValue(57)
        
        if pgConfigurations:
            useRandomGen.setChecked(pgConfigurations.get("useProcessGeneration", True))
            maxTime.setValue(pgConfigurations.get("maxTime", 5))
            arrivalLambda.setValue(pgConfigurations.get("arrival", {}).get("lambda", 4.0))
            burstLambda.setValue(pgConfigurations.get("burst", {}).get("lambda", 0.5))
            seed.setValue(pgConfigurations.get("seed", 57))
        
        self.layout().addRow(useRandomGen)
        self.layout().addRow("Max Time:", maxTime)
        self.layout().addRow("Arrival λ:", arrivalLambda)
        self.layout().addRow("Burst λ:", burstLambda)
        self.layout().addRow("Seed:", seed)
        
        self.useRandomGen = useRandomGen
        self.maxTime = maxTime
        self.arrivalLambda = arrivalLambda
        self.burstLambda = burstLambda
        self.seed = seed
    
    def getProcessGenerationConfig(self):
        useRandomGen = self.useRandomGen.isChecked()
        maxTime = self.maxTime.value()
        arrivalLambda = self.arrivalLambda.value()
        burstLambda = self.burstLambda.value()
        seed = self.seed.value()
        
        if maxTime <= 0:
            raise ValueError("Max Time must be greater than zero.")
        if arrivalLambda <= 0:
            raise ValueError("Arrival λ must be greater than zero.")
        if burstLambda <= 0:
            raise ValueError("Burst λ must be greater than zero.")
        if seed <= 0:
            raise ValueError("Seed must be greater than zero.")
            
        return {
            "useProcessGeneration": useRandomGen,
            "maxTime": maxTime,
            "arrival": {"lambda": arrivalLambda},
            "burst": {"lambda": burstLambda},
            "priorities": {
                "values": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weights": [0.25, 0.20, 0.15, 0.10, 0.08, 0.07, 0.05, 0.04, 0.02, 0.01]
            },
            "periods": {
                "values": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weights": [0.25, 0.20, 0.15, 0.10, 0.08, 0.07, 0.05, 0.04, 0.02, 0.01]
            },
            "seed": seed
        }