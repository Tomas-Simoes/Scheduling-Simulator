from PyQt6.QtCore import QDateTime

class GlobalClock():
    currentTime_ms = 0
    simulationTime_ms = 0
    lastRealTime = 0

    def updateGlobalTime():
        nowRealTime = QDateTime.currentMSecsSinceEpoch()
        timeElapsed = nowRealTime - GlobalClock.lastRealTime

        GlobalClock.currentTime_ms = GlobalClock.simulationTime_ms + timeElapsed

    def setSimulationTime(time):
        GlobalClock.lastRealTime = QDateTime.currentMSecsSinceEpoch()
        GlobalClock.simulationTime_ms = time 

    def getTime():
        return GlobalClock.currentTime_ms