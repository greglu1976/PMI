import tkinter as tk
from tkinter import ttk
import threading
import time

from lib._FUNCS.LVTRRCBF import LVTRRCBF  # Импортируем класс для тестирования

class LVTRRCBF_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Тестирование функции КСВ")
        self.lvtrrcbf = None
        self.polling_thread = None
        self.is_polling = False

        # Инициализация переменных для SGF параметров
        self.sgf_params = {
            "SGF1": tk.IntVar(value=0),  # Ввод функции в работу
            "SGF2": tk.IntVar(value=0),  # Блокировка включения низкого уровня контроля изоляции
            "SGF3": tk.IntVar(value=0),  # Блокировка включения от неисправности положения В
            "SGF4": tk.IntVar(value=0),  # Блокировка включения от превышения ресурса В
            "SGF5": tk.IntVar(value=0),  # Контроль ОТ цепей ЭМВ, ЭМО1 и ЭМО2
            "SGF6": tk.IntVar(value=0),  # Контроль ЭМВ, ЭМО1 и ЭМО2 при формировании неисправности цепей ЭМУ
            "SGF7": tk.IntVar(value=0),  # Контроль низкого уровня изоляции для работы аварийного уровня изоляции
            "SGF8": tk.IntVar(value=0),  # Разрешение сброса "РФК" от кнопки
            "SGF9": tk.IntVar(value=0),  # Блокировка управления от аварийного уровня контроля изоляции
        }

        # Инициализация переменных для настроек таймеров
        self.settings = {
            "T1": tk.DoubleVar(value=1),  # Таймер 1
            "T2": tk.DoubleVar(value=2),  # Таймер 2
            "T3": tk.DoubleVar(value=1.5),  # Таймер 3
        }

        # Инициализация переменных для входных значений
        self.input_vars = {
            "VYVOD": tk.IntVar(value=0),  # Выход
            "OV": tk.IntVar(value=0),  # Оперативный вывод
            "ot_emo1emv": tk.IntVar(value=0),  # От ЭМО1 и ЭМВ
            "ot_emo2": tk.IntVar(value=0),  # От ЭМО2
            "lovn_otkl": tk.IntVar(value=0),  # ЛОВН отключение
            "urov_nasebya": tk.IntVar(value=0),  # Уровень на себя
            "avar_isol_V": tk.IntVar(value=0),  # Аварийный уровень изоляции В
            "niz_isol_V": tk.IntVar(value=0),  # Низкий уровень изоляции В
            "pruzh_ne_zaved": tk.IntVar(value=0),  # Пружина не заведена
            "V_neispr_pol": tk.IntVar(value=0),  # Неисправность положения В
            "V_otkl": tk.IntVar(value=0),  # Отключение В
            "V_vkl": tk.IntVar(value=0),  # Включение В
            "Sbros": tk.IntVar(value=0),  # Сброс
            "UV_otkl": tk.IntVar(value=0),  # УВ отключение
            "otkl_ot_knopk": tk.IntVar(value=0),  # Отключение от кнопки
            "oper_otkl_V": tk.IntVar(value=0),  # Оперативное отключение В
            "KRV_resurs_V": tk.IntVar(value=0),  # Превышение ресурса В
            "vnesh_blok_upr_V": tk.IntVar(value=0),  # Внешняя блокировка управления В
            "kontr_emv": tk.IntVar(value=0),  # Контроль ЭМВ
            "kontr_emo1": tk.IntVar(value=0),  # Контроль ЭМО1
            "kontr_emo2": tk.IntVar(value=0),  # Контроль ЭМО2
            "rabota_emv": tk.IntVar(value=0),  # Работа ЭМВ
            "rabota_emo1": tk.IntVar(value=0),  # Работа ЭМО1
            "rabota_emo2": tk.IntVar(value=0),  # Работа ЭМО2
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
            ttk.Combobox(sgf_frame, textvariable=var, values=[0, 1, 2], state="readonly").grid(row=row, column=col + 1)
            row += 1
            if row >= 5:
                row = 0
                col += 2

        # Frame для настроек таймеров
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        row = 0
        col = 0
        for key, var in self.settings.items():
            ttk.Label(settings_frame, text=key).grid(row=row, column=col, sticky="w")
            ttk.Entry(settings_frame, textvariable=var).grid(row=row, column=col + 1)
            row += 1

        # Frame для кнопок
        buttons_frame = ttk.LabelFrame(self.root, text="Buttons")
        buttons_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Кнопка Init
        ttk.Button(buttons_frame, text="Init", command=self.init_lvtrrcbf).grid(row=0, column=0, pady=10)

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
            if row >= 13:
                row = 0
                col += 2

        # Frame для выходных значений
        output_frame = ttk.LabelFrame(self.root, text="Outputs")
        output_frame.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")

        outputs = [
            "vvod", "oper_vyvod", "ksv_v_samoproisv_otkl", "ksv_neispr_V", "ksv_v_avar_otkl",
            "ksv_rfk", "ksv_blok_vkl", "ksv_blok_otkl", "ksv_neisp_emu", "ksv_zashita_emv",
            "ksv_zashita_emo1", "ksv_zashita_emo2", "ET_t1", "ET_t2", "ET_t31", "ET_t32", "ET_t33",
            "_p001", "_p002", "_p003", "_p004", "_p005", "_p006", "_p007", "_p008", "_p009", "_p010"
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

    def init_lvtrrcbf(self):
        self.lvtrrcbf = LVTRRCBF(
            SGF1=self.sgf_params["SGF1"].get(),
            SGF2=self.sgf_params["SGF2"].get(),
            SGF3=self.sgf_params["SGF3"].get(),
            SGF4=self.sgf_params["SGF4"].get(),
            SGF5=self.sgf_params["SGF5"].get(),
            SGF6=self.sgf_params["SGF6"].get(),
            SGF7=self.sgf_params["SGF7"].get(),
            SGF8=self.sgf_params["SGF8"].get(),
            SGF9=self.sgf_params["SGF9"].get(),
            T1=self.settings["T1"].get(),
            T2=self.settings["T2"].get(),
            T3=self.settings["T3"].get(),
        )
        print("LVTRRCBF initialized")

    def start_polling(self):
        if self.lvtrrcbf is None:
            print("LVTRRCBF not initialized")
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
            result = self.lvtrrcbf.Step(**inputs)

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
    app = LVTRRCBF_GUI(root)
    root.mainloop()