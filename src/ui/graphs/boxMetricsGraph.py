# ui/graphs/boxPlotMetricsGraph.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QLabel
from PyQt6.QtCore    import pyqtSlot
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure               import Figure

class BoxMetricsGraph(QWidget):
    """
    Displays distributions of completion metrics (turnaround, waiting, response times) as
    box-and-whisker plots. Ideal for summarizing algorithm performance at simulation end.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.turnaround_times = []
        self.waiting_times = []
        self.response_times = []

        # Set up figure and canvas
        self.layout = QVBoxLayout(self)
        self.fig = Figure(dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.canvas)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Completion Metrics Distribution")
        self.ax.set_ylabel("Time (ms)")


    @pyqtSlot(object)
    def updateGraph(self, completed):
        """
        Receive list of completed processes at simulation end.
        Each process has attributes: turnaroundTime, waitingTime, firstScheduling, arrivalTime.
        """
        if not completed:
            return

        # Gather metrics
        self.turnaround_times = [p.turnaroundTime for p in completed]
        self.waiting_times    = [p.waitingTime    for p in completed]
        self.response_times   = [ (p.firstScheduling / 1000.0) - p.arrivalTime for p in completed ]

        self.redraw()

    def redraw(self):
        # Clear previous
        self.ax.clear()

        # Restore title and axis label
        self.ax.set_title("Completion Metrics Distribution")
        self.ax.set_ylabel("Time (ms)")

        data = [self.turnaround_times, self.waiting_times, self.response_times]

        # Boxplot
        bp = self.ax.boxplot(data, patch_artist=True)

        # Color the boxes
        colors = ['lightcoral', 'lightblue', 'lightgreen']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)

        # Grid on y-axis
        self.ax.grid(True, axis='y', linestyle='--', alpha=0.7)

        self.ax.legend([bp["boxes"][0], bp["boxes"][1], bp["boxes"][2]],
                    ["Turnaround", "Waiting", "Response"],
                    loc="upper right")

        self.canvas.draw()

