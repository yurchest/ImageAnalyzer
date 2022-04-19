from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5,4), dpi=200)
        super().__init__(fig)

        self.setParent(parent)

        x = np.array([50, 30, 40])
        self.ax.plot(x, [1,2,3])

