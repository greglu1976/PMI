########################
### Версия для 2026 года (М300-Т2) - Исправленная работа с потоками
########################
# 
#######################

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
import threading
import time
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
import openpyxl
import json
import sys

# Проверка импортов
try:
    from lib2.PARTS.TECH_T2 import part_TECH_T2 
    from MainConfigHandler import MainConfigHandler
    from SettingsHandler import SettingsHandler
    from ToolTip import ToolTip
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    # sys.exit(1) # Раскомментируйте, если нужно прерывать выполнение

# --- Основной GUI ---
class PartOfTECH_T_GUI:

    # === СПИСОК ВЫХОДНЫХ ПАРАМЕТРОВ (единое определение) ===
    OUTPUT_PARAMS = [
            "TALMGASLGC_1_PTRC1_FuncEnabled", "TALMGASLGC_1_PTRC1_FuncOperDisabled", "TALMGASLGC_1_PTRC1_Op", "TALMGASLGC_1_PTRC1_OpOnSignal", "TALMGASLGC_1_PTRC1_BlockGASProtSign", "ET_ptrc1_talmgaslgc",
            "TTRGASLGC_1_PTRC1_FuncEnabled", "TTRGASLGC_1_PTRC1_FuncOperDisabled", "TTRGASLGC_1_PTRC1_Op", "TTRGASLGC_1_PTRC1_OpOnSignal",
            "TTRGASLGC_1_PTRC1_BlockGASProtTrip", "ET_ptrc1_ttrgaslgc", "TLTCGASLGC_1_PTRC1_FuncEnabled", "TLTCGASLGC_1_PTRC1_FuncOperDisabled",
            "TLTCGASLGC_1_PTRC1_Op", "TLTCGASLGC_1_PTRC1_OpOnSignal", "TLTCGASLGC_1_PTRC1_BlockGASLTCProt", "ET_ptrc1_tltcgaslgc",
            "TRESOFFLVLGC_1_PTRC1_FuncEnabled", "TRESOFFLVLGC_1_PTRC1_FuncOperDisabled", "pusk_ptrc1_tofflvlgc", "TRESOFFLVLGC_1_PTRC1_Op",
            "TRESOFFLVLGC_1_LVCBRBLC1_FuncEnabled", "TRESOFFLVLGC_1_LVCBRBLC1_FuncOperDisabled", "TRESOFFLVLGC_1_LVCBRBLC1_BlkOp",
            "TRESOFFLVLGC_1_RBRE1_FuncEnabled", "TRESOFFLVLGC_1_RBRE1_FuncOperDisabled", "TRESOFFLVLGC_1_RBRE1_BlkOp",
            "T2_SignAssembly_1_GASSign", "T2_SignAssembly_1_GASBlock", "T2_SignAssembly_1_LowIsolGAS", 
            "T2_SignAssembly_1_OpExt", "T2_SignAssembly_1_CtlCir", "T2_SignAssembly_1_TestBlock", "T2_SignAssembly_1_OCSign",
            "T2_SignAssembly_1_GAS_OCControlSignAssem", "T2_SignAssembly_1_OCcir_CBSignAssem", "T2_SignAssembly_1_OCnnSign", "T2_SignAssembly_1_SwOperExcTim", "T2_SignAssembly_1_ExtSignGen", "T2_LVALH_1_CALH1_Alarm"
        ]

    def __init__(self, root):
        self.root = root
        self.root.title("Тестирование Газовых и Технологических Защит М300-Т2. вер1 от 2026")
        self.part = None
        self.polling_thread = None
        self.is_polling = False

        self.function_name = tk.StringVar(value="Функция")
        self.mode_name = tk.StringVar(value="Режим")

        # === ЗАГРУЗКА МЕТАДАННЫХ ===
        try:
            self.meta_handler = MainConfigHandler.from_json_file("meta.json")
        except Exception as e:
            print(f"⚠️ Не удалось загрузить meta.json: {e}")
            self.meta_handler = None

        # === ИНИЦИАЛИЗАЦИЯ СЛОВАРЕЙ ПЕРЕМЕННЫХ ===
        
        # SGF-параметры
        sgf_keys = self._get_sgf_param_names()
        self.sgf_params = {name: tk.IntVar(value=0) for name in sgf_keys}
        
        # Настройки (T-параметры)
        setting_keys = self._get_setting_names()
        self.settings = {name: tk.DoubleVar(value=1.0) for name in setting_keys}
        
        # Входные параметры
        input_keys = self._get_input_names()
        self.input_vars = {name: tk.IntVar(value=0) for name in input_keys}

        # Выходные метки
        self.output_labels = {}

        # === ГЕНЕРАЦИЯ ПОДСКАЗОК ИЗ JSON ===
        self.tooltips = {}
        all_param_keys = sgf_keys + setting_keys + input_keys + list(self.OUTPUT_PARAMS)
        
        if self.meta_handler:
            for key in all_param_keys:
                desc = self.meta_handler.get_description_by_base_name(key)
                if desc:
                    self.tooltips[key] = desc

        # === СОЗДАНИЕ ИНТЕРФЕЙСА ===
        self.create_widgets()

    def _get_sgf_param_names(self):
        return [
            "TALMGASLGC_1_PTRC1_EnaDis",
            "TALMGASLGC_1_PTRC1_LowIsolSignCtrl",
            "TTRGASLGC_1_PTRC1_EnaDis",
            "TTRGASLGC_1_PTRC1_LowIsolTripCtrl",
            "TLTCGASLGC_1_PTRC1_EnaDis",
            "TLTCGASLGC_1_PTRC1_LowIsolTripCtrl",
            "TRESOFFLVLGC_1_PTRC1_EnaDis",
            "TRESOFFLVLGC_1_RBRE1_EnaDis",
            "TRESOFFLVLGC_1_RBRE1_PVOC2_Ctrl",
            "TRESOFFLVLGC_1_RBRE1_PVOC3_Ctrl",
            "TRESOFFLVLGC_1_LVCBRBLC1_EnaDis",
            "TRESOFFLVLGC_1_LVCBRBLC1_PVOC2_Ctrl",
            "TRESOFFLVLGC_1_LVCBRBLC1_PVOC3_Ctrl",
            "T2_LVALH_1_CALH1_GASSign_Ctl",
            "T2_LVALH_1_CALH1_LowIsolGAS_Ctl",
            "T2_LVALH_1_CALH1_GASBlock_Ctl",
            "T2_LVALH_1_CALH1_OCSign_Ctl",
            "T2_LVALH_1_CALH1_OCnnSign_Ctl",
            "T2_LVALH_1_CALH1_OpExt_Ctl",
            "T2_LVALH_1_CALH1_CtlCir_Ctl",
            "T2_LVALH_1_CALH1_TestBlock_Ctl",
            "T2_LVALH_1_CALH1_SwOperExcTim_Ctl",
            "T2_LVALH_1_CALH1_ExtSignGen_Ctl",
            "T2_SignAssembly_1_Ctl_SA1",
            "T2_SignAssembly_1_Ctl_SA2",
            "T2_SignAssembly_1_Ctl_SA3",
            "T2_SignAssembly_1_Ctl_SA4",
            "T2_SignAssembly_1_Ctl_SA5",
            "T2_SignAssembly_1_Ctl_SA6",
            "T2_SignAssembly_1_Ctl_SG1",
            "T2_SignAssembly_1_Ctl_SG2",
            "T2_SignAssembly_1_Ctl_SG3",
            "T2_SignAssembly_1_Ctl_GAS_OCControl",
            "T2_SignAssembly_1_Ctl_OCcir_CB",
            "T2_SignAssembly_1_Ctl_ARCnn1_OCControl",
            "T2_SignAssembly_1_Ctl_ARCnn2_OCControl",
            "T2_SignAssembly_1_Ctl_CBFPnn1_OCControl",
            "T2_SignAssembly_1_Ctl_CBFPnn2_OCControl",
            "T2_SignAssembly_1_Ctl_IEDvt_OCControl1",
            "T2_SignAssembly_1_Ctl_IEDvt_OCControl2",
        ]

    def _get_setting_names(self):
        return [
            "TALMGASLGC_1_PTRC1_TopOnBlk",
            "TTRGASLGC_1_LLN0_TopOnBlk",
            "TLTCGASLGC_1_LLN0_TopOnBlk",
        ]


    def _get_input_names(self):
        return [
            "DI_ControllerDisable",
            "Reset",
            "DI_TALMGASLGC",
            "DI_TALMGASLGC_Sign",
            "TALMGASLGC_1_SignContact",
            "GASSignIsolOp",
            "DI_TTRGASLGC",
            "DI_TTRGASLGC_Sign",
            "TTRGASLGC_1_TripContact",
            "GASTripIsolOp",
            "DI_TLTCGASLGC",
            "DI_TLTCGASLGC_Sign",
            "JetRelayContact",
            "GASLTCIsolOp",
            "DI_TRESOFFLVLGS",
            "DI_PTRC1",
            "DI_RBRE1",
            "DI_LVCBRBLC1",
        ]

    def create_widgets(self):
        # SGF Parameters
        sgf_frame = ttk.LabelFrame(self.root, text="SGF Parameters")
        sgf_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        row, col = 0, 0
        for key in self._get_sgf_param_names():
            var = self.sgf_params[key]
            label = ttk.Label(sgf_frame, text=key)
            label.grid(row=row, column=col, sticky="w")
            tooltip = self.tooltips.get(key)
            if tooltip:
                ToolTip(label, tooltip)
            ttk.Combobox(sgf_frame, textvariable=var, values=[0, 1], state="readonly", width=5).grid(row=row, column=col + 1)
            row += 1
            if row >= 14:
                row = 0
                col += 2

        # Settings (T-parameters)
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        row, col = 0, 0
        for key in self._get_setting_names():
            var = self.settings[key]
            label = ttk.Label(settings_frame, text=key)
            label.grid(row=row, column=col, sticky="w")
            tooltip = self.tooltips.get(key)
            if tooltip:
                ToolTip(label, tooltip)
            ttk.Entry(settings_frame, textvariable=var, width=10).grid(row=row, column=col + 1)
            row += 1
            if row >= 3:
                row = 0
                col += 2

        # Buttons
        buttons_frame = ttk.LabelFrame(self.root, text="Buttons")
        buttons_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(buttons_frame, text="Init", command=self.init_part).grid(row=0, column=0, pady=10)
        ttk.Button(buttons_frame, text="Start", command=self.start_polling).grid(row=0, column=1, pady=10)
        ttk.Button(buttons_frame, text="Stop", command=self.stop_polling).grid(row=0, column=2, pady=10)
        ttk.Button(buttons_frame, text="Save", command=self.save_to_excel).grid(row=0, column=3, pady=10)
        ttk.Button(buttons_frame, text="Load", command=self.load_from_excel).grid(row=0, column=4, pady=10)

        ttk.Button(buttons_frame, text="Load JSON", command=self.load_settings_from_json).grid(row=0, column=5, padx=2, pady=5)
        ttk.Button(buttons_frame, text="Save JSON", command=self.save_settings_to_json).grid(row=0, column=6, padx=2, pady=5)

        ttk.Label(buttons_frame, text="Функция:").grid(row=0, column=7, padx=5, pady=5)
        ttk.Entry(buttons_frame, textvariable=self.function_name, width=15).grid(row=0, column=8, padx=5, pady=5)
        ttk.Label(buttons_frame, text="Режим:").grid(row=0, column=9, padx=5, pady=5)
        ttk.Entry(buttons_frame, textvariable=self.mode_name, width=15).grid(row=0, column=10, padx=5, pady=5)

        # Статус бар
        self.status_label = ttk.Label(buttons_frame, text="Шаг", background="green", foreground="white")
        self.status_label.grid(row=0, column=11, padx=5, pady=5)

        # Input Parameters
        input_frame = ttk.LabelFrame(self.root, text="Входные параметры")
        input_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        row, col = 0, 0
        for key in self._get_input_names():
            var = self.input_vars[key]
            cb = ttk.Checkbutton(input_frame, text=key, variable=var)
            cb.grid(row=row, column=col, sticky="w")
            tooltip = self.tooltips.get(key)
            if tooltip:
                ToolTip(cb, tooltip)
            row += 1
            if row >= 6:
                row = 0
                col += 2

        # Output Parameters
        output_frame = ttk.LabelFrame(self.root, text="Выходные параметры")
        output_frame.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")

        row, col = 0, 0
        for output in self.OUTPUT_PARAMS:
            label = ttk.Label(output_frame, text=output, width=33, anchor="w")
            label.grid(row=row, column=col, sticky="w")
            self.output_labels[output] = label

            tooltip = self.tooltips.get(output)
            if tooltip:
                ToolTip(label, tooltip)

            row += 1
            if row >= 32:
                row = 0
                col += 2

    def init_part(self):
        try:
            self.part = part_TECH_T2(
           # Передаем SGF-параметры из self.sgf_params
            SGF1_ptrc1_talmgaslgc=self.sgf_params["TALMGASLGC_1_PTRC1_EnaDis"].get(),
            SGF2_ptrc1_talmgaslgc=self.sgf_params["TALMGASLGC_1_PTRC1_LowIsolSignCtrl"].get(),
            T1_ptrc1_talmgaslgc=self.settings["TALMGASLGC_1_PTRC1_TopOnBlk"].get()/1000,
            SGF1_ptrc1_ttrgaslgc=self.sgf_params["TTRGASLGC_1_PTRC1_EnaDis"].get(),
            SGF2_ptrc1_ttrgaslgc=self.sgf_params["TTRGASLGC_1_PTRC1_LowIsolTripCtrl"].get(),
            T1_ptrc1_ttrgaslgc=self.settings["TTRGASLGC_1_LLN0_TopOnBlk"].get()/1000,
            SGF1_ptrc1_tltcgaslgc=self.sgf_params["TLTCGASLGC_1_PTRC1_EnaDis"].get(),
            SGF2_ptrc1_tltcgaslgc=self.sgf_params["TLTCGASLGC_1_PTRC1_LowIsolTripCtrl"].get(),
            T1_ptrc1_tltcgaslgc=self.settings["TLTCGASLGC_1_LLN0_TopOnBlk"].get()/1000,
            SGF1_ptrc1_tofflvlgc=self.sgf_params["TRESOFFLVLGC_1_PTRC1_EnaDis"].get(),
            SGF1_rbre1_tofflvlgc=self.sgf_params["TRESOFFLVLGC_1_RBRE1_EnaDis"].get(),
            SGF2_rbre1_tofflvlgc=self.sgf_params["TRESOFFLVLGC_1_RBRE1_PVOC2_Ctrl"].get(),
            SGF3_rbre1_tofflvlgc=self.sgf_params["TRESOFFLVLGC_1_RBRE1_PVOC3_Ctrl"].get(),
            SGF1_rblc1_tofflvlgc=self.sgf_params["TRESOFFLVLGC_1_LVCBRBLC1_EnaDis"].get(),
            SGF2_rblc1_tofflvlgc=self.sgf_params["TRESOFFLVLGC_1_LVCBRBLC1_PVOC2_Ctrl"].get(),
            SGF3_rblc1_tofflvlgc=self.sgf_params["TRESOFFLVLGC_1_LVCBRBLC1_PVOC3_Ctrl"].get(),
            SGF1_t_lvalh=self.sgf_params["T2_LVALH_1_CALH1_GASSign_Ctl"].get(),
            SGF2_t_lvalh=self.sgf_params["T2_LVALH_1_CALH1_LowIsolGAS_Ctl"].get(),
            SGF3_t_lvalh=self.sgf_params["T2_LVALH_1_CALH1_GASBlock_Ctl"].get(),
            SGF4_t_lvalh=self.sgf_params["T2_LVALH_1_CALH1_OCSign_Ctl"].get(),
            SGF5_t_lvalh=self.sgf_params["T2_LVALH_1_CALH1_OCnnSign_Ctl"].get(),
            SGF6_t_lvalh=self.sgf_params["T2_LVALH_1_CALH1_OpExt_Ctl"].get(),
            SGF7_t_lvalh=self.sgf_params["T2_LVALH_1_CALH1_CtlCir_Ctl"].get(),
            SGF8_t_lvalh=self.sgf_params["T2_LVALH_1_CALH1_TestBlock_Ctl"].get(),
            SGF9_t_lvalh=self.sgf_params["T2_LVALH_1_CALH1_SwOperExcTim_Ctl"].get(),
            SGF10_t_lvalh=self.sgf_params["T2_LVALH_1_CALH1_ExtSignGen_Ctl"].get(),
            SGF1_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_SA1"].get(),
            SGF2_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_SA2"].get(),
            SGF3_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_SA3"].get(),
            SGF4_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_SA4"].get(),
            SGF5_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_SA5"].get(),
            SGF6_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_SA6"].get(),
            SGF7_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_SG1"].get(),
            SGF8_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_SG2"].get(),
            SGF9_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_SG3"].get(),
            SGF10_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_GAS_OCControl"].get(),
            SGF11_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_OCcir_CB"].get(),
            SGF12_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_ARCnn1_OCControl"].get(),
            SGF13_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_ARCnn2_OCControl"].get(),
            SGF14_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_CBFPnn1_OCControl"].get(),
            SGF15_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_CBFPnn2_OCControl"].get(),
            SGF16_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_IEDvt_OCControl1"].get(),
            SGF17_t_signassembly=self.sgf_params["T2_SignAssembly_1_Ctl_IEDvt_OCControl2"].get(),  
            )
            print("part_TECH_T2 initialized")
           # messagebox.showinfo("Успех", "Модель инициализирована")
        except Exception as e:
            messagebox.showerror("Ошибка инициализации", str(e))
            print(f"Error initializing part: {e}")

    def start_polling(self):
        if not self.part:
            messagebox.showwarning("Внимание", "Сначала нажмите Init")
            return
        if self.is_polling:
            return
        self.is_polling = True
        self.polling_thread = threading.Thread(target=self.poll_inputs, daemon=True)
        self.polling_thread.start()
        print("Polling started")

    def stop_polling(self):
        self.is_polling = False
        if self.polling_thread and self.polling_thread.is_alive():
            self.polling_thread.join(timeout=2.0)
        print("Polling stopped")

    def poll_inputs(self):
        while self.is_polling:
            inputs = {key: var.get() for key, var in self.input_vars.items()}
            result = self.part.Step(**inputs)
            for output, value in zip(self.output_labels.keys(), result):
                label = self.output_labels[output]
                label.config(text=f"{output}: {round(value, 2)}")
                bg_color = "red" if int(value) != 0 else "green"
                label.config(background=bg_color, foreground="white")
            time.sleep(0.3)
            self.status_label.config(text="Шаг", background="white", foreground="black")
            time.sleep(0.05)
            self.status_label.config(text="Шаг", background="#F0F0F0", foreground="black")
    def _handle_thread_error(self, msg):
        """Обработчик ошибок из потока, выполняется в главном потоке"""
        messagebox.showerror("Ошибка потока", msg)

    def _update_gui_outputs(self, result):
        """Выполняется в главном потоке. Обновляет виджеты."""
        if not self.is_polling:
            return

        try:
            for output, value in zip(self.output_labels.keys(), result):
                label = self.output_labels[output]
                text_val = f"{output}: {round(value, 2)}"
                label.config(text=text_val)
                
                if int(value) != 0:
                    label.config(background="red", foreground="white")
                else:
                    label.config(background="green", foreground="white")
            
            # Мигание статуса
            self.status_label.config(text="Шаг", background="#D0D0D0", foreground="black")
            self.root.after(50, lambda: self.status_label.config(text="Шаг", background="#F0F0F0", foreground="black"))
            
        except Exception as e:
            print(f"GUI Update Error: {e}")

    def save_to_excel(self):
        function = self.function_name.get().strip()
        mode = self.mode_name.get().strip()
        if not function or not mode:
            messagebox.showwarning("Внимание", "Поля 'Функция' и 'Режим' должны быть заполнены")
            return
        output_file = f"{function}_{mode}.xlsx"

        try:
            sgf_df = pd.DataFrame({key: [var.get()] for key, var in self.sgf_params.items()})
            settings_df = pd.DataFrame({key: [var.get()] for key, var in self.settings.items()})
            inputs_df = pd.DataFrame({key: [var.get()] for key, var in self.input_vars.items()})
            
            outputs_data = {}
            for key, label in self.output_labels.items():
                try:
                    val_str = label.cget("text").split(": ")[-1]
                    outputs_data[key] = [float(val_str)]
                except:
                    outputs_data[key] = [0.0]
            outputs_df = pd.DataFrame(outputs_data)

            with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
                sgf_df.to_excel(writer, sheet_name="SGF_Parameters", index=False)
                settings_df.to_excel(writer, sheet_name="Settings", index=False)
                inputs_df.to_excel(writer, sheet_name="Inputs", index=False)
                outputs_df.to_excel(writer, sheet_name="Outputs", index=False)

            wb = openpyxl.load_workbook(output_file)
            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            def format_sheet(sheet):
                for col_num, column in enumerate(sheet.columns, start=1):
                    sheet.column_dimensions[openpyxl.utils.get_column_letter(col_num)].width = 25
                    for row_num, cell in enumerate(column, start=1):
                        if row_num == 1: continue
                        try:
                            if float(cell.value) != 0:
                                cell.fill = red_fill
                        except (ValueError, TypeError):
                            pass

            for sheet_name in wb.sheetnames:
                format_sheet(wb[sheet_name])

            wb.save(output_file)
            print(f"Данные сохранены в {output_file}")
            #messagebox.showinfo("Успех", f"Данные сохранены в {output_file}")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))

    def load_from_excel(self):
        file_path = askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return
        try:
            xls = pd.ExcelFile(file_path)
            
            mapping = [
                ("SGF_Parameters", self.sgf_params),
                ("Settings", self.settings),
                ("Inputs", self.input_vars)
            ]

            for sheet_name, var_dict in mapping:
                if sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    for key, var in var_dict.items():
                        if key in df.columns:
                            val = df.at[0, key]
                            if isinstance(var, tk.IntVar):
                                var.set(int(val) if pd.notna(val) else 0)
                            elif isinstance(var, tk.DoubleVar):
                                var.set(float(val) if pd.notna(val) else 0.0)
            
            messagebox.showinfo("Успех", "Данные загружены из Excel")
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", str(e))

    def load_settings_from_json(self):
        """Загружает SGF и T-параметры из JSON-файла, добавляя '_SG1' к именам."""
        file_path = askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        try:
            handler = SettingsHandler.from_json_file(file_path)
            
            for key in self.sgf_params:
                json_key = key + "_SG1"
                value_str = handler.get_value_by_parameter(json_key)
                if value_str is None:
                    continue
                    
                try:
                    type_str = None
                    if self.meta_handler:
                        param_info = self.meta_handler.get_param_info(json_key)
                        if param_info:
                            type_str = param_info.get("type")
                    
                    if type_str == "3": 
                        value_lower = str(value_str).lower().strip()
                        bool_map = {
                            "true": 1, "1": 1, "on": 1, "вкл": 1, "да": 1, "yes": 1, "enabled": 1,
                            "false": 0, "0": 0, "off": 0, "выкл": 0, "нет": 0, "no": 0, "disabled": 0
                        }
                        self.sgf_params[key].set(bool_map.get(value_lower, 0))
                    else: 
                        value_clean = str(value_str).replace(',', '.').strip()
                        for suffix in ['%', '°', 'мс', 'с', 'м']:
                            if value_clean.endswith(suffix):
                                value_clean = value_clean[:-len(suffix)].strip()
                        self.sgf_params[key].set(int(float(value_clean)))
                            
                except Exception as e:
                    print(f"Ошибка SGF {json_key}: {e}")

            for key in self.settings:
                json_key = key + "_SG1"
                value_str = handler.get_value_by_parameter(json_key)
                if value_str is None:
                    continue
                try:
                    value_clean = str(value_str).replace(',', '.').strip()
                    for unit in ['%', '°', 'мс', 'с', 'м']:
                        if value_clean.lower().endswith(unit):
                            value_clean = value_clean[:-len(unit)].strip()
                    self.settings[key].set(float(value_clean))
                except Exception as e:
                    print(f"Ошибка Setting {json_key}: {e}")

            messagebox.showinfo("Успех", "Уставки успешно загружены из JSON-файла.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить уставки:\n{str(e)}")

    def save_settings_to_json(self):
        """Сохраняет SGF и T-параметры в JSON-файл с суффиксом _SG1."""
        file_path = askopenfilename(
            title="Сохранить уставки как...",
            filetypes=[("JSON files", "*.json")],
            defaultextension=".json"
        )
        if not file_path:
            return
        try:
            try:
                handler = SettingsHandler.from_json_file(file_path)
            except:
                handler = SettingsHandler([]) 
            
            for base_key in self.sgf_params:
                json_key = base_key + "_SG1"
                raw_value = self.sgf_params[base_key].get()
                
                param_type = "3" 
                if self.meta_handler:
                    param_info = self.meta_handler.get_param_info(json_key)
                    if param_info and "type" in param_info:
                        param_type = str(param_info["type"])

                if param_type == "3":
                    formatted = "1" if raw_value != 0 else "0"
                else:
                    formatted = str(int(raw_value))

                handler.add_or_update_parameter(json_key, formatted)
            
            for base_key in self.settings:
                json_key = base_key + "_SG1"
                raw_value = self.settings[base_key].get()
                formatted = f"{float(raw_value):.6g}"
                handler.add_or_update_parameter(json_key, formatted)
            
            handler.save_to_json_file(file_path)
            messagebox.showinfo("Успех", f"Уставки сохранены в:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении:\n{str(e)}")

    def _get_output_names(self):
        return self.OUTPUT_PARAMS    


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('vista') 
    
    app = PartOfTECH_T_GUI(root)
    root.mainloop()