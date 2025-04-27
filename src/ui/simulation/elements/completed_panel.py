from typing import Dict, List
from PyQt6.QtWidgets import (
    QWidget, QGroupBox, QLabel, QVBoxLayout, QHBoxLayout, 
    QSizePolicy, QScrollArea, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt, pyqtSlot
from ui.custom.process_block import ProcessBlock
from processes.process import Process

import math

class CompletedPanel(QGroupBox):
    completedProcessBlocks: Dict[int, ProcessBlock]
    prioritiesLabels: Dict[int, QLabel]
    statisticsLabels: List[QLabel]

    def __init__(self, config, parent=None):
        super().__init__("Complete Processes Panel", parent)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.config = config 
        self.readyProcessBlocks = {}
        self.prioritiesLabels = {}
        
        self.completedProcessSection()
        self.completedQueueSection()
        self.statisticsSection()
        self.mainLayout.addStretch(1)

    @pyqtSlot(object, int)
    def updateCompletedProcesses(self, processList: List[Process], processSwitchCount):
        newPIDs = {process.pid for process in processList}
        oldPIDs = set(self.readyProcessBlocks.keys())

        removedPIDs = oldPIDs - newPIDs

        for pid in removedPIDs:
            removedBlock = self.readyProcessBlocks.pop(pid)
            self.completedLayout.removeWidget(removedBlock)
            removedBlock.setParent(None)
            removedBlock.deleteLater()            

        for process in processList:
            pid = process.pid
            if pid not in self.readyProcessBlocks:
                newProcessBlock = ProcessBlock(process)
                newProcessBlock.clicked.connect(self.updateCompletedProcessInformation)

                self.readyProcessBlocks[pid] = newProcessBlock
                self.completedLayout.addWidget(newProcessBlock)

        #self.updatePrioritiesSection(processList)
        self.updateStatistics(processList, processSwitchCount)

    def updateStatistics(self, processList: List[Process], processSwitchCount):
        numProcesses = len(processList)
        
        if numProcesses == 0:
            return  
        
        self.statisticsLabels["totalProcessCompleted"].setText(f"Total processes completed: {numProcesses}")

        completionTimes = [process.completionTime for process in processList if process.completionTime is not None]
        if completionTimes:
            avgCompletionTime = sum(completionTimes) / len(completionTimes)
            self.statisticsLabels["averageCompletitionTime"].setText(f"Average Completion time: {avgCompletionTime:.2f} (min: {min(completionTimes):.2f}, max: {max(completionTimes):.2f})")

        # Calculate turnaround time statistics
        turnaroundTimes = [process.turnaroundTime for process in processList if process.turnaroundTime > 0]
        if turnaroundTimes:
            avgTurnaroundTime = sum(turnaroundTimes) / len(turnaroundTimes)
            self.statisticsLabels["averageTurnaroundTime"].setText(f"Average Turnaround time: {avgTurnaroundTime:.2f} (min: {min(turnaroundTimes):.2f}, max: {max(turnaroundTimes):.2f})")
        
            # Calculate turnaround variance
            turnaroundVariance = sum((t - avgTurnaroundTime) ** 2 for t in turnaroundTimes) / len(turnaroundTimes)
            self.statisticsLabels["turnaroundVariance"].setText(f"Turnaround variance: {turnaroundVariance:.2f}")

        # Calculate waiting time statistics
        waitingTimes = [process.waitingTime for process in processList if process.waitingTime >= 0]
        if waitingTimes:
            avgWaitingTime = sum(waitingTimes) / len(waitingTimes)
            self.statisticsLabels["averageWaitingTime"].setText(f"Average Waiting time: {avgWaitingTime:.2f} (min: {min(waitingTimes):.2f}, max: {max(waitingTimes):.2f})")

        # Process Switch Count
        self.statisticsLabels["processSwitchCount"].setText(f"Process switch count: {processSwitchCount}")

    def updateCompletedProcessInformation(self, process):
        if not process:
            for key in self.processInformationLabels:
                self.processInformationLabels[key].setText(f"{key.replace('_', ' ').capitalize()}: N/A")
            return

        # Prepare the formatted values with fallback to "N/A"
        pid = str(process.pid)
        arrival = f"{process.arrivalTime:.2f}" if process.arrivalTime is not None else "N/A"
        burst = f"{process.burstTime:.2f}" if process.burstTime is not None else "N/A"
        priority = str(process.priority) if process.priority is not None else "N/A"
        is_completed = "Yes" if process.is_completed else "No"
        remaining = f"{process.remaining_time:.2f}" if process.remaining_time is not None else "N/A"
        waiting = f"{process.waitingTime:.2f}" if process.waitingTime is not None else "N/A"
        turnaround = f"{process.turnaroundTime:.2f}" if process.turnaroundTime is not None else "N/A"
        start = f"{process.startTime:.2f}" if process.startTime is not None else "N/A"
        status = str(getattr(process, "status", "N/A"))

        # Set the texts
        self.processInformationLabels["pid"].setText(f"PID: {pid}")
        self.processInformationLabels["arrivalTime"].setText(f"Arrival Time: {arrival}")
        self.processInformationLabels["burstTime"].setText(f"Burst Time: {burst}")
        self.processInformationLabels["priority"].setText(f"Priority: {priority}")
        self.processInformationLabels["isCompleted"].setText(f"Is Completed: {is_completed}")
        self.processInformationLabels["remainingTime"].setText(f"Remaining Time: {remaining}")
        self.processInformationLabels["waitingTime"].setText(f"Waiting time: {waiting}")
        self.processInformationLabels["turnaroundTime"].setText(f"Turnaround time: {turnaround}")
        self.processInformationLabels["startTime"].setText(f"Start time: {start}")
        self.processInformationLabels["status"].setText(f"Status: {status}")


    # Creates a section that let's you see a completed process information
    def completedProcessSection(self):
        containerGroup = QGroupBox("Process Information (press one in Ready Queue)")
        containerGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        # Horizontal layout to hold both sections
        containerLayout = QHBoxLayout()
        containerLayout.setSpacing(20)

        informationGroup = QGroupBox("Information")
        informationGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        informationLayout = QGridLayout()
        informationLayout.setVerticalSpacing(2)
        informationLayout.setHorizontalSpacing(20)

        self.processInformationLabels = {
            "pid": QLabel("PID: No"),
            "arrivalTime": QLabel("Arrival Time: 0"),
            "burstTime": QLabel("Burst Time: 0   (min: 0, max: 0)"),
            "priority": QLabel("Priority: 0"),
            "isCompleted": QLabel("Is Completed: No"),
            "remainingTime": QLabel("Remaining Time: 0"),
            "waitingTime": QLabel("Waiting time: 0"),
            "turnaroundTime": QLabel("Turnaround time: 0"),
            "startTime": QLabel("Start time: 0"),
            "status": QLabel("Status: 0"),
        }

        # Add to grid layout in two columns
        for i, label in enumerate(self.processInformationLabels.values()):
            row = i // 2
            col = i % 2
            informationLayout.addWidget(label, row, col)

        informationGroup.setLayout(informationLayout)

        containerLayout.addWidget(informationGroup)
        containerGroup.setLayout(containerLayout)
        
        self.mainLayout.addWidget(containerGroup)
    
    # Creates completed queue section, which contains a list of completed ProcessBlocks
    def completedQueueSection(self):
        completedQueueGroup = QGroupBox("Completed Process Queue")
        completedQueueGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scrollWidget = QWidget()
        completedLayout = QHBoxLayout(scrollWidget)
        completedLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        completedLayout.setContentsMargins(0, 0, 0, 0)
        completedLayout.setSpacing(10)  
        
        scrollArea.setWidget(scrollWidget)
        
        completedQueueLayout = QVBoxLayout()
        completedQueueLayout.addWidget(scrollArea)
        completedQueueGroup.setLayout(completedQueueLayout)
        completedQueueGroup.setMaximumHeight(150)
        completedQueueLayout.setContentsMargins(0, 0, 0, 0)
        completedQueueLayout.setSpacing(0)

        self.mainLayout.addWidget(completedQueueGroup)

        self.completedLayout = completedLayout
        self.completedQueueGroup = completedQueueGroup
    
    def statisticsSection(self):
        # Statistics section
        statisticsGroup = QGroupBox("Statistics")
        statisticsGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        statisticsLayout = QVBoxLayout()
        statisticsLayout.setSpacing(2)

        self.statisticsLabels = {
            "totalProcessCompleted": QLabel("Total processes completed: 0"),
            "averageCompletitionTime": QLabel("Average Completition time: 0   (min: 0, max: 0)"),
            "averageTurnaroundTime": QLabel("Average Turnaround time: 0   (min: 0, max: 0)"),
            "averageWaitingTime": QLabel("Average Turnaround time: 0   (min: 0, max: 0)"),
            "turnaroundVariance": QLabel("Turnaround variance: 0"),
            "processSwitchCount": QLabel("Process switch count: 0")
        }
        
        for label in self.statisticsLabels.values():
            statisticsLayout.addWidget(label)
        
        statisticsGroup.setLayout(statisticsLayout)
        self.mainLayout.addWidget(statisticsGroup)
    
 
