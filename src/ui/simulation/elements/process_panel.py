from typing import Dict, List
from PyQt6.QtWidgets import (
    QWidget, QGroupBox, QLabel, QVBoxLayout, QHBoxLayout, 
    QSizePolicy, QScrollArea, QGridLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSlot
from ui.custom.process_block import ProcessBlock
from processes.process import Process

import math

class ProcessesPanel(QGroupBox):
    readyProcessBlocks: Dict[int, ProcessBlock]
    prioritiesLabels: Dict[int, QLabel]
    statisticsLabels: List[QLabel]

    def __init__(self, config, parent=None):
        super().__init__("Processes Panel", parent)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.config = config 
        self.readyProcessBlocks = {}
        self.prioritiesLabels = {}
        
        self.runningProcessSection()
        self.readyQueueSection()
        self.processInformation()
        self.prioritiesAndStatisticsSection()

        self.mainLayout.addStretch(1)

    @pyqtSlot(object)
    def updateRunningProcess(self, process: Process):
        if self.runningProcessBlock:
            self.runningProcessLayout.removeWidget(self.runningProcessBlock)
            self.runningProcessBlock.deleteLater()

        self.runningProcessBlock = ProcessBlock(process)
        self.runningProcessLayout.insertWidget(0, self.runningProcessBlock)

        if not process:
            for key in self.runningInformationLabels:
                self.runningInformationLabels[key].setText(f"{key.capitalize()}: N/A")
            
            return

        burst = f"{process.burstTime:.2f}" if process.burstTime is not None else "N/A"
        start = f"{process.startTime:.2f}" if process.startTime is not None else "N/A"
        completed = f"{process.completionTime:.2f}" if process.completionTime is not None else "N/A"
        remaining = f"{process.remaining_time:.2f}" if process.remaining_time is not None else "N/A"

        self.runningInformationLabels["pid"].setText(f"PID: {process.pid}")
        self.runningInformationLabels["priority"].setText(f"Priority: {process.priority}")
        self.runningInformationLabels["burstTime"].setText(f"Burst Time: {burst}")
        self.runningInformationLabels["startTime"].setText(f"Start Time: {start}")
        self.runningInformationLabels["completedTime"].setText(f"Completed Time: {completed}")
        self.runningInformationLabels["remainingTime"].setText(f"Remaining Time: {remaining}")

    @pyqtSlot(object)
    def updateReadyProcesses(self, processList: List[Process]):
        newPIDs = {process.pid for process in processList}
        oldPIDs = set(self.readyProcessBlocks.keys())

        removedPIDs = oldPIDs - newPIDs

        for pid in removedPIDs:
            removedBlock = self.readyProcessBlocks.pop(pid)
            self.readyLayout.removeWidget(removedBlock)
            removedBlock.setParent(None)
            removedBlock.deleteLater()            

        for process in processList:
            pid = process.pid
            if pid not in self.readyProcessBlocks:
                newProcessBlock = ProcessBlock(process)
                newProcessBlock.clicked.connect(self.updateProcessInformation)

                self.readyProcessBlocks[pid] = newProcessBlock
                self.readyLayout.addWidget(newProcessBlock)

        self.updatePrioritiesSection(processList)
        self.updateStatistics(processList)

    def updateProcessInformation(self, process: Process):
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


    def updatePrioritiesSection(self, processList: List[Process]):
        if len(processList) == 0:
            return

        priorityCounts = {i: 0 for i in range(10)}

        for process in processList:
            priorityCounts[process.priority] += 1

        for priority, count in priorityCounts.items():
            self.prioritiesLabels.get(priority).setText(
                f"Priority {priority} ({self.config['processGeneration']['priorities']['weights'][priority]:.2f}): {count} processes         ({(count / len(processList)) * 100:.2f}%)")

    def updateStatistics(self, processList: List[Process]):
        numProcesses = len(processList)
        
        if numProcesses == 0:
            return  

        totalBurstTimes = sum(process.burstTime for process in processList)
        self.statisticsLabels["totalExpectedTime"].setText(f"Total expected execution time: {totalBurstTimes:.2f}")
        
        # Average execution time        
        averageBurstTime = totalBurstTimes / numProcesses
        minBurstTime = min(process.burstTime for process in processList)
        maxBurstTime = max(process.burstTime for process in processList)
        self.statisticsLabels["averageExecutionTime"].setText(f"Average Execution Time: {averageBurstTime:.2f}   (min: {minBurstTime:.2f}, max: {maxBurstTime:.2f})")
        
        # Standard Deviation of burst time
        standardDeviation = math.sqrt(sum((process.burstTime - averageBurstTime) ** 2 for process in processList) / numProcesses)
        self.statisticsLabels["standardDeviation"].setText(f"Standard Deviation of Burst Time: {standardDeviation:.2f}")
        
        # Average inter-arrival time
        sortedArrivalTimes = sorted(process.arrivalTime for process in processList)
        averageInterArrivalTime = sum(sortedArrivalTimes[i+1] - sortedArrivalTimes[i] for i in range(len(sortedArrivalTimes) - 1)) / (numProcesses - 1) if numProcesses > 1 else 0
        self.statisticsLabels["averageInterArrivalTime"].setText(f"Average Inter-Arrival Time: {averageInterArrivalTime:.2f}")
        
        # Total number of processes
        self.statisticsLabels["totalNumber"].setText(f"Total number of processes: {numProcesses}")

    # Creates running process section in the following format:
    #       
    #  Current Running Process  | Statistics about that Processs
    def runningProcessSection(self):
        containerGroup = QGroupBox("Running Process")
        runningProcessLayout = QHBoxLayout()
        
        # Process block on the left
        self.runningProcessBlock = ProcessBlock() 
        runningProcessLayout.addWidget(self.runningProcessBlock)
        
        # Information group in the middle
        informationGroup = QGroupBox("Information")
        informationLayout = QVBoxLayout()
        
        self.runningInformationLabels = {
            "pid": QLabel("PID: No"),
            "priority": QLabel("Priority: 0"),
            "burstTime": QLabel("Burst Time: 0"),
            "startTime": QLabel("Start time: 0"),
            "completedTime": QLabel("Completed Time: 0"),
            "remainingTime": QLabel("Remaining Time: 0"),
        }
        
        for label in self.runningInformationLabels.values():
            informationLayout.addWidget(label)
        
        informationGroup.setLayout(informationLayout)
        runningProcessLayout.addWidget(informationGroup)
        
        # Create a widget to hold the image and apply left padding
        imageContainer = QWidget()
        imageLayout = QHBoxLayout(imageContainer)
        
        # Set left margin to add padding (adjust the value as needed)
        imageLayout.setContentsMargins(100, 0, 0, 0)  # Left: 20px, others: 0px
        
        # Add the image to the layout
        image = QLabel()
        pixmap = QPixmap("./image_cropped.png")
        image.setPixmap(pixmap)
        imageLayout.addWidget(image)
        
        # Add the image container to the main layout
        runningProcessLayout.addWidget(imageContainer)
        
        containerGroup.setLayout(runningProcessLayout)
        self.mainLayout.addWidget(containerGroup)
        self.runningProcessLayout = runningProcessLayout

    # Creates ready queue section, which contains a list of ProcessBlocks
    def readyQueueSection(self):
        readyQueueGroup = QGroupBox("Ready Process Queue")
        readyQueueGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scrollWidget = QWidget()
        readyLayout = QHBoxLayout(scrollWidget)
        readyLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        readyLayout.setContentsMargins(0, 0, 0, 0)
        readyLayout.setSpacing(10)  
        
        scrollArea.setWidget(scrollWidget)
        
        readyQueueLayout = QVBoxLayout()
        readyQueueLayout.addWidget(scrollArea)
        readyQueueGroup.setLayout(readyQueueLayout)
        readyQueueGroup.setMaximumHeight(150)
        readyQueueLayout.setContentsMargins(0, 0, 0, 0)
        readyQueueLayout.setSpacing(0)

        self.mainLayout.addWidget(readyQueueGroup)

        self.readyLayout = readyLayout
        self.readyQueueGroup = readyQueueGroup

    def processInformation(self):
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
            "burstTime": QLabel("Burst Time: 0"),
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
    
    def prioritiesAndStatisticsSection(self):
        containerGroup = QGroupBox("Statistics")
        containerGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        # Horizontal layout to hold both sections
        containerLayout = QHBoxLayout()
        containerLayout.setSpacing(20)

        containerLayout.addWidget(self.prioritiesSection())
        containerLayout.addWidget(self.statisticsSection())
        containerGroup.setLayout(containerLayout)
        
        self.mainLayout.addWidget(containerGroup)


    def prioritiesSection(self):
        prioritiesGroup = QGroupBox("Priorities (Weight%)")
        prioritiesGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        prioritiesLayout = QGridLayout()
        prioritiesLayout.setVerticalSpacing(2)
        prioritiesLayout.setHorizontalSpacing(10)
        
        for i in range(10):
            row = i % 5
            col = i // 5
            label = QLabel(f"Priority {i} ({self.config['processGeneration']['priorities']['weights'][i]}): None")
            prioritiesLayout.addWidget(label, row, col)

            self.prioritiesLabels[i] = label
        
        prioritiesGroup.setLayout(prioritiesLayout)
        return prioritiesGroup
    
    def statisticsSection(self):
        # Statistics section
        statisticsGroup = QGroupBox("Statistics")
        statisticsGroup.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        statisticsLayout = QVBoxLayout()
        statisticsLayout.setSpacing(2)

        self.statisticsLabels = {
            "totalNumber": QLabel("Total number of processes: 0"),
            "totalExpectedTime": QLabel("Total expected execution time: 0"),
            "averageExecutionTime": QLabel("Average Execution Time: 0   (min: 0, max: 0)"),
            "averageInterArrivalTime": QLabel("Average Inter-Arrival Time: 0"),
            "standardDeviation": QLabel("Standard Deviation of Burst Time: 0")
        }
        
        for label in self.statisticsLabels.values():
            statisticsLayout.addWidget(label)
        
        statisticsGroup.setLayout(statisticsLayout)
        return statisticsGroup

 
