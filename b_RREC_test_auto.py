import tkinter as tk
from tkinter import ttk
import threading
import time

from lib._FUNCS.LVLINRREC import LVLINRREC  # Импортируем класс для тестирования

class LVLINRREC_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Тестирование функции АПВ")
        self.lvlinrrec = None
        self.polling_thread = None
        self.is_polling = False

        # Инициализация переменных для SGF параметров и настроек
        self.sgf_params = {
            "SGF1": tk.IntVar(value=0),  # Ввод функции в работу
            "SGF2": tk.IntVar(value=0),  # Режим контроля напряжения
            "SGF3": tk.IntVar(value=0),  # Контроль синхронизма и напряжений
            "SGF4": tk.IntVar(value=0),  # Количество циклов АПВ
            "SGF5": tk.IntVar(value=0),  # Блокировка второго цикла при ОЗЗ
        }

        self.settings = {
            "T1": tk.DoubleVar(value=1),  # Таймер готовности для однократного АПВ
            "T2": tk.DoubleVar(value=2),  # Таймер готовности для двухкратного АПВ
            "T3": tk.DoubleVar(value=1.5),  # Таймер задержки включения
            "T4": tk.DoubleVar(value=0.5),  # Таймер задержки второго цикла
            "T5": tk.DoubleVar(value=2.5),  # Таймер задержки включения второго цикла
            "T6": tk.DoubleVar(value=0.5),  # 
        }

        # Инициализация переменных для входных значений
        self.input_vars = {
            "VYVOD": tk.IntVar(value=0),  # Выход
            "OV": tk.IntVar(value=0),  # Оперативный вывод
            "KSV_blk": tk.IntVar(value=0),  # Блокировка КСВ
            "Vvkl": tk.IntVar(value=0),  # Включение
            "KSV_rfk": tk.IntVar(value=0),  # Режим КСВ
            "ZAPV_zapv": tk.IntVar(value=0),  # Запрет АПВ
            "Vnesh_zaprAPV": tk.IntVar(value=0),  # Внешний запрет АПВ
            "APV_blk2cycl": tk.IntVar(value=0),  # Блокировка второго цикла
            "GSOZZ": tk.IntVar(value=0),  # Готовность СЗЗ
            "KSV_avarotkl": tk.IntVar(value=0),  # Аварийное отключение КСВ
            "KS_razrAvtVklV": tk.IntVar(value=0),  # Разрешение автоматического включения
            "APV_bezKontr": tk.IntVar(value=0),  # АПВ без контроля
            "APV_KNNSH": tk.IntVar(value=0),  # АПВ с контролем КННш
            "APV_KONsh": tk.IntVar(value=0),  # АПВ с контролем КОНш
            "KNNsh_pusk": tk.IntVar(value=0),  # Пуск КННш
            "KONp_pusk": tk.IntVar(value=0),  # Пуск КОНп
            "KONsh_pusk": tk.IntVar(value=0),  # Пуск КОНш
            "KNNp_pusk": tk.IntVar(value=0),  # Пуск КННп
        }

        # Инициализация переменных для выходных значений
        self.output_labels = {}

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Frame для SGF параметров
        sgf_frame = ttk.LabelFrame(self.root, text="SGF Parameters")
        sgf_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        row = 0
        col = 0
        for key, var in self.sgf_params.items():
            ttk.Label(sgf_frame, text=key).grid(row=row, column=col, sticky="w")
            ttk.Combobox(sgf_frame, textvariable=var, values=[0, 1, 2, 3, 4], state="readonly").grid(row=row, column=col + 1)
            row += 1
            if row >= 5:
                row = 0
                col += 2

        # Frame для настроек
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        row = 0
        col = 0
        for key, var in self.settings.items():
            ttk.Label(settings_frame, text=key).grid(row=row, column=col, sticky="w")
            ttk.Entry(settings_frame, textvariable=var).grid(row=row, column=col + 1)
            row += 1
            if row >= 6:
                row = 0
                col += 2

        # Frame для кнопок
        buttons_frame = ttk.LabelFrame(self.root, text="Buttons")
        buttons_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Кнопка Init
        ttk.Button(buttons_frame, text="Init", command=self.init_lvlinrrec).grid(row=0, column=0, pady=10)

        # Кнопка Start
        ttk.Button(buttons_frame, text="Start", command=self.start_polling).grid(row=0, column=1, pady=10)

        # Кнопка Stop
        ttk.Button(buttons_frame, text="Stop", command=self.stop_polling).grid(row=0, column=2, pady=10)

        # Frame для входных значений
        input_frame = ttk.LabelFrame(self.root, text="Inputs")
        input_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        row = 0
        col = 0
        for key, var in self.input_vars.items():
            ttk.Label(input_frame, text=key).grid(row=row, column=col, sticky="w")
            ttk.Checkbutton(input_frame, variable=var).grid(row=row, column=col + 1)
            row += 1
            if row >= 10:
                row = 0
                col += 2

        # Frame для выходных значений
        output_frame = ttk.LabelFrame(self.root, text="Outputs")
        output_frame.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")

        outputs = [
            "vvod", "oper_vyvod", "apv_gotov_1", "apv_gotov_2", "apv_tekush_cycl",
            "apv_1_cycl", "apv_vkl", "apv_2_cycl", "apv_tek_2_cycl", "apv_zaderzh_vkl",
            "apv_vkl_ks", "ET_t1", "ET_t2", "ET_t3", "ET_t4", "ET_t5", "ET_t6", "_p001", "_p002", "_p003", "_p004", "_p005", "_p006", "_p007", "_p008", "_p009", "_p010", "_p011", "_p012", "_p013", "_p014"
        ]

        row = 0
        col = 0
        for output in outputs:
            label = ttk.Label(output_frame, text=output, width=20, anchor="w")
            label.grid(row=row, column=col, sticky="w")
            self.output_labels[output] = label
            row += 1
            if row >= 17:
                row = 0
                col += 2

    def init_lvlinrrec(self):
        self.lvlinrrec = LVLINRREC(
            SGF1=self.sgf_params["SGF1"].get(),
            SGF2=self.sgf_params["SGF2"].get(),
            SGF3=self.sgf_params["SGF3"].get(),
            SGF4=self.sgf_params["SGF4"].get(),
            SGF5=self.sgf_params["SGF5"].get(),
            T1=self.settings["T1"].get(),
            T2=self.settings["T2"].get(),
            T3=self.settings["T3"].get(),
            T4=self.settings["T4"].get(),
            T5=self.settings["T5"].get(),
            T6=self.settings["T6"].get(),
        )
        print("LVLINRREC initialized")

    def start_polling(self):
        if self.lvlinrrec is None:
            print("LVLINRREC not initialized")
            return

        self.is_polling = True
        self.polling_thread = threading.Thread(target=self.poll_inputs, daemon=True)
        self.polling_thread.start()

    def stop_polling(self):
        self.is_polling = False
        if self.polling_thread and self.polling_thread.is_alive():
            self.polling_thread.join(timeout=1.0)
        print("Polling stopped")

    def poll_inputs(self):
        while self.is_polling:
            inputs = {key: var.get() for key, var in self.input_vars.items()}
            result = self.lvlinrrec.Step(**inputs)

            # Обновление выходных значений
            for output, value in zip(self.output_labels.keys(), result):
                label = self.output_labels[output]
                label.config(text=f"{output}: {value}")
                if value != 0:
                    label.config(background="red")
                else:
                    label.config(background="green")

            time.sleep(0.3)  # Время шага опроса


if __name__ == "__main__":
    root = tk.Tk()
    app = LVLINRREC_GUI(root)
    root.mainloop()