import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QCheckBox, QSlider, QDoubleSpinBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Circle
from matplotlib.backend_bases import MouseButton

class RSTrigger:
    def __init__(self, state=0):
        self.state = state
    
    def run(self, set_condition, reset_condition):
        if set_condition:
            self.state = 1
        elif reset_condition:
            self.state = 0
        return self.state

class STRPTOC:
    def __init__(self, SGF1, Iset):
        self.SGF1 = SGF1
        self.Iset = Iset
        self.RS = RSTrigger(state=0)

    def Step(self, VYVOD, OV, OVst, IA, IB, IC):
        vvod = (not (OV or VYVOD or OVst)) and (self.SGF1 == 1)
        oper_vyvod = (OV or VYVOD or OVst) and (self.SGF1 == 1)
        
        I = max(IA, IB, IC)
        io = (self.SGF1 == 1) and (self.RS.run((I >= self.Iset), (I < 0.95 * self.Iset)))
        pusk = vvod and io
        
        return vvod, oper_vyvod, pusk, io
    
    def get_SGF1(self):
        return self.SGF1
    
    def set_SGF1(self, value):
        self.SGF1 = value

class STRPTOCVisualizer(FigureCanvas):
    def __init__(self, strptoc, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.strptoc = strptoc
        
        # Инициализация переменных для масштабирования/перемещения
        self.cur_xlim = (0, 10)
        self.cur_ylim = (0, 10)
        self.press = None
        self.background = None
        
        self.setup_visualization()
        
        # Подключаем обработчики событий
        self.mpl_connect('button_press_event', self.on_press)
        self.mpl_connect('button_release_event', self.on_release)
        self.mpl_connect('motion_notify_event', self.on_motion)
        self.mpl_connect('scroll_event', self.on_scroll)
        
    def setup_visualization(self):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(self.cur_xlim)
        self.ax.set_ylim(self.cur_ylim)
        self.ax.axis('off')
        
        # Рисуем прямоугольник (основной блок)
        rect = Rectangle((3, 2), 4, 6, linewidth=2, edgecolor='black', facecolor='lightgray')
        self.ax.add_patch(rect)
        
        # Добавляем текст с названием класса
        self.ax.text(5, 7, 'STRPTOC', ha='center', va='center', fontsize=12)
        
        # Входы слева
        inputs = ['SGF1', 'VYVOD', 'OV', 'OVst', 'IA', 'IB', 'IC', 'Iset']
        self.input_circles = {}
        for i, inp in enumerate(inputs):
            y_pos = 7 - i * 0.8
            self.ax.plot([1, 3], [y_pos, y_pos], 'k-')
            self.ax.text(0.5, y_pos, inp, ha='right', va='center')
            
            # Создаем кружки для входов
            circle = Circle((1, y_pos), 0.2, color='blue')
            self.ax.add_patch(circle)
            self.input_circles[inp] = circle
        
        # Выходы справа
        outputs = ['vvod', 'oper_vyvod', 'pusk', 'io']
        self.output_circles = {}
        for i, out in enumerate(outputs):
            y_pos = 7 - i * 0.8
            self.ax.plot([7, 9], [y_pos, y_pos], 'k-')
            self.ax.text(9.5, y_pos, out, ha='left', va='center')
            
            # Создаем кружки для выходов
            circle = Circle((9, y_pos), 0.2, color='green')
            self.ax.add_patch(circle)
            self.output_circles[out] = circle
        
        self.draw()
    
    def update_input_colors(self, VYVOD, OV, OVst, SGF1):
        # Обновляем цвета дискретных входов
        self.input_circles['VYVOD'].set_color('red' if VYVOD else 'green')
        self.input_circles['OV'].set_color('red' if OV else 'green')
        self.input_circles['OVst'].set_color('red' if OVst else 'green')
        self.input_circles['SGF1'].set_color('red' if SGF1 == 1 else 'green')
        self.draw()
    
    def update_output_colors(self, vvod, oper_vyvod, pusk, io):
        # Обновляем цвета выходов
        self.output_circles['vvod'].set_color('red' if vvod else 'green')
        self.output_circles['oper_vyvod'].set_color('red' if oper_vyvod else 'green')
        self.output_circles['pusk'].set_color('red' if pusk else 'green')
        self.output_circles['io'].set_color('red' if io else 'green')
        self.draw()
    
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
    def __init__(self, strptoc, visualizer):
        super().__init__()
        self.strptoc = strptoc
        self.visualizer = visualizer
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # SGF1 (0 или 1)
        sg1_layout = QHBoxLayout()
        sg1_layout.addWidget(QLabel("SGF1:"))
        self.sg1_checkbox = QCheckBox("1 (активно)")
        self.sg1_checkbox.setChecked(self.strptoc.get_SGF1() == 1)
        self.sg1_checkbox.stateChanged.connect(self.update_visualization)
        sg1_layout.addWidget(self.sg1_checkbox)
        layout.addLayout(sg1_layout)
        
        # Флажки для boolean входов
        self.vyvod_check = QCheckBox("VYVOD")
        self.vyvod_check.stateChanged.connect(self.update_visualization)
        layout.addWidget(self.vyvod_check)
        
        self.ov_check = QCheckBox("OV")
        self.ov_check.stateChanged.connect(self.update_visualization)
        layout.addWidget(self.ov_check)
        
        self.ovst_check = QCheckBox("OVst")
        self.ovst_check.stateChanged.connect(self.update_visualization)
        layout.addWidget(self.ovst_check)
        
        # Слайдеры для токов
        self.ia_slider = self.create_slider("IA:", 0, 10, 0.1, 0)
        layout.addWidget(self.ia_slider)
        
        self.ib_slider = self.create_slider("IB:", 0, 10, 0.1, 0)
        layout.addWidget(self.ib_slider)
        
        self.ic_slider = self.create_slider("IC:", 0, 10, 0.1, 0)
        layout.addWidget(self.ic_slider)
        
        # Уставка Iset
        self.iset_spin = QDoubleSpinBox()
        self.iset_spin.setRange(0, 10)
        self.iset_spin.setSingleStep(0.1)
        self.iset_spin.setValue(self.strptoc.Iset)
        self.iset_spin.valueChanged.connect(self.update_visualization)
        iset_layout = QHBoxLayout()
        iset_layout.addWidget(QLabel("Iset:"))
        iset_layout.addWidget(self.iset_spin)
        layout.addLayout(iset_layout)
        
        self.setLayout(layout)
    
    def create_slider(self, label, min_val, max_val, step, init_val):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        layout.addWidget(QLabel(label))
        
        slider = QSlider(Qt.Horizontal)
        slider.setRange(int(min_val / step), int(max_val / step))
        slider.setValue(int(init_val / step))
        slider.valueChanged.connect(self.update_visualization)
        
        spin = QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setSingleStep(step)
        spin.setValue(init_val)
        spin.valueChanged.connect(lambda v: slider.setValue(int(v / step)))
        
        slider.valueChanged.connect(lambda v: spin.setValue(v * step))
        
        layout.addWidget(slider)
        layout.addWidget(spin)
        
        return widget
    
    def update_visualization(self):
        # Получаем значения из элементов управления
        sg1 = 1 if self.sg1_checkbox.isChecked() else 0
        vyvod = self.vyvod_check.isChecked()
        ov = self.ov_check.isChecked()
        ovst = self.ovst_check.isChecked()
        ia = self.ia_slider.layout().itemAt(1).widget().value() * 0.1
        ib = self.ib_slider.layout().itemAt(1).widget().value() * 0.1
        ic = self.ic_slider.layout().itemAt(1).widget().value() * 0.1
        iset = self.iset_spin.value()
        
        # Обновляем параметры STRPTOC
        self.strptoc.set_SGF1(sg1)
        self.strptoc.Iset = iset
        
        # Выполняем шаг
        vvod, oper_vyvod, pusk, io = self.strptoc.Step(vyvod, ov, ovst, ia, ib, ic)
        
        # Обновляем визуализацию
        self.visualizer.update_input_colors(vyvod, ov, ovst, sg1)
        self.visualizer.update_output_colors(vvod, oper_vyvod, pusk, io)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Создаем экземпляр STRPTOC
        self.strptoc = STRPTOC(SGF1=1, Iset=5.0)
        
        # Создаем визуализатор
        self.visualizer = STRPTOCVisualizer(self.strptoc)
        
        # Создаем панель управления
        self.control_panel = ControlPanel(self.strptoc, self.visualizer)
        
        # Настраиваем основной интерфейс
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.addWidget(self.visualizer, stretch=2)
        layout.addWidget(self.control_panel, stretch=1)
        
        self.setCentralWidget(central_widget)
        self.setWindowTitle('STRPTOC Visualizer')
        self.resize(1000, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())