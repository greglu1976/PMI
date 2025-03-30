import sys
import importlib
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QCheckBox, QSlider, 
                             QDoubleSpinBox, QLineEdit, QPushButton)
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Circle
from matplotlib.backend_bases import MouseButton
from inspect import signature, Parameter

class UniversalVisualizer(FigureCanvas):
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        
        # Инициализация переменных
        self.cur_xlim = (0, 10)
        self.cur_ylim = (0, 10)
        self.press = None
        self.background = None
        self.test_instance = None
        self.test_method = None
        self.input_widgets = {}
        
        # Настройка событий
        self.mpl_connect('button_press_event', self.on_press)
        self.mpl_connect('button_release_event', self.on_release)
        self.mpl_connect('motion_notify_event', self.on_motion)
        self.mpl_connect('scroll_event', self.on_scroll)
        
    def load_class(self, class_path, method_name='execute'):
        """Загружает класс из строки вида 'module.submodule.ClassName'"""
        try:
            if not class_path or '.' not in class_path:
                raise ValueError("Class path must be in format 'module.ClassName'")
                
            module_path, class_name = class_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            self.test_instance = cls()
            self.test_method = getattr(self.test_instance, method_name, None)
            
            if self.test_method is None:
                raise AttributeError(f"Method '{method_name}' not found in class")
                
            self.setup_visualization()
            return True
        except Exception as e:
            print(f"Error loading class: {e}")
            return False
    
    def setup_visualization(self):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(self.cur_xlim)
        self.ax.set_ylim(self.cur_ylim)
        self.ax.axis('off')
        
        if not self.test_method:
            self.ax.text(5, 5, "No test class loaded", ha='center', va='center')
            self.draw()
            return
        
        # Анализ сигнатуры метода
        sig = signature(self.test_method)
        params = list(sig.parameters.values())
        
        # Рисуем основной блок
        rect = Rectangle((3, 2), 4, 6, linewidth=2, edgecolor='black', facecolor='lightgray')
        self.ax.add_patch(rect)
        self.ax.text(5, 7, self.test_instance.__class__.__name__, ha='center', va='center')
        
        # Входы слева
        self.input_circles = {}
        for i, param in enumerate(params):
            y_pos = 7 - i * 0.8
            self.ax.plot([1, 3], [y_pos, y_pos], 'k-')
            self.ax.text(0.5, y_pos, param.name, ha='right', va='center')
            
            circle = Circle((1, y_pos), 0.2, color='blue')
            self.ax.add_patch(circle)
            self.input_circles[param.name] = circle
        
        # Выходы справа
        self.output_circles = {}
        self.ax.text(7.5, 7.5, "Outputs:", ha='left', va='center')
        
        self.draw()
    
    def update_visualization(self, input_values, output_values):
        if not self.test_method:
            return
            
        # Обновляем входы
        if hasattr(input_values, 'items'):
            for name, value in input_values.items():
                color = self._get_color_for_value(value)
                if name in self.input_circles:
                    self.input_circles[name].set_color(color)
        
        # Обновляем выходы
        if output_values is None:
            return
            
        if not hasattr(output_values, 'items'):
            output_values = {'result': output_values}
        
        for i, (name, value) in enumerate(output_values.items()):
            y_pos = 7 - i * 0.8
            if name not in self.output_circles:
                self.ax.plot([7, 9], [y_pos, y_pos], 'k-')
                self.ax.text(9.5, y_pos, name, ha='left', va='center')
                circle = Circle((9, y_pos), 0.2, color='green')
                self.ax.add_patch(circle)
                self.output_circles[name] = circle
            
            color = self._get_color_for_value(value)
            self.output_circles[name].set_color(color)
        
        self.draw()
    
    def _get_color_for_value(self, value):
        """Определяет цвет на основе типа значения"""
        if isinstance(value, bool):
            return 'red' if value else 'green'
        elif isinstance(value, (int, float)):
            return 'blue'
        return 'purple'
    
    # Обработчики событий для перемещения и масштабирования
    def on_press(self, event):
        if event.button == MouseButton.LEFT:
            self.press = event.xdata, event.ydata, self.cur_xlim, self.cur_ylim
    
    def on_release(self, event):
        self.press = None
        self.background = None
    
    def on_motion(self, event):
        if self.press is None or event.inaxes != self.ax: return
        
        xpress, ypress, xlim, ylim = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        
        self.cur_xlim = (xlim[0] - dx, xlim[1] - dx)
        self.cur_ylim = (ylim[0] - dy, ylim[1] - dy)
        
        self.ax.set_xlim(self.cur_xlim)
        self.ax.set_ylim(self.cur_ylim)
        self.draw()
    
    def on_scroll(self, event):
        if event.inaxes != self.ax: return
        
        scale_factor = 1.2 if event.button == 'up' else 1/1.2
        
        # Получаем текущие границы
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        # Вычисляем новые границы
        new_width = (xlim[1] - xlim[0]) * scale_factor
        new_height = (ylim[1] - ylim[0]) * scale_factor
        
        # Центр масштабирования - положение курсора
        x_center = event.xdata
        y_center = event.ydata
        
        # Устанавливаем новые границы
        self.ax.set_xlim([x_center - new_width/2, x_center + new_width/2])
        self.ax.set_ylim([y_center - new_height/2, y_center + new_height/2])
        
        self.cur_xlim = self.ax.get_xlim()
        self.cur_ylim = self.ax.get_ylim()
        
        self.draw()


class ControlPanel(QWidget):
    def __init__(self, visualizer):
        super().__init__()
        self.visualizer = visualizer
        self.input_widgets = {}
        self.parameter_widgets = {}  # Для хранения виджетов параметров
        self.timer = QTimer()
        self.timer.timeout.connect(self.execute_test)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Поле для ввода пути к классу
        self.class_path_edit = QLineEdit()
        self.class_path_edit.setPlaceholderText("module.submodule.ClassName")
        layout.addWidget(QLabel("Class path:"))
        layout.addWidget(self.class_path_edit)
        
        # Кнопка загрузки класса
        load_btn = QPushButton("Load Class")
        load_btn.clicked.connect(self._handle_load_class)
        layout.addWidget(load_btn)
        
        # Группа параметров класса
        self.param_group = QWidget()
        param_layout = QVBoxLayout(self.param_group)
        param_layout.addWidget(QLabel("Параметры класса:"))
        
        # Поля для SGF1 и Iset
        self.sgf1_check = QCheckBox("SGF1 (Активен)")
        param_layout.addWidget(self.sgf1_check)
        
        self.iset_spin = QDoubleSpinBox()
        self.iset_spin.setRange(0, 100)
        self.iset_spin.setSingleStep(0.1)
        param_layout.addWidget(QLabel("Iset:"))
        param_layout.addWidget(self.iset_spin)
        
        layout.addWidget(self.param_group)
        
        # Область для входных параметров метода
        self.inputs_group = QWidget()
        self.inputs_layout = QVBoxLayout(self.inputs_group)
        self.inputs_layout.addWidget(QLabel("Входные параметры:"))
        layout.addWidget(self.inputs_group)
        
        # Кнопки управления
        btn_layout = QHBoxLayout()
        
        start_btn = QPushButton("Start (0.3s)")
        start_btn.clicked.connect(self.startTimer)
        btn_layout.addWidget(start_btn)
        
        stop_btn = QPushButton("Stop")
        stop_btn.clicked.connect(self.stopTimer)
        btn_layout.addWidget(stop_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def startTimer(self):  # Переименовано в startTimer
        """Запускает периодический опрос с интервалом 0.3 секунды"""
        self.timer.start(300)  # 300 ms = 0.3 секунды

    def stopTimer(self):  # Переименовано в stopTimer
        """Останавливает периодический опрос"""
        self.timer.stop()
    
    def _handle_load_class(self):
        class_path = self.class_path_edit.text().strip()
        if not class_path:
            print("Please enter class path")
            return
            
        if self.visualizer.load_class(class_path):
            # Устанавливаем начальные значения параметров
            if hasattr(self.visualizer.test_instance, 'SGF1'):
                self.sgf1_check.setChecked(self.visualizer.test_instance.SGF1 == 1)
            if hasattr(self.visualizer.test_instance, 'Iset'):
                self.iset_spin.setValue(self.visualizer.test_instance.Iset)
            
            self.setup_input_controls()
    
    def setup_input_controls(self):
        # Очищаем предыдущие элементы управления
        for i in reversed(range(self.inputs_layout.count())): 
            widget = self.inputs_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.input_widgets.clear()
        
        if not self.visualizer.test_method:
            return
            
        sig = signature(self.visualizer.test_method)
        for name, param in sig.parameters.items():
            if param.annotation == bool:
                widget = QCheckBox(name)
                self.input_widgets[name] = (widget, bool)
                self.inputs_layout.addWidget(widget)
            elif param.annotation == int:
                widget = QSlider(Qt.Horizontal)
                widget.setRange(0, 100)
                self.input_widgets[name] = (widget, int)
                self.inputs_layout.addWidget(QLabel(name))
                self.inputs_layout.addWidget(widget)
            else:
                widget = QDoubleSpinBox()
                widget.setRange(0, 100)
                widget.setSingleStep(0.1)
                self.input_widgets[name] = (widget, float)
                self.inputs_layout.addWidget(QLabel(name))
                self.inputs_layout.addWidget(widget)
    
    def execute_test(self):
        if not self.visualizer.test_method:
            return
        
        # Обновляем параметры класса
        if hasattr(self.visualizer.test_instance, 'set_SGF1'):
            self.visualizer.test_instance.set_SGF1(1 if self.sgf1_check.isChecked() else 0)
        if hasattr(self.visualizer.test_instance, 'Iset'):
            self.visualizer.test_instance.Iset = self.iset_spin.value()
        
        # Собираем входные значения
        input_values = {}
        for name, (widget, typ) in self.input_widgets.items():
            if typ == bool:
                value = widget.isChecked()
            elif typ == int:
                value = widget.value()
            else:
                value = widget.value()
            input_values[name] = value
        
        # Выполняем метод
        try:
            result = self.visualizer.test_method(**input_values)
            self.visualizer.update_visualization(input_values, result)
        except Exception as e:
            print(f"Error executing method: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Создаем визуализатор
        self.visualizer = UniversalVisualizer()
        
        # Создаем панель управления
        self.control_panel = ControlPanel(self.visualizer)
        
        # Настройка интерфейса
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.addWidget(self.visualizer, stretch=2)
        layout.addWidget(self.control_panel, stretch=1)
        
        self.setCentralWidget(central_widget)
        self.setWindowTitle('Universal Class Visualizer')
        self.resize(1200, 800)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())