from PyQt6.QtWidgets import (
    QWidget, QGroupBox, QLabel, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QScrollArea, QGridLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSlot

from ui.custom.process_block import ProcessBlock
from ui.graphs.completedOverTimeGraph import CompletionOverTimeGraph
from ui.graphs.waitingOverTimeGraph import WaitingOverTimeGraph

from global_clock import GlobalClock
class ClockPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Time Panel", parent)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)  
        self.main_layout.setSpacing(10)  # Adjust the spacing as needed
        self.setLayout(self.main_layout)
        
        clock_widget = QWidget()
        clock_layout = QHBoxLayout()  
        clock_layout.setSpacing(2)
        clock_layout.setContentsMargins(0, 0, 0, 0)
        clock_widget.setLayout(clock_layout)
        
        hours = QLabel("00")
        minutes = QLabel("00")
        seconds = QLabel("00")
        milliseconds = QLabel("000")
        separatorH = QLabel(":")
        separatorM = QLabel(":")
        
        hours.setFont(QFont("Courier", 40, QFont.Weight.Bold))
        minutes.setFont(QFont("Courier", 40, QFont.Weight.Bold))
        seconds.setFont(QFont("Courier", 40, QFont.Weight.Bold))
        milliseconds.setFont(QFont("Courier", 20, QFont.Weight.Normal))
        separatorH.setFont(QFont("Courier", 40, QFont.Weight.Bold)) 
        separatorM.setFont(QFont("Courier", 40, QFont.Weight.Bold)) 
        
        for label in [minutes, seconds, milliseconds, separatorH, separatorM]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        milliseconds.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
        
        clock_layout.addWidget(hours)
        clock_layout.addWidget(separatorH)
        clock_layout.addWidget(minutes)
        clock_layout.addWidget(separatorM)
        clock_layout.addWidget(seconds)
        clock_layout.addWidget(milliseconds)

        # Create a horizontal layout to hold the two graphs side by side
        graph_layout = QHBoxLayout()

        # Initialize the graphs
        self.completionOverTimeGraph = CompletionOverTimeGraph()
        self.waitingOverTimeGraph = WaitingOverTimeGraph()

        # Add the graphs to the horizontal layout
        graph_layout.addWidget(self.completionOverTimeGraph)
        graph_layout.addWidget(self.waitingOverTimeGraph)

        # Add the clock widget and the graph layout to the main layout
        self.main_layout.addWidget(clock_widget, 0, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.main_layout.addLayout(graph_layout)  # Use addLayout to add the horizontal graph layout

        self.main_layout.addStretch(1)  # Add stretch at the bottom to fill space

        self.hours = hours 
        self.minutes = minutes 
        self.seconds = seconds 
        self.milliseconds = milliseconds
    
    def updateClockDisplay(self):
        total_ms = GlobalClock.getTime()
        
        h = total_ms // (1000 * 60 * 60)
        m = (total_ms // (1000 * 60)) % 60
        s = (total_ms // 1000) % 60
        ms = total_ms % 1000

        self.hours.setText(f"{h:02d}")
        self.minutes.setText(f"{m:02d}")
        self.seconds.setText(f"{s:02d}")
        self.milliseconds.setText(f"{ms:03d}")

    def updateCompletionOverTimeGraph(self, completionCount):
        self.completionOverTimeGraph.addNewPoint(GlobalClock.getTime(), completionCount)

