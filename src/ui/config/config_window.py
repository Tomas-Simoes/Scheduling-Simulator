from PyQt6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel,
    QFileDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt  

from ui.config.elements.pg_panel import PGConfigPanel
from ui.config.elements.clock_panel import ClockConfigPanel
from ui.config.elements.scheduling_panel import SchedulingConfigPanel

from ui.simulation.simulation_window import SimulationWindow

import json

class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scheduling Simulation")
        self.resize(400, 600)
        
        self.buildConfigurationMenu()

    """
        Builds the configuration menu in the following format:

        - Process Generation Configs
        - Clock Configs
        - Scheduling Configs
        - Load Config from file button
        - Logo
        - Start Simulation Button
    """
    def buildConfigurationMenu(self, config=None):
        centralWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        # Configuration Panels
        self.pgPanel = PGConfigPanel(config["processGeneration"] if config else None)
        self.clockPanel = ClockConfigPanel(config["clock"] if config else None)
        self.schedulingPanel = SchedulingConfigPanel(config["scheduling"] if config else None)

        # Add Load Config File Button
        btnLoadConfig = QPushButton("Load config from file")
        btnLoadConfig.setToolTip("Click to load a config file.")
        btnLoadConfig.clicked.connect(self.loadConfigFile)  
        
        # Logo
        image = QLabel(self)
        image.setPixmap(QPixmap("./image.png"))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image.setScaledContents(True) 
        imageLayout = QHBoxLayout()
        imageLayout.setContentsMargins(20,20,20,20)
        imageLayout.addWidget(image)

        # Start Simulation Button
        btnStart = QPushButton("Start Simulation")
        btnStart.setToolTip("Click to start the simulation with the configured settings.")
        btnStart.clicked.connect(self.validateAndStartSimulation)

        # Add panels and button to the main layout
        self.mainLayout.addWidget(self.pgPanel)
        self.mainLayout.addWidget(self.clockPanel)
        self.mainLayout.addWidget(self.schedulingPanel)
        self.mainLayout.addWidget(btnLoadConfig)
        self.mainLayout.addLayout(imageLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(btnStart)

    """
     onPress start simulation button
     
     - builds our current config into a generalized object 
     - changes the current window to our SimulationWindow
    """
    def validateAndStartSimulation(self):
        config = self.buildAndValidateConfig()
        
        if config:
            self.simulationWindow = SimulationWindow(config)
            self.simulationWindow.show()
            self.close()
                
    # each GUI Configuration Panel has a method which extracts the current 
    # configuration and format's it into the correct format
    def buildAndValidateConfig(self):
        config = {
            "processGeneration": self.pgPanel.getProcessGenerationConfig(),
            "clock": self.clockPanel.getClockConfig(),
            "scheduling": self.schedulingPanel.getSchedulingConfig()
        }
        
        return config

    # onPress load config from file button
    # let's user select a configuration file and overwrites the current Configuration Panel 
    # with the config file 
    def loadConfigFile(self):
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        fileDialog.setNameFilter("JSON files (*.json)")
        
        if fileDialog.exec():
            filePaths = fileDialog.selectedFiles()
            if filePaths:
                filePath = filePaths[0]
                
                try:
                    with open(filePath, 'r') as f:
                        configData = json.load(f)
                    
                    self.clearCurrentLayout()
                    self.buildConfigurationMenu(configData)
                except Exception as e:
                    self.showError(f"Failed to load configuration file:\n{e}")

    # clears everything on Configuration Panel
    def clearCurrentLayout(self):
        if hasattr(self, 'mainLayout') and self.mainLayout:
            while self.mainLayout.count():
                item = self.mainLayout.takeAt(0)
                widget = item.widget()
                
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    del item