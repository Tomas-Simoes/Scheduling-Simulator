from PyQt6.QtWidgets import QPlainTextEdit, QVBoxLayout, QSizePolicy, QGroupBox
import json, copy

class ConfigPanel(QGroupBox):
    def __init__(self, config, parent=None):
        super().__init__("Configuration Panel",parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        cloned_config = copy.deepcopy(config)
        del cloned_config["processGeneration"]["priorities"]

        formatted_json = json.dumps(cloned_config, indent=2)

        text_box = QPlainTextEdit()
        text_box.setReadOnly(True)
        text_box.setPlainText(formatted_json)
        text_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout.addWidget(text_box)
