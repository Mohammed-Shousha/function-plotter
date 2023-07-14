from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QWidget,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

import numpy as np
import sys

from utils import validate_input, create_expression_function
from constants import RANGE_ERROR_MSG, FUNCTION_ERROR_MSG, RANGE
from styles import INPUT_STYLE, WARNING_STYLE, BUTTON_STYLE, WINDOW_STYLE


class FunctionPlotter(QWidget):
    def __init__(self):
        super().__init__()

        # set up user input widgets
        self.input_label = QLabel('Enter a mathematical function:')
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('e.g. sin(x) + 2*x^2')
        self.input_edit.returnPressed.connect(self.plot)
        self.input_edit.setStyleSheet(INPUT_STYLE)

        self.min_label = QLabel('Minimum x value:')
        self.min_spinbox = QDoubleSpinBox()
        self.min_spinbox.setRange(*RANGE)
        self.min_spinbox.setValue(-10)
        self.min_spinbox.setStyleSheet(INPUT_STYLE)

        self.max_label = QLabel('Maximum x value:')
        self.max_spinbox = QDoubleSpinBox()
        self.max_spinbox.setRange(*RANGE)
        self.max_spinbox.setValue(10)
        self.max_spinbox.setStyleSheet(INPUT_STYLE)

        self.plot_button = QPushButton('Plot')
        self.plot_button.setStyleSheet(BUTTON_STYLE)
        self.plot_button.clicked.connect(self.plot)

        # set up warning label
        self.warning_label = QLabel()
        self.warning_label.setStyleSheet(WARNING_STYLE)

        # set up plot display
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        # set up layout
        self.input_layout = QHBoxLayout()
        self.input_layout.addWidget(self.input_label)
        self.input_layout.addWidget(self.input_edit)

        self.range_layout = QHBoxLayout()
        self.range_layout.addWidget(self.min_label)
        self.range_layout.addWidget(self.min_spinbox)
        self.range_layout.addWidget(self.max_label)
        self.range_layout.addWidget(self.max_spinbox)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.plot_button)

        self.plot_layout = QVBoxLayout()
        self.plot_layout.addLayout(self.input_layout)
        self.plot_layout.addLayout(self.range_layout)
        self.plot_layout.addLayout(self.button_layout)
        self.plot_layout.addWidget(self.toolbar)
        self.plot_layout.addWidget(self.canvas)
        self.plot_layout.addWidget(self.warning_label)

        self.setLayout(self.plot_layout)
        self.setWindowTitle('Function Plotter')
        self.setGeometry(100, 100, 800, 600)

    def show_warning(self, message):
        self.warning_label.setText('Invalid input: ' + message)

    def plot(self):
        user_input = self.input_edit.text()
        x_min = self.min_spinbox.value()
        x_max = self.max_spinbox.value()

        if x_min >= x_max:
            self.show_warning(RANGE_ERROR_MSG)
            return

        if not validate_input(user_input):
            self.show_warning(FUNCTION_ERROR_MSG)
            return

        try:
            expr = create_expression_function(user_input)
            x = np.linspace(x_min, x_max, 1000)
            y = expr(x)
        except:
            self.show_warning(FUNCTION_ERROR_MSG)
            return

        self.figure.clear()
        self.warning_label.setText('')
        ax = self.figure.add_subplot()
        ax.plot(x, y)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FunctionPlotter()
    window.setStyleSheet(WINDOW_STYLE)
    window.show()
    sys.exit(app.exec_())
