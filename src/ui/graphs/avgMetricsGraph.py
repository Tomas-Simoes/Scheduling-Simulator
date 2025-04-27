# ui/graphs/metricsGraph.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore    import pyqtSlot
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure               import Figure
from global_clock import GlobalClock

class AvgMetricsGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Holds (time, avg_turnaround, avg_waiting) samples
        self.data = []

        self.fig = Figure(dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Expanding)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Completition Metrics Average")
        self.ax.set_xlabel("Time (ms)")
        self.ax.set_ylabel("Units")
        self.ax.grid(True)

        self.line_turn, = self.ax.plot([], [], label="Avg Turnaround")
        self.line_wait, = self.ax.plot([], [], label="Avg Waiting")
        self.line_response, = self.ax.plot([], [], label="Avg Response Time")

        self.ax.legend()
        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

    # Receives current a list of completed processes and calculates averages .
    @pyqtSlot(object)
    def updateGraph(self, completed):
        if completed:
            avg_turnaround = sum(p.turnaroundTime for p in completed) / len(completed)
            avg_waiting    = sum(p.waitingTime    for p in completed) / len(completed)
            avg_responseTime  = sum(((p.firstScheduling / 1000) - p.arrivalTime) for p in completed) / len(completed)
        else:
            avg_turnaround = avg_waiting = avg_responseTime = 0.0

        self.data.append((GlobalClock.getTime(), avg_turnaround, avg_waiting, avg_responseTime))
        self.redraw()

    def redraw(self):
        times, turns, waits, response = zip(*self.data)

        self.line_turn.set_data(times, turns)
        self.line_wait.set_data(times, waits)
        self.line_response.set_data(times, response)

        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
