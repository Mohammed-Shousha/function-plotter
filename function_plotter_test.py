import pytest

from function_plotter import FunctionPlotter

from constants import RANGE_ERROR_MSG, FUNCTION_ERROR_MSG


@pytest.fixture
def app(qtbot):
    test_app = FunctionPlotter()
    qtbot.addWidget(test_app)
    return test_app


def test_labels(app):
    assert app.windowTitle() == 'Function Plotter'
    assert app.input_label.text() == 'Enter a mathematical function:'
    assert app.min_label.text() == 'Minimum x value:'
    assert app.max_label.text() == 'Maximum x value:'


def test_initial_range(app):
    assert app.min_spinbox.value() == -10
    assert app.max_spinbox.value() == 10


def test_initial_input(app):
    assert app.input_edit.text() == ''
    assert app.input_edit.placeholderText() == 'e.g. sin(x) + 2*x^2'


def test_spinbox_range(app):
    assert app.min_spinbox.minimum() == -1000
    assert app.min_spinbox.maximum() == 1000

    assert app.max_spinbox.minimum() == -1000
    assert app.max_spinbox.maximum() == 1000


def test_edit_spinbox(app):
    app.min_spinbox.setValue(-5)
    app.max_spinbox.setValue(5)

    app.min_spinbox.stepBy(-10)
    app.max_spinbox.stepBy(10)

    assert app.min_spinbox.value() == -15
    assert app.max_spinbox.value() == 15


def test_edit_input(app):
    app.input_edit.setText('x^2 + 2')
    assert app.input_edit.text() == 'x^2 + 2'

    app.input_edit.setText('')
    assert app.input_edit.text() == ''

    app.input_edit.setText('sin(x) + 2*x^2')
    assert app.input_edit.text() == 'sin(x) + 2*x^2'


def test_invalid_range(app):
    app.input_edit.setText('x^2')
    app.min_spinbox.setValue(5)
    app.max_spinbox.setValue(-5)
    app.plot_button.click()

    assert app.warning_label.text() == 'Invalid input: ' + RANGE_ERROR_MSG


def test_invalid_function(app):
    app.input_edit.setText('x^2 + ')
    app.min_spinbox.setValue(-5)
    app.max_spinbox.setValue(5)
    app.plot_button.click()

    assert app.warning_label.text() == 'Invalid input: ' + FUNCTION_ERROR_MSG


def test_first_degree_function(app):
    app.input_edit.setText('2*x + 2')
    app.min_spinbox.setValue(-5)
    app.max_spinbox.setValue(5)
    app.plot_button.click()

    assert app.figure.axes[0].lines[0].get_ydata()[0] == -8
    assert app.figure.axes[0].lines[0].get_ydata()[-1] == 12


def test_second_degree_function(app):
    app.input_edit.setText('x^2 + 2')
    app.min_spinbox.setValue(-5)
    app.max_spinbox.setValue(5)
    app.plot_button.click()

    assert app.figure.axes[0].lines[0].get_ydata()[0] == 27
    assert app.figure.axes[0].lines[0].get_ydata()[-1] == 27
