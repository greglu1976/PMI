import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import threading
import time
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.dimensions import ColumnDimension
import openpyxl

# Импортируем класс partTOKZ
from lib._PARTS.TOKZ import partTOKZ

class PartOfTOKGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Тестирование токовых функций ФСУ, v1.0 от 24.03.25")
        self.part = None
        self.polling_thread = None
        self.is_polling = False

        # Инициализация переменных для имени файла
        self.function_name = tk.StringVar(value="Функция")
        self.mode_name = tk.StringVar(value="Режим")

        # Инициализация переменных для параметров SGF и настроек
        self.sgf_params = {
            "SGF1_ptoc1_lvtoc": tk.IntVar(value=0),
            "SGF2_ptoc1_lvtoc": tk.IntVar(value=0),
            "SGF1_hvptoc1_lovctoc": tk.IntVar(value=0),
            "SGF1_ptoc1_lvarctoc": tk.IntVar(value=0),
            "SGF2_ptoc1_lvarctoc": tk.IntVar(value=0),
            "SGF1_ptoc1_ltcblktoc": tk.IntVar(value=0), 
            #"SGF1_hvptoc1_strpalc": tk.IntVar(value=0),
            #"SGF1_lvptoc1_strpalc": tk.IntVar(value=0),
            #"SGF1_lvptoc2_strpalc": tk.IntVar(value=0),
            "SGF1_nsptoc1_lvnstoc": tk.IntVar(value=0),
            "SGF2_nsptoc1_lvnstoc": tk.IntVar(value=0),
            "SGF1_ptrc1_ttoclgc": tk.IntVar(value=0),
            "SGF2_ptrc1_ttoclgc": tk.IntVar(value=0),
            "SGF3_ptrc1_ttoclgc": tk.IntVar(value=0),
            "SGF1_ptrc1_tofflvlgc": tk.IntVar(value=0),
            "SGF1_rbre1_tofflvlgc": tk.IntVar(value=0),
            "SGF2_rbre1_tofflvlgc": tk.IntVar(value=0),
            "SGF3_rbre1_tofflvlgc": tk.IntVar(value=0),
            "SGF1_rblc1_tofflvlgc": tk.IntVar(value=0),
            "SGF2_rblc1_tofflvlgc": tk.IntVar(value=0),
            "SGF3_rblc1_tofflvlgc": tk.IntVar(value=0),
        }

        self.settings = {
            "T1_ptoc1_lvtoc": tk.DoubleVar(value=1),
            "Iset_ptoc1_lvtoc": tk.DoubleVar(value=1),
            "T1_hvptoc1_lovctoc": tk.DoubleVar(value=1),
            "Iset_hvptoc1_lovctoc": tk.DoubleVar(value=1),
            "Iset_ptoc1_lvarctoc": tk.DoubleVar(value=1),
            "Iset_ptoc1_ltcblktoc": tk.DoubleVar(value=1),
            #"Iset_hvptoc1_strpalc": tk.DoubleVar(value=1),
            #"Iset_lvptoc1_strpalc": tk.DoubleVar(value=1),
            #"Iset_lvptoc2_strpalc": tk.DoubleVar(value=1),
            "T1_nsptoc1_lvnstoc": tk.DoubleVar(value=1),
            "I2set_nsptoc1_lvnstoc": tk.DoubleVar(value=1),
            "RatioSet_nsptoc1_lvnstoc": tk.DoubleVar(value=1),
            "In_nsptoc1_lvnstoc": tk.DoubleVar(value=1),
            "T1_ptrc1_ttoclgc": tk.DoubleVar(value=1),
        }

        self.input_vars = {
            "VYVOD": tk.IntVar(value=0),
            "IA": tk.DoubleVar(value=0),
            "dIA": tk.DoubleVar(value=0),
            "IB": tk.DoubleVar(value=0),
            "dIB": tk.DoubleVar(value=0),
            "IC": tk.DoubleVar(value=0),
            "dIC": tk.DoubleVar(value=0),
            #"IA1": tk.DoubleVar(value=0),
            #"IB1": tk.DoubleVar(value=0),
            #"IC1": tk.DoubleVar(value=0),
            #"IA2": tk.DoubleVar(value=0),
            #"IB2": tk.DoubleVar(value=0),
            #"IC2": tk.DoubleVar(value=0),                        
            "OV_ptoc1_lvtoc": tk.IntVar(value=0),
            "NaSign_ptoc1_lvtoc": tk.IntVar(value=0),
            "OV_hvptoc1_lovctoc": tk.IntVar(value=0),
            "NaOtkl_hvptoc1_lovctoc": tk.IntVar(value=0),
            "OV_ptoc1_lvarctoc": tk.IntVar(value=0),
            "mtz1_pusk": tk.IntVar(value=0),
            "mtz2_pusk": tk.IntVar(value=0),
            "mtz3_pusk": tk.IntVar(value=0),
            "OV_ptoc1_ltcblktoc": tk.IntVar(value=0),            
            #"OV_strpalc": tk.IntVar(value=0),
            #"OV_hvptoc1_strpalc": tk.IntVar(value=0),
            #"OV_lvptoc1_strpalc": tk.IntVar(value=0),
            #"OV_lvptoc2_strpalc": tk.IntVar(value=0),
            "OV_nsptoc1_lvnstoc": tk.IntVar(value=0),
            "NaSign_nsptoc1_lvnstoc": tk.IntVar(value=0),
            "OV_ptrc1_ttoclgc": tk.IntVar(value=0),
            "vnesh_pusk_ptrc1_ttoclgc": tk.IntVar(value=0),
            "blok_lzt_ptrc1_ttoclgc": tk.IntVar(value=0),
            "OV_tofflvlg": tk.IntVar(value=0),
            "OVlo_tofflvlg": tk.IntVar(value=0),
            "OVzapv_tofflvlg": tk.IntVar(value=0),
            "OVzavr_tofflvlg": tk.IntVar(value=0),
        }

        self.output_labels = {}

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Frame for SGF parameters
        sgf_frame = ttk.LabelFrame(self.root, text="SGF Parameters")
        sgf_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        row = 0
        col = 0
        for key, var in self.sgf_params.items():
            ttk.Label(sgf_frame, text=key).grid(row=row, column=col, sticky="w")
            ttk.Combobox(sgf_frame, textvariable=var, values=[0, 1, 2], state="readonly").grid(row=row, column=col + 1)
            row += 1
            if row >= 10:
                row = 0
                col += 2

        # Frame for settings
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        row = 0
        col = 0
        for key, var in self.settings.items():
            ttk.Label(settings_frame, text=key).grid(row=row, column=col, sticky="w")
            ttk.Entry(settings_frame, textvariable=var).grid(row=row, column=col + 1)
            row += 1
            if row >= 9:
                row = 0
                col += 2


        # Frame for buttons
        buttons_frame = ttk.LabelFrame(self.root, text="Buttons")
        buttons_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Button Init
        ttk.Button(buttons_frame, text="Init", command=self.init_part).grid(row=0, column=0, pady=10)
        # Button Start
        ttk.Button(buttons_frame, text="Start", command=self.start_polling).grid(row=0, column=1, pady=10)
        # Button Stop
        ttk.Button(buttons_frame, text="Stop", command=self.stop_polling).grid(row=0, column=2, pady=10)
        # Button Save
        ttk.Button(buttons_frame, text="Save", command=self.save_to_excel).grid(row=0, column=3, pady=10)
        # Button Load
        ttk.Button(buttons_frame, text="Load", command=self.load_from_excel).grid(row=0, column=4, pady=10)

        # Поля для задания имени файла
        ttk.Label(buttons_frame, text="Функция:").grid(row=0, column=5, padx=5, pady=5)
        ttk.Entry(buttons_frame, textvariable=self.function_name, width=15).grid(row=0, column=6, padx=5, pady=5)
        ttk.Label(buttons_frame, text="Режим:").grid(row=0, column=7, padx=5, pady=5)
        ttk.Entry(buttons_frame, textvariable=self.mode_name, width=15).grid(row=0, column=8, padx=5, pady=5)

        # Добавляем новый элемент (например, Label) с возможностью изменения цвета
        self.status_label = ttk.Label(buttons_frame, text="Шаг", background="green", foreground="white")
        self.status_label.grid(row=0, column=9, padx=5, pady=5)

        # Frame for input values
        input_frame = ttk.LabelFrame(self.root, text="Inputs")
        input_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        row = 0
        col = 0
        for key, var in self.input_vars.items():
            if isinstance(var, tk.IntVar):
                ttk.Checkbutton(input_frame, text=key, variable=var).grid(row=row, column=col, sticky="w")
            elif isinstance(var, tk.DoubleVar):
                ttk.Label(input_frame, text=key).grid(row=row, column=col, sticky="w")
                ttk.Entry(input_frame, textvariable=var).grid(row=row, column=col + 1)
            row += 1
            if row >= 5:
                row = 0
                col += 2

        # Frame for output values
        output_frame = ttk.LabelFrame(self.root, text="Outputs")
        output_frame.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        outputs = [
            "vvod_ptoc1_lvtoc", "oper_vyvod_ptoc1_lvtoc", "pusk_ptoc1_lvtoc", "io_ptoc1_lvtoc", "srabsign_ptoc1_lvtoc", "srab_ptoc1_lvtoc",
            "vvod_hvptoc1_lovctoc", "oper_vyvod_hvptoc1_lovctoc", "pusk_hvptoc1_lovctoc", "io_hvptoc1_lovctoc", "srab_hvptoc1_lovctoc", "srabotkl_hvptoc1_lovctoc",
            "vvod_ptoc1_lvarctoc", "oper_vyvod_ptoc1_lvarctoc", "pusk_ptoc1_lvarctoc", "io_ptoc1_lvarctoc",
            #"vvod_hvptoc1_strpalc", "oper_vyvod_hvptoc1_strpalc", "pusk_hvptoc1_strpalc", "io_hvptoc1_strpalc", "vvod_lvptoc1_strpalc", "oper_vyvod_lvptoc1_strpalc", "pusk_lvptoc1_strpalc", "io_lvptoc1_strpalc", "vvod_lvptoc2_strpalc", "oper_vyvod_lvptoc2_strpalc", "pusk_lvptoc2_strpalc", "io_lvptoc2_strpalc", "pusk_strpalc", "vvod_strpalc",
            "vvod_nsptoc1_lvnstoc", "oper_vyvod_nsptoc1_lvnstoc", "srab_nsptoc1_lvnstoc", "srabsign_nsptoc1_lvnstoc", "pusk_nsptoc1_lvnstoc", "io_I2_nsptoc1_lvnstoc", "io_rat_nsptoc1_lvnstoc",
            "vvod_ptrc1_ttoclgc", "oper_vyvod_ptrc1_ttoclgc", "pusk_ptrc1_ttoclgc", "srab_ptrc1_ttoclgc",
            "vvod_ptrc1_tofflvlgc", "oper_vyvod_ptrc1_tofflvlgc", "pusk_ptrc1_tofflvlgc", "srab_ptrc1_tofflvlgc", "vvod_rblc1_tofflvlgc", "oper_vyvod_rblc1_tofflvlgc", "zapret_rblc1_tofflvlgc", "vvod_rbre1_tofflvlgc", "oper_vyvod_rbre1_tofflvlgc", "zapret_rbre1_tofflvlgc",
            "pusk_lvalv",
            "vvod_ptoc1_ltcblktoc", "oper_vyvod_ptoc1_ltcblktoc", "pusk_ptoc1_ltcblktoc", "io_ptoc1_ltcblktoc",             
            "IAB", "IBC", "ICA", "I1", "I2", "I0"
        ]

        row = 0
        col = 0
        for output in outputs:
            label = ttk.Label(output_frame, text=output, width=35, anchor="w")
            label.grid(row=row, column=col, sticky="w")
            self.output_labels[output] = label
            row += 1
            if row >= 32:
                row = 0
                col += 2

    def init_part(self):
        self.part = partTOKZ(
            SGF1_ptoc1_lvtoc=self.sgf_params["SGF1_ptoc1_lvtoc"].get(),
            SGF2_ptoc1_lvtoc=self.sgf_params["SGF2_ptoc1_lvtoc"].get(),
            T1_ptoc1_lvtoc=self.settings["T1_ptoc1_lvtoc"].get(),
            Iset_ptoc1_lvtoc=self.settings["Iset_ptoc1_lvtoc"].get(),
            SGF1_hvptoc1_lovctoc=self.sgf_params["SGF1_hvptoc1_lovctoc"].get(),
            T1_hvptoc1_lovctoc=self.settings["T1_hvptoc1_lovctoc"].get(),
            Iset_hvptoc1_lovctoc=self.settings["Iset_hvptoc1_lovctoc"].get(),
            SGF1_ptoc1_lvarctoc=self.sgf_params["SGF1_ptoc1_lvarctoc"].get(),
            SGF2_ptoc1_lvarctoc=self.sgf_params["SGF2_ptoc1_lvarctoc"].get(),
            Iset_ptoc1_lvarctoc=self.settings["Iset_ptoc1_lvarctoc"].get(),
            SGF1_ptoc1_ltcblktoc=self.sgf_params["SGF1_ptoc1_ltcblktoc"].get(),
            Iset_ptoc1_ltcblktoc=self.settings["Iset_ptoc1_ltcblktoc"].get(),                        
            #SGF1_hvptoc1_strpalc=self.sgf_params["SGF1_hvptoc1_strpalc"].get(),
            #Iset_hvptoc1_strpalc=self.settings["Iset_hvptoc1_strpalc"].get(),
            #SGF1_lvptoc1_strpalc=self.sgf_params["SGF1_lvptoc1_strpalc"].get(),
            #Iset_lvptoc1_strpalc=self.settings["Iset_lvptoc1_strpalc"].get(),
            #SGF1_lvptoc2_strpalc=self.sgf_params["SGF1_lvptoc2_strpalc"].get(),
           # Iset_lvptoc2_strpalc=self.settings["Iset_lvptoc2_strpalc"].get(),
            SGF1_nsptoc1_lvnstoc=self.sgf_params["SGF1_nsptoc1_lvnstoc"].get(),
            SGF2_nsptoc1_lvnstoc=self.sgf_params["SGF2_nsptoc1_lvnstoc"].get(),
            T1_nsptoc1_lvnstoc=self.settings["T1_nsptoc1_lvnstoc"].get(),
            I2set_nsptoc1_lvnstoc=self.settings["I2set_nsptoc1_lvnstoc"].get(),
            RatioSet_nsptoc1_lvnstoc=self.settings["RatioSet_nsptoc1_lvnstoc"].get(),
            In_nsptoc1_lvnstoc=self.settings["In_nsptoc1_lvnstoc"].get(),
            SGF1_ptrc1_ttoclgc=self.sgf_params["SGF1_ptrc1_ttoclgc"].get(),
            SGF2_ptrc1_ttoclgc=self.sgf_params["SGF2_ptrc1_ttoclgc"].get(),
            SGF3_ptrc1_ttoclgc=self.sgf_params["SGF3_ptrc1_ttoclgc"].get(),
            T1_ptrc1_ttoclgc=self.settings["T1_ptrc1_ttoclgc"].get(),
            SGF1_ptrc1_tofflvlgc=self.sgf_params["SGF1_ptrc1_tofflvlgc"].get(),
            SGF1_rbre1_tofflvlgc=self.sgf_params["SGF1_rbre1_tofflvlgc"].get(),
            SGF2_rbre1_tofflvlgc=self.sgf_params["SGF2_rbre1_tofflvlgc"].get(),
            SGF3_rbre1_tofflvlgc=self.sgf_params["SGF3_rbre1_tofflvlgc"].get(),
            SGF1_rblc1_tofflvlgc=self.sgf_params["SGF1_rblc1_tofflvlgc"].get(),
            SGF2_rblc1_tofflvlgc=self.sgf_params["SGF2_rblc1_tofflvlgc"].get(),
            SGF3_rblc1_tofflvlgc=self.sgf_params["SGF3_rblc1_tofflvlgc"].get(),
        )
        print("partTOKZ initialized")

    def start_polling(self):
        if self.part is None:
            print("partTOKZ not initialized")
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
            result = self.part.Step(**inputs)

            # Обновление выходных значений
            for output, value in zip(self.output_labels.keys(), result):
                label = self.output_labels[output]
                label.config(text=f"{output}: {round(value, 2)}")
                if int(value) != 0 or float(value)!=0:
                    label.config(background="red", foreground="white")
                else:
                    label.config(background="green", foreground="white")

            time.sleep(0.3)  # Время шага опроса
            self.status_label.config(text="Шаг", background="white", foreground="white")
            time.sleep(0.05)  # Время шага опроса
            self.status_label.config(text="Шаг", background="#F0F0F0", foreground="#F0F0F0")

    def save_to_excel(self):
        # Формируем имя файла
        function = self.function_name.get().strip()
        mode = self.mode_name.get().strip()
        if not function or not mode:
            print("Поля 'Функция' и 'Режим' должны быть заполнены")
            return
        output_file = f"{function}_{mode}.xlsx"

        # Создаем DataFrame для каждой группы данных
        sgf_df = pd.DataFrame({
            key: [var.get()] for key, var in self.sgf_params.items()
        })
        settings_df = pd.DataFrame({
            key: [var.get()] for key, var in self.settings.items()
        })
        inputs_df = pd.DataFrame({
            key: [var.get()] for key, var in self.input_vars.items()
        })
        outputs_df = pd.DataFrame({
            key: [label.cget("text").split(": ")[-1]] for key, label in self.output_labels.items()
        })

        # Сохраняем данные в Excel
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            sgf_df.to_excel(writer, sheet_name="SGF_Parameters", index=False)
            settings_df.to_excel(writer, sheet_name="Settings", index=False)
            inputs_df.to_excel(writer, sheet_name="Inputs", index=False)
            outputs_df.to_excel(writer, sheet_name="Outputs", index=False)

        # Применяем форматирование к файлу Excel
        wb = openpyxl.load_workbook(output_file)
        red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

        def format_sheet(sheet, df):
            """Функция для форматирования листа."""
            for col_num, column in enumerate(sheet.columns, start=1):
                column_letter = openpyxl.utils.get_column_letter(col_num)
                sheet.column_dimensions[column_letter].width = 20
                for row_num, cell in enumerate(column, start=1):
                    if row_num == 1:  # Пропускаем заголовки
                        continue
                    try:
                        value = float(cell.value)
                        if value != 0:
                            cell.fill = red_fill
                    except (ValueError, TypeError):
                        pass

        format_sheet(wb["SGF_Parameters"], sgf_df)
        format_sheet(wb["Settings"], settings_df)
        format_sheet(wb["Inputs"], inputs_df)
        format_sheet(wb["Outputs"], outputs_df)

        wb.save(output_file)
        print(f"Data saved to {output_file} with formatting")

    def load_from_excel(self):
        file_path = askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return
        try:
            xls = pd.ExcelFile(file_path)
            sgf_df = pd.read_excel(xls, sheet_name="SGF_Parameters")
            for key, var in self.sgf_params.items():
                if key in sgf_df.columns:
                    var.set(sgf_df.at[0, key])

            inputs_df = pd.read_excel(xls, sheet_name="Inputs")
            for key, var in self.input_vars.items():
                if key in inputs_df.columns:
                    var.set(inputs_df.at[0, key])

            print("Data loaded successfully")
        except Exception as e:
            print(f"Error loading data: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PartOfTOKGUI(root)
    root.mainloop()