import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QSlider, QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from dozersim.results.results import Analysis
from dozersim.simulation import parameters, objectives
from dozersim.visualizations.plotting import get_variable_plot, plot_results_3d, plot_results_scatter, \
    plot_results_2d

app = QApplication(sys.argv)


class Visualization(QMainWindow):
    def __init__(self, parent=None, title: str = "Dozer simulation gui"):
        super().__init__()
        self.setWindowTitle(title)
        self.current_window = -1
        self.tabs_main = QTabWidget()
        self.setCentralWidget(self.tabs_main)
        self.resize(1280, 900)
        self._analyses: list[Analysis] = []
        self._analyses_windows: list[AnalysisWindows] = []
        self.show()

    @property
    def analysis(self):
        return self._analyses[-1]

    def add_analysis(self, analysis: Analysis):
        self._analyses.append(analysis)
        analysis_tab = AnalysisWindows(analysis=analysis)
        self.tabs_main.addTab(analysis_tab, f'analysis {len(self._analyses)}')
        self._analyses_windows.append(analysis_tab)

    def add_plot(self, x_object: parameters.Parameter | objectives.Objective,
                 y_object: parameters.Parameter | objectives.Objective,
                 z_object: parameters.Parameter | objectives.Objective = None,
                 plot_type: str = 'line'):
        self._analyses_windows[-1].add_plot(x_object, y_object, z_object, plot_type)


class AnalysisWindows(QTabWidget):

    def __init__(self, analysis: Analysis, parent=None):
        super().__init__(parent)
        self.additional_plots = []
        self._analysis = analysis
        self.result_tabs = QTabWidget()

        self.plot_variables()
        var_tab = QWidget()
        self.addTab(var_tab, 'Results')
        layout = QVBoxLayout()
        var_tab.setLayout(layout)

        bar = QWidget()
        label = QLabel()
        label.setText(f'Select set between 1 and {len(self._analysis.results)}:')
        pushButton = QPushButton()
        pushButton.setText('Confirm selection')
        pushButton.setMaximumWidth(150)
        spinBox = QSpinBox()
        spinBox.setMinimum(1)
        spinBox.setMaximum(len(self._analysis.results))
        # spinBox.setPrefix('set ')
        # spinBox.setSuffix(f' of {len(self._analysis.results)}')
        spinBox.setMaximumWidth(150)
        spinBox.setMinimumWidth(100)
        bar_layout = QHBoxLayout()
        bar_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        bar_layout.addWidget(label)
        bar_layout.addWidget(spinBox)
        bar_layout.addWidget(pushButton)
        bar.setLayout(bar_layout)
        layout.addWidget(bar)
        layout.addWidget(self.result_tabs)
        headers, data = analysis.get_analysis_table()
        self.addTab(MyTable(headers=headers, data=data), 'Sets')

    def plot_variables(self, idx: int = -1):
        result_idx = self._analysis.results[idx]

        for load_case in result_idx.load_cases:
            path_tabs = QTabWidget()
            for path in result_idx.paths:
                if path is not None:
                    variables = result_idx.get_variables(load_case, path)
                    variable_tabs = QTabWidget()
                    for var in variables:
                        variable_tabs.addTab(MyPlot(fig=get_variable_plot(var)), var.name)
                    path_tabs.addTab(variable_tabs, path.name)
            headers, data = result_idx.get_result_table(load_case=load_case)
            path_tabs.addTab(MyTable(headers=headers, data=data), 'Results')
            # tabs_level1.addTab(tabs_level2, load_case)

            self.result_tabs.addTab(path_tabs, load_case)

    def add_plot(self, x_object, y_object, z_object=None,
                 plot_type: str = 'line'):
        res_collection = self._analysis
        z_type = issubclass(type(z_object), (parameters.Parameter | objectives.Objective))
        fig = plot_dict[z_type, plot_type](res_collection, x_object, y_object, z_object)
        self.additional_plots.append(fig)
        self.addTab(MyPlot(fig=fig), f'plot {len(self.additional_plots)}')


plot_dict = {
    (False, 'line'): plot_results_2d,
    (False, 'scatter'): plot_results_scatter,
    (True, 'line'): plot_results_3d
}


class MyPlot(QWidget):

    def __init__(self, parent=None, fig: Figure = None):
        super().__init__()
        sc = FigureCanvas(figure=fig)
        layout = QVBoxLayout()
        self.setLayout(layout)
        new_toolbar = NavigationToolbar(sc)
        layout.addWidget(sc)
        layout.addWidget(new_toolbar)


def show_plots():
    app.exec()


class MyTable(QWidget):
    def __init__(self, headers, data, parent=None):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        new_table = QTableWidget()
        new_table.setRowCount(len(data))
        new_table.setColumnCount(len(data[0]))
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                q_item = QTableWidgetItem(item)
                new_table.setItem(i, j, q_item)
        # new_table.resizeColumnsToContents()
        new_table.resizeRowsToContents()
        new_table.setHorizontalHeaderLabels(headers)
        new_table.move(0, 0)
        layout.addWidget(new_table)
