# GUI imports
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)

# Plotting imports
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

# Utilities imports
import numpy as np
import sys
import re

# TODO: use regex directly to check for invalid input
# TODO: add constarints to input
# TODO: provide feedback on invalid input

# list of allowed words to be entered by the user
allowed_words = [
    'x',
    'sin',
    'cos',
    'sqrt',
    'exp',
    'tan',
    'log',
    '/',
    '+',
    '*',
    '^',
    '-',
    '(',
    ')',
]

pattern = r'^(\s*([0-9]+(?:\.[0-9]+)?|{})\s*)+$'.format(
    '|'.join(map(re.escape, allowed_words)))


# dictionary of replacements for string to mathematical expression conversion
replacements = {
    'sin': 'np.sin',
    'cos': 'np.cos',
    'sqrt': 'np.sqrt',
    'exp': 'np.exp',
    'tan': 'np.tan',
    'log': 'np.log',
    '^': '**',
}

# define main application window


class FunctionPlotter(QWidget):
    def __init__(self):
        super().__init__()

        # set up user input widgets
        self.input_label = QLabel('Enter a mathematical expression:')
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('e.g. sin(x) + 2*x^2')
        self.input_edit.returnPressed.connect(self.plot)

        self.min_label = QLabel('Minimum x value:')
        self.min_spinbox = QDoubleSpinBox()
        self.min_spinbox.setRange(-1000, 1000)
        self.min_spinbox.setValue(-10)

        self.max_label = QLabel('Maximum x value:')
        self.max_spinbox = QDoubleSpinBox()
        self.max_spinbox.setRange(-1000, 1000)
        self.max_spinbox.setValue(10)

        self.plot_button = QPushButton('Plot')
        self.plot_button.clicked.connect(self.plot)

        # set up plot display
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
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

        self.setLayout(self.plot_layout)
        self.setWindowTitle('Function Plotter')
        self.setGeometry(100, 100, 800, 600)

    # define function to plot user input
    def validate_input(self, user_input):
        return re.match(pattern, user_input)

    def plot(self):
        # get user input
        user_input = self.input_edit.text()
        x_min = self.min_spinbox.value()
        x_max = self.max_spinbox.value()

        # check if input is valid
        # for word in re.findall(r'[a-zA-Z]+|[!@#$%^&*()_+=.-]', user_input):
        #     print(word)
        #     if word not in allowed_words:
        #         # Display warning message and return if any word is not allowed
        #         QMessageBox.warning(
        #             self, 'Invalid Input', 'Please enter a valid mathematical expression.')
        #         return

        if not self.validate_input(user_input):
            QMessageBox.warning(self, 'Invalid Input',
                                'Please enter a valid mathematical expression.')
            return

        # convert input to mathematical expression
        for word, replacement in replacements.items():
            user_input = user_input.replace(word, replacement)
        try:
            def expr(x): return eval(user_input)
            x = np.linspace(x_min, x_max, 1000)
            y = expr(x)

        except:
            QMessageBox.warning(self, 'Invalid Input',
                                'Please enter a valid mathematical expression.')
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.canvas.draw()


if __name__ == '__main__':
    # create application instance
    app = QApplication(sys.argv)

    # create main window instance
    window = FunctionPlotter()

    # show main window
    window.show()

    # run event loop
    sys.exit(app.exec_())
