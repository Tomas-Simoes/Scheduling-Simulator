from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore    import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib
matplotlib.use('Qt5Agg')
from global_clock import GlobalClock

class WaitingOverTimeGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.completionTimeData = []
        self.derivativeData = []

        self.layout = QVBoxLayout(self)
        self.figure = plt.figure(figsize=(4, 4), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.canvas)

        # Primary axis
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title('Waiting Processes Over Time')
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Number of Waiting Processes')
        self.axes.grid(True)

        # Secondary axis for derivative
        self.ax2 = self.axes.twinx()
        self.ax2.set_ylabel('Waiting Rate', color='blue')

        # Plot lines with labels
        self.line, = self.axes.plot([], [], linestyle='-', color='#8c564b', label='Completed Processes')
        self.derivative_line, = self.ax2.plot([], [], linestyle='-', color='#1f77b4', label=r'$\mathrm{d}N/\mathrm{d}t$')

        # Single combined legend
        lines, labels = self.axes.get_legend_handles_labels()
        dlines, dlabels = self.ax2.get_legend_handles_labels()
        self.axes.legend(lines + dlines, labels + dlabels, loc='upper left')

    def redraw(self):
        if not self.completionTimeData:
            self.axes.set_xlim(0, 12)
            self.axes.set_ylim(0, 6)
            self.ax2.set_ylim(0, 1.2)
            self.canvas.draw()
            return

        times, counts = zip(*self.completionTimeData)
        self.line.set_data(times, counts)

        # Left axis limits (with extra padding)
        max_count = max(counts) if counts else 0
        y_max = max_count * 1.2 if max_count > 0 else 1.2
        self.axes.set_ylim(0, y_max)
        self.axes.set_xlim(0, max(times) * 1.2)

        # Derivative data
        if self.derivativeData:
            deriv_times, deriv_rates = zip(*self.derivativeData)
            self.derivative_line.set_data(deriv_times, deriv_rates)
            max_deriv = max(deriv_rates) if deriv_rates else 0
            y2_max = max_deriv * 1.3 if max_deriv > 0 else 1.2
            self.ax2.set_ylim(0, y2_max)
        else:
            self.ax2.set_ylim(0, 1.2)

        # Overall margins for slight zoom-out
        self.axes.margins(x=0.05, y=0.05)
        self.ax2.margins(y=0.1)

        self.canvas.draw()

    def addNewPoint(self, completedCount):
        self.completionTimeData.append((GlobalClock.getTime(), completedCount))

    def addNewDerivatePoint(self):
        if len(self.completionTimeData) < 2:
            return

        current_time = GlobalClock.getTime()
        window_size = 7500  
        recent = [(t, c) for t, c in self.completionTimeData if current_time - t <= window_size]

        if len(recent) >= 2:
            t0, c0 = recent[0]
            t1, c1 = recent[-1]
            dt = t1 - t0
            if dt > 100:
                rate = (c1 - c0) / (dt / 1000.0)
                rate = min(max(rate, 0), 5.0)
                self.derivativeData.append((current_time, rate))
                if len(self.derivativeData) > 200:
                    self.derivativeData = self.derivativeData[-100:]
                self.redraw()
