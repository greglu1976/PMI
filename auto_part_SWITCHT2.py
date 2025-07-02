# автоматическое тестирование ФСУ T2 в части КСВ, КП, КА, УВ + СС, ПС

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

# Импортируем новый класс SWITCH3
from lib._PARTS.SWITCH_T2 import SWITCH

class PartOfSwitchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Тестирование ФСУ Т2 в части КСВ, КП, КА, УВ, СС, ПС и УРОВ. v1.0 01.07.25")
        self.part = None
        self.polling_thread = None
        self.is_polling = False

        # Инициализация переменных для имени файла
        self.function_name = tk.StringVar(value="Функция")
        self.mode_name = tk.StringVar(value="Режим")

        # Инициализация переменных для параметров SGF, настроек, входных и выходных значений
        self.sgf_params = {
            "SGF1_rcbf1_lvcbsup": tk.IntVar(value=0),
            "SGF2_rcbf1_lvcbsup": tk.IntVar(value=0),
            "SGF3_rcbf1_lvcbsup": tk.IntVar(value=0),
            "SGF4_rcbf1_lvcbsup": tk.IntVar(value=0),
            "SGF5_rcbf1_lvcbsup": tk.IntVar(value=0),
            "SGF6_rcbf1_lvcbsup": tk.IntVar(value=0),
            "SGF7_rcbf1_lvcbsup": tk.IntVar(value=0),
            "SGF8_rcbf1_lvcbsup": tk.IntVar(value=0),
            "SGF1_swctrl": tk.IntVar(value=0),
            "SGF1_cbcswi1_swctrl": tk.IntVar(value=0),
            "SGF2_cbcswi1_swctrl": tk.IntVar(value=0),
            "SGF1_cbcswi1_hvbctrl": tk.IntVar(value=0),
            "SGF1_tsd": tk.IntVar(value=0),
            "SGF1_xcbr1_tsd": tk.IntVar(value=0),
            "SGF2_xcbr1_tsd": tk.IntVar(value=0),
            "SGF3_xcbr1_tsd": tk.IntVar(value=0),
            "SGF4_xcbr1_tsd": tk.IntVar(value=0),
            "SGF5_xcbr1_tsd": tk.IntVar(value=0),
            "SGF6_xcbr1_tsd": tk.IntVar(value=0),
            "SGF1_rbrf1_tpbrf": tk.IntVar(value=0),
            "SGF2_rbrf1_tpbrf": tk.IntVar(value=0),
            "SGF3_rbrf1_tpbrf": tk.IntVar(value=0),
            "SGF4_rbrf1_tpbrf": tk.IntVar(value=0),
            "SGF5_rbrf1_tpbrf": tk.IntVar(value=0),
            "SGF6_rbrf1_tpbrf": tk.IntVar(value=0),
            "SGF1_hvcbptrc1_hvtcboff": tk.IntVar(value=0),
            "SGF9_lvalh": tk.IntVar(value=0),
        }

        self.settings = {
            "T1_rcbf1_lvcbsup": tk.DoubleVar(value=1),
            "T2_rcbf1_lvcbsup": tk.DoubleVar(value=1),
            "T3_rcbf1_lvcbsup": tk.DoubleVar(value=1),
            "T1_cbcswi1_swctrl": tk.DoubleVar(value=1),
            "T2_cbcswi1_swctrl": tk.DoubleVar(value=1),
            "T3_cbcswi1_swctrl": tk.DoubleVar(value=1),
            "T4_cbcswi1_swctrl": tk.DoubleVar(value=1),
            "T1_cbcswi1_hvbctrl": tk.DoubleVar(value=1),
            "T1_xcbr1_tsd": tk.DoubleVar(value=1),
            "T2_xcbr1_tsd": tk.DoubleVar(value=1),
            "T3_xcbr1_tsd": tk.DoubleVar(value=1),
            "T4_xcbr1_tsd": tk.DoubleVar(value=1),
            "T1_rbrf1_tpbrf": tk.DoubleVar(value=1),
            "Iset_rbrf1_tpbrf": tk.DoubleVar(value=0.2),
            "T1_hvcbptrc1_hvtcboff": tk.DoubleVar(value=1),            
        }

        self.input_vars = {
            "VYVOD": tk.IntVar(value=0),
            "OV_rcbf1_lvcbsup": tk.IntVar(value=0),
            "ot_emo1emv": tk.IntVar(value=0),
            "ot_emo2": tk.IntVar(value=0),
            #"lovn_otkl": tk.IntVar(value=0),
            #"urov_nasebya": tk.IntVar(value=0),
            "avar_isol_V": tk.IntVar(value=0),
            "niz_isol_V": tk.IntVar(value=0),
            "pruzh_ne_zaved": tk.IntVar(value=0),
            "Sbros": tk.IntVar(value=0),
            "otkl_ot_knopk": tk.IntVar(value=0),
            "oper_otkl_V": tk.IntVar(value=0),
            "KRV_resurs_V": tk.IntVar(value=0),
            "vnesh_blok_upr_V": tk.IntVar(value=0),
            "kontr_emv": tk.IntVar(value=0),
            "kontr_emo1": tk.IntVar(value=0),
            "kontr_emo2": tk.IntVar(value=0),
            "rabota_emv": tk.IntVar(value=0),
            "rabota_emo1": tk.IntVar(value=0),
            "rabota_emo2": tk.IntVar(value=0),
            "OV_swctrl": tk.IntVar(value=0),
            "otkl_v_ot_pu": tk.IntVar(value=0),
            "otkl_v_ichm": tk.IntVar(value=0),
            "mestnoe": tk.IntVar(value=0),
            "otkl_v_ot_tu": tk.IntVar(value=0),
            "otkl_v_asu": tk.IntVar(value=0),
            "kluch_md_priv": tk.IntVar(value=0),
            "vkl_v_ot_pu": tk.IntVar(value=0),
            "vkl_v_ichm": tk.IntVar(value=0),
            "distanz": tk.IntVar(value=0),
            "vkl_v_ot_tu": tk.IntVar(value=0),
            "vkl_v_asu": tk.IntVar(value=0),
            "v_otkl_bk": tk.IntVar(value=0),
            "v_vkl_bk": tk.IntVar(value=0),
            "OV_cbcswi1_hvbctrl": tk.IntVar(value=0),
            "oper_vkl_v": tk.IntVar(value=0),
            "OV_tsd": tk.IntVar(value=0),
            #"lovn_lo_otkl_avar": tk.IntVar(value=0),
            #"oper_otkl_v": tk.IntVar(value=0),
            #"sbros": tk.IntVar(value=0),
            "pusk_urov_vnesh": tk.IntVar(value=0),
            "vnesh_otkl_zdz1": tk.IntVar(value=0),
            "vnesh_otkl_urov1": tk.IntVar(value=0),
            "vnesh_otkl_zdz2": tk.IntVar(value=0),
            "vnesh_otkl_urov2": tk.IntVar(value=0),            
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
            "vvod_rcbf1_lvcbsup", "oper_vyvod_rcbf1_lvcbsup", "v_samoproisv_otkl_rcbf1_lvcbsup", "neispr_V_rcbf1_lvcbsup",
            "v_avar_otkl_rcbf1_lvcbsup", "rfk_rcbf1_lvcbsup", "blok_vkl_rcbf1_lvcbsup", "blok_otkl_rcbf1_lvcbsup",
            "neisp_emu_rcbf1_lvcbsup", "zashita_emv_rcbf1_lvcbsup", "zashita_emo1_rcbf1_lvcbsup", "zashita_emo2_rcbf1_lvcbsup",
            "vvod_swctrl", "oper_vyvod_swctrl", "vvod_cbcswi1_swctrl", "uv_otkluchit_cbcswi1_swctrl", "uv_idet_per_cbcswi1_swctrl",
            "uv_prev_vrem_per_cbcswi1_swctrl", "uv_vkluchit_cbcswi1_swctrl", "uv_ne_opredeleno_cbcswi1_swctrl",
            "uv_otklucheno_cbcswi1_swctrl", "uv_vklucheno_cbcswi1_swctrl", "uv_neispr_neopred_cbcswi1_swctrl",
            "vvod_cbcswi1_hvbctrl", "oper_vyvod_cbcswi1_hvbctrl", "uv_vkl_cbcswi1_hvbctrl",
            "vvod_tsd", "oper_vyvod_tsd", "vvod_xcbr1_tsd", "v_prom_pol_xcbr1_tsd", "v_otkluchen_xcbr1_tsd",
            "v_vkluchen_xcbr1_tsd", "v_neisp_pol_xcbr1_tsd", "v_otkluchit_rele_xcbr1_tsd", "v_vkluchit_rele_xcbr1_tsd", "ss_prev_vrem_per_ka", "pusk_t_lvalh",
            "srab_na_sebya_rbrf1_tpbrf",
            "vvod_hvcbptrc1_hvtcboff", "otkl_hvcbptrc1_hvtcboff", "otkl_avar_hvcbptrc1_hvtcboff"
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
        self.part = SWITCH(
            SGF1_rcbf1_lvcbsup=self.sgf_params["SGF1_rcbf1_lvcbsup"].get(),
            SGF2_rcbf1_lvcbsup=self.sgf_params["SGF2_rcbf1_lvcbsup"].get(),
            SGF3_rcbf1_lvcbsup=self.sgf_params["SGF3_rcbf1_lvcbsup"].get(),
            SGF4_rcbf1_lvcbsup=self.sgf_params["SGF4_rcbf1_lvcbsup"].get(),
            SGF5_rcbf1_lvcbsup=self.sgf_params["SGF5_rcbf1_lvcbsup"].get(),
            SGF6_rcbf1_lvcbsup=self.sgf_params["SGF6_rcbf1_lvcbsup"].get(),
            SGF7_rcbf1_lvcbsup=self.sgf_params["SGF7_rcbf1_lvcbsup"].get(),
            SGF8_rcbf1_lvcbsup=self.sgf_params["SGF8_rcbf1_lvcbsup"].get(),
            T1_rcbf1_lvcbsup=self.settings["T1_rcbf1_lvcbsup"].get(),
            T2_rcbf1_lvcbsup=self.settings["T2_rcbf1_lvcbsup"].get(),
            T3_rcbf1_lvcbsup=self.settings["T3_rcbf1_lvcbsup"].get(),
            SGF1_swctrl=self.sgf_params["SGF1_swctrl"].get(),
            SGF1_cbcswi1_swctrl=self.sgf_params["SGF1_cbcswi1_swctrl"].get(),
            SGF2_cbcswi1_swctrl=self.sgf_params["SGF2_cbcswi1_swctrl"].get(),
            T1_cbcswi1_swctrl=self.settings["T1_cbcswi1_swctrl"].get(),
            T2_cbcswi1_swctrl=self.settings["T2_cbcswi1_swctrl"].get(),
            T3_cbcswi1_swctrl=self.settings["T3_cbcswi1_swctrl"].get(),
            T4_cbcswi1_swctr=self.settings["T4_cbcswi1_swctrl"].get(),
            SGF1_cbcswi1_hvbctrl=self.sgf_params["SGF1_cbcswi1_hvbctrl"].get(),
            T1_cbcswi1_hvbctrl=self.settings["T1_cbcswi1_hvbctrl"].get(),
            SGF1_tsd=self.sgf_params["SGF1_tsd"].get(),
            SGF1_xcbr1_tsd=self.sgf_params["SGF1_xcbr1_tsd"].get(),
            SGF2_xcbr1_tsd=self.sgf_params["SGF2_xcbr1_tsd"].get(),
            SGF3_xcbr1_tsd=self.sgf_params["SGF3_xcbr1_tsd"].get(),
            SGF4_xcbr1_tsd=self.sgf_params["SGF4_xcbr1_tsd"].get(),
            SGF5_xcbr1_tsd=self.sgf_params["SGF5_xcbr1_tsd"].get(),
            SGF6_xcbr1_tsd=self.sgf_params["SGF6_xcbr1_tsd"].get(),
            T1_xcbr1_tsd=self.settings["T1_xcbr1_tsd"].get(),
            T2_xcbr1_tsd=self.settings["T2_xcbr1_tsd"].get(),
            T3_xcbr1_tsd=self.settings["T3_xcbr1_tsd"].get(),
            T4_xcbr1_tsd=self.settings["T4_xcbr1_tsd"].get(),
            SGF9_t_lvalh=self.sgf_params["SGF9_lvalh"].get(),
            SGF1_rbrf1_tpbrf=self.sgf_params["SGF1_rbrf1_tpbrf"].get(),
            SGF2_rbrf1_tpbrf=self.sgf_params["SGF2_rbrf1_tpbrf"].get(),
            SGF3_rbrf1_tpbrf=self.sgf_params["SGF3_rbrf1_tpbrf"].get(),
            SGF4_rbrf1_tpbrf=self.sgf_params["SGF4_rbrf1_tpbrf"].get(),
            SGF5_rbrf1_tpbrf=self.sgf_params["SGF5_rbrf1_tpbrf"].get(),
            SGF6_rbrf1_tpbrf=self.sgf_params["SGF6_rbrf1_tpbrf"].get(),
            T1_rbrf1_tpbrf=self.settings["T1_rbrf1_tpbrf"].get(),
            Iset_rbrf1_tpbrf=self.settings["Iset_rbrf1_tpbrf"].get(),
            SGF1_hvcbptrc1_hvtcboff=self.sgf_params["SGF1_hvcbptrc1_hvtcboff"].get(),
            T1_hvcbptrc1_hvtcboff=self.settings["T1_hvcbptrc1_hvtcboff"].get(),
        )
        print("part_SWITCH initialized")

    def start_polling(self):
        if self.part is None:
            print("part_SWITCH not initialized")
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
                #if isinstance(label, tuple):
                #print(f"{output}: {value}")
                label.config(text=f"{output}: {round(value, 2)}")

                if int(value) != 0:
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

            settings_df = pd.read_excel(xls, sheet_name="Settings")
            for key, var in self.settings.items():
                if key in settings_df.columns:
                    var.set(settings_df.at[0, key])

            inputs_df = pd.read_excel(xls, sheet_name="Inputs")
            for key, var in self.input_vars.items():
                if key in inputs_df.columns:
                    var.set(inputs_df.at[0, key])

            print("Data loaded successfully")
        except Exception as e:
            print(f"Error loading data: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PartOfSwitchGUI(root)
    root.mainloop()