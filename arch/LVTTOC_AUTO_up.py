# Тестирование ФБ МТЗ через GUI

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import threading
import time

import pandas as pd

from LVTTOC_FB_MTZ import LVTTOC

class LVTTOC_GUI:
    def __init__(self, root):
        self.root = root 
        self.root.title("LVTTOC Tester/ Тестирование ФБ МТЗ для ЮНИТ-М300-Т2")
        self.lvttoc = None
        self.polling_thread = None  # Для управления потоком опроса
        self.is_polling = False     # Флаг для остановки опроса

        # Инициализация переменных для SGF параметров, настроек, входных и выходных значений
        self.sgf_params = {
            "SGF1_ptoc1": tk.IntVar(value=0),
            "SGF2_ptoc1": tk.IntVar(value=0),
            "SGF3_ptoc1": tk.IntVar(value=0),
            "SGF4_ptoc1": tk.IntVar(value=0),
            "SGF5_ptoc1": tk.IntVar(value=0),
            "SGF6_ptoc1": tk.IntVar(value=0),
            "SGF7_ptoc1": tk.IntVar(value=0),
            "SGF1_ptoc2": tk.IntVar(value=0),
            "SGF2_ptoc2": tk.IntVar(value=0),
            "SGF3_ptoc2": tk.IntVar(value=0),
            "SGF4_ptoc2": tk.IntVar(value=0),
            "SGF5_ptoc2": tk.IntVar(value=0),
            "SGF6_ptoc2": tk.IntVar(value=0),
            "SGF7_ptoc2": tk.IntVar(value=0),
            "SGF1_ptoc3": tk.IntVar(value=0),
            "SGF2_ptoc3": tk.IntVar(value=0),
            "SGF3_ptoc3": tk.IntVar(value=0),
            "SGF4_ptoc3": tk.IntVar(value=0),
            "SGF5_ptoc3": tk.IntVar(value=0),
            "SGF6_ptoc3": tk.IntVar(value=0),
            "SGF7_ptoc3": tk.IntVar(value=0),
            "SGF1_ptuv1": tk.IntVar(value=0),
            "SGF1_ptuv2": tk.IntVar(value=0),
            "SGF1_phar1": tk.IntVar(value=0),
            "SGF1_rblc1": tk.IntVar(value=0),
            "SGF1": tk.IntVar(value=0),
        }

        self.settings = {
            "T1_ptoc1": tk.DoubleVar(value=0.23),
            "Iset_ptoc1": tk.DoubleVar(value=3),
            "Icoarse_ptoc1": tk.DoubleVar(value=5),
            "T1_ptoc2": tk.DoubleVar(value=0),
            "Iset_ptoc2": tk.DoubleVar(value=1),
            "Icoarse_ptoc2": tk.DoubleVar(value=2),
            "T1_ptoc3": tk.DoubleVar(value=0),
            "Iset_ptoc3": tk.DoubleVar(value=1),
            "Icoarse_ptoc3": tk.DoubleVar(value=2),
            "Uop_ptuv1": tk.DoubleVar(value=40),
            "U2op_ptuv1": tk.DoubleVar(value=5),
            "Uop_ptuv2": tk.DoubleVar(value=40),
            "U2op_ptuv2": tk.DoubleVar(value=5),
            "Imax_phar1": tk.DoubleVar(value=3),
            "Ratio_phar1": tk.DoubleVar(value=0.4),
        }

        self.input_vars = {
            "VYVOD": tk.IntVar(value=0),
            "OV": tk.IntVar(value=0),
            "OVst_ptoc1": tk.IntVar(value=0),
            "OVst_ptoc2": tk.IntVar(value=0),
            "OVst_ptoc3": tk.IntVar(value=0),
            "NaSign_ptoc1": tk.IntVar(value=0),
            "NaSign_ptoc2": tk.IntVar(value=0),
            "NaSign_ptoc3": tk.IntVar(value=0),
            "SV1vkl": tk.IntVar(value=0),
            "SV2vkl": tk.IntVar(value=0),
            "IA": tk.DoubleVar(value=0),
            "IB": tk.DoubleVar(value=0),
            "IC": tk.DoubleVar(value=0),
            "IAB": tk.DoubleVar(value=0),
            "IBC": tk.DoubleVar(value=0),
            "ICA": tk.DoubleVar(value=0),
            "KZN1neipr": tk.IntVar(value=0),
            "VNN1vkl": tk.IntVar(value=0),
            "KZN2neipr": tk.IntVar(value=0),
            "VNN2vkl": tk.IntVar(value=0),
            "KPONvnesh_ptuv1": tk.IntVar(value=0),
            "UAB_ptuv1": tk.DoubleVar(value=0),
            "UBC_ptuv1": tk.DoubleVar(value=0),
            "UCA_ptuv1": tk.DoubleVar(value=0),
            "U2_ptuv1": tk.DoubleVar(value=0),
            "KPONvnesh_ptuv2": tk.IntVar(value=0),
            "UAB_ptuv2": tk.DoubleVar(value=0),
            "UBC_ptuv2": tk.DoubleVar(value=0),
            "UCA_ptuv2": tk.DoubleVar(value=0),
            "U2_ptuv2": tk.DoubleVar(value=0),
            "IA2harm": tk.DoubleVar(value=0),
            "IB2harm": tk.DoubleVar(value=0),
            "IC2harm": tk.DoubleVar(value=0),
        }

        self.output_labels = {}

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Frame for SGF parameters
        sgf_frame = ttk.LabelFrame(self.root, text="SGF Parameters")
        sgf_frame.grid(row=0, column=0, padx=0, pady=0, sticky="w")

        row = 0
        col = 0
        for key, var in self.sgf_params.items():
            ttk.Label(sgf_frame, text=key).grid(row=row, column=col, sticky="w")
            if "SGF7" in key:
                ttk.Combobox(sgf_frame, textvariable=var, values=[0, 1, 2], state="readonly").grid(row=row, column=col + 1)
            else:
                ttk.Combobox(sgf_frame, textvariable=var, values=[0, 1], state="readonly").grid(row=row, column=col + 1)
            row += 1
            if row >= 7:
                row = 0
                col += 2

        # Frame for settings
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.grid(row=1, column=0, padx=0, pady=0, sticky="w")

        row = 0
        col = 0
        for key, var in self.settings.items():
            ttk.Label(settings_frame, text=key).grid(row=row, column=col, sticky="w")
            ttk.Entry(settings_frame, textvariable=var).grid(row=row, column=col + 1)
            row += 1
            if row >= 10:
                row = 0
                col += 2

        # Frame for buttons
        buttons_frame = ttk.LabelFrame(self.root, text="Buttons")
        buttons_frame.grid(row=2, column=0, padx=0, pady=0, sticky="w")

        # Button Init
        ttk.Button(buttons_frame, text="Init", command=self.init_lvttoc).grid(row=1, column=1, columnspan=2, pady=10)

        # Button Start
        ttk.Button(buttons_frame, text="Start", command=self.start_polling).grid(row=2, column=1, pady=10)

        # Button Stop
        ttk.Button(buttons_frame, text="Stop", command=self.stop_polling).grid(row=2, column=2, pady=10)

        # Button Save
        ttk.Button(buttons_frame, text="Save", command=self.save_to_excel).grid(row=3, column=1, pady=10)

        # Button Load
        ttk.Button(buttons_frame, text="Load", command=self.load_from_excel).grid(row=3, column=2, pady=10)

        # Frame for input values
        input_frame = ttk.LabelFrame(self.root, text="Inputs")
        input_frame.grid(row=3, column=0, padx=0, pady=0, sticky="w")

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
        output_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")

        outputs = [
            "vvod_ptoc1", "oper_vyvod_ptoc1", "mtzA_pusk_ptoc1", "mtzB_pusk_ptoc1", "mtzC_pusk_ptoc1",
            "gen_pusk_ptoc1", "mtz_srabsign_ptoc1", "mtz_srab_ptoc1", "io_A_ptoc1", "io_B_ptoc1", "io_C_ptoc1",
            "vvod_ptoc2", "oper_vyvod_ptoc2", "mtzA_pusk_ptoc2", "mtzB_pusk_ptoc2", "mtzC_pusk_ptoc2",
            "gen_pusk_ptoc2", "mtz_srabsign_ptoc2", "mtz_srab_ptoc2", "io_A_ptoc2", "io_B_ptoc2", "io_C_ptoc2",
            "vvod_ptoc3", "oper_vyvod_ptoc3", "mtzA_pusk_ptoc3", "mtzB_pusk_ptoc3", "mtzC_pusk_ptoc3",
            "gen_pusk_ptoc3", "mtz_srabsign_ptoc3", "mtz_srab_ptoc3", "io_A_ptoc3", "io_B_ptoc3", "io_C_ptoc3",
            "kpon_pusk_ptuv1", "kpon_pusk_ptuv2",
            "ia_start_out_phar1", "ib_start_out_phar1", "ic_start_out_phar1", "start_phar1",
            "blok_rblc1", "mtz_pusk"
        ]

        row = 0
        for output in outputs:
            label = ttk.Label(output_frame, text=output, width=20, anchor="w")
            label.grid(row=row, column=0, sticky="w")
            self.output_labels[output] = label
            row += 1

    def init_lvttoc(self):
        self.lvttoc = LVTTOC(
            SGF1=self.sgf_params["SGF1"].get(),
            SGF1_ptoc1=self.sgf_params["SGF1_ptoc1"].get(),
            SGF2_ptoc1=self.sgf_params["SGF2_ptoc1"].get(),
            SGF3_ptoc1=self.sgf_params["SGF3_ptoc1"].get(),
            SGF4_ptoc1=self.sgf_params["SGF4_ptoc1"].get(),
            SGF5_ptoc1=self.sgf_params["SGF5_ptoc1"].get(),
            SGF6_ptoc1=self.sgf_params["SGF6_ptoc1"].get(),
            SGF7_ptoc1=self.sgf_params["SGF7_ptoc1"].get(),
            T1_ptoc1=self.settings["T1_ptoc1"].get(),
            Iset_ptoc1=self.settings["Iset_ptoc1"].get(),
            Icoarse_ptoc1=self.settings["Icoarse_ptoc1"].get(),
            SGF1_ptoc2=self.sgf_params["SGF1_ptoc2"].get(),
            SGF2_ptoc2=self.sgf_params["SGF2_ptoc2"].get(),
            SGF3_ptoc2=self.sgf_params["SGF3_ptoc2"].get(),
            SGF4_ptoc2=self.sgf_params["SGF4_ptoc2"].get(),
            SGF5_ptoc2=self.sgf_params["SGF5_ptoc2"].get(),
            SGF6_ptoc2=self.sgf_params["SGF6_ptoc2"].get(),
            SGF7_ptoc2=self.sgf_params["SGF7_ptoc2"].get(),
            T1_ptoc2=self.settings["T1_ptoc2"].get(),
            Iset_ptoc2=self.settings["Iset_ptoc2"].get(),
            Icoarse_ptoc2=self.settings["Icoarse_ptoc2"].get(),
            SGF1_ptoc3=self.sgf_params["SGF1_ptoc3"].get(),
            SGF2_ptoc3=self.sgf_params["SGF2_ptoc3"].get(),
            SGF3_ptoc3=self.sgf_params["SGF3_ptoc3"].get(),
            SGF4_ptoc3=self.sgf_params["SGF4_ptoc3"].get(),
            SGF5_ptoc3=self.sgf_params["SGF5_ptoc3"].get(),
            SGF6_ptoc3=self.sgf_params["SGF6_ptoc3"].get(),
            SGF7_ptoc3=self.sgf_params["SGF7_ptoc3"].get(),
            T1_ptoc3=self.settings["T1_ptoc3"].get(),
            Iset_ptoc3=self.settings["Iset_ptoc3"].get(),
            Icoarse_ptoc3=self.settings["Icoarse_ptoc3"].get(),
            SGF1_ptuv1=self.sgf_params["SGF1_ptuv1"].get(),
            Uop_ptuv1=self.settings["Uop_ptuv1"].get(),
            U2op_ptuv1=self.settings["U2op_ptuv1"].get(),
            SGF1_ptuv2=self.sgf_params["SGF1_ptuv2"].get(),
            Uop_ptuv2=self.settings["Uop_ptuv2"].get(),
            U2op_ptuv2=self.settings["U2op_ptuv2"].get(),
            SGF1_phar1=self.sgf_params["SGF1_phar1"].get(),
            Imax_phar1=self.settings["Imax_phar1"].get(),
            Ratio_phar1=self.settings["Ratio_phar1"].get(),
            SGF1_rblc1=self.sgf_params["SGF1_rblc1"].get(),
        )
        print("LVTTOC initialized")

    def start_polling(self):
        if self.lvttoc is None:
            print("LVTTOC not initialized")
            return

        self.is_polling = True
        self.polling_thread = threading.Thread(target=self.poll_inputs, daemon=True)
        self.polling_thread.start()

    def stop_polling(self):
        self.is_polling = False
        if self.polling_thread and self.polling_thread.is_alive():
            self.polling_thread.join()
        print("Polling stopped")

    def poll_inputs(self):
        while self.is_polling:
            inputs = {key: var.get() for key, var in self.input_vars.items()}
            result = self.lvttoc.Step(**inputs)

            # Обновление выходных значений
            for output, value in zip(self.output_labels.keys(), result):
                label = self.output_labels[output]
                label.config(text=f"{output}: {int(value)}")
                if int(value) == 1:
                    label.config(background="red")
                else:
                    label.config(background="green")

            time.sleep(0.1)

    def save_to_excel(self):
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
        with pd.ExcelWriter("data.xlsx", engine="openpyxl") as writer:
            sgf_df.to_excel(writer, sheet_name="SGF_Parameters", index=False)
            settings_df.to_excel(writer, sheet_name="Settings", index=False)
            inputs_df.to_excel(writer, sheet_name="Inputs", index=False)
            outputs_df.to_excel(writer, sheet_name="Outputs", index=False)

        print("Data saved to data.xlsx")

    def load_from_excel(self):
        # Выбор файла для загрузки
        file_path = askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            # Чтение данных из Excel
            xls = pd.ExcelFile(file_path)

            # Загрузка SGF Parameters
            sgf_df = pd.read_excel(xls, sheet_name="SGF_Parameters")
            for key, var in self.sgf_params.items():
                if key in sgf_df.columns:
                    var.set(sgf_df.at[0, key])

            # Загрузка Settings
            settings_df = pd.read_excel(xls, sheet_name="Settings")
            for key, var in self.settings.items():
                if key in settings_df.columns:
                    var.set(settings_df.at[0, key])

            # Загрузка Inputs
            inputs_df = pd.read_excel(xls, sheet_name="Inputs")
            for key, var in self.input_vars.items():
                if key in inputs_df.columns:
                    var.set(inputs_df.at[0, key])

            print("Data loaded successfully")

        except Exception as e:
            print(f"Error loading data: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LVTTOC_GUI(root)
    root.mainloop()