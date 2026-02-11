import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
import threading
import time
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.dimensions import ColumnDimension
import openpyxl
import json
# Импортируем класс partTOKZ
from lib2.PARTS.TOKZ import partTOKZ
from MainConfigHandler import MainConfigHandler
from SettingsHandler import SettingsHandler
from ToolTip import ToolTip

class PartOfTOKGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Тестирование токовых функций ФСУ, v3.0 от 2026 разработка")
        self.part = None
        self.polling_thread = None
        self.is_polling = False
        
        # Инициализация переменных для имени файла
        self.function_name = tk.StringVar(value="Функция")
        self.mode_name = tk.StringVar(value="Режим")
        
        # === ЗАГРУЗКА МЕТАДАННЫХ ===
        try:
            self.meta_handler = MainConfigHandler.from_json_file("meta.json")
        except Exception as e:
            print(f"⚠️ Не удалось загрузить meta.json: {e}")
            self.meta_handler = None


        # Инициализация переменных для параметров SGF и настроек
        self.sgf_params = {
            "T_LVTOC_1_PTOC1_EnaDis": tk.IntVar(value=0),
            "T_LVTOC_1_PTOC1_KschemeCT": tk.IntVar(value=0),
            "T_AUTOVC_1_OVCPTOC1_EnaDis": tk.IntVar(value=0),
            "T_LVARCTOC_1_PTOC1_EnaDis": tk.IntVar(value=0),
            "T_LVARCTOC_1_PTOC1_StrMod": tk.IntVar(value=0),
            "LTCBLKTOC_1_PTOC1_EnaDis": tk.IntVar(value=0), 
            "LVNSTOC_1_NSPTOC1_EnaDis": tk.IntVar(value=0),
            "LVNSTOC_1_NSPTOC1_AssymCtrlMod": tk.IntVar(value=0),
            "TTOCLGC_UIRZ_1_PTRC1_EnaDis": tk.IntVar(value=0),
            "TTOCLGC_UIRZ_1_PTRC1_LVTPTOC2_Ctrl": tk.IntVar(value=0),
            "TTOCLGC_UIRZ_1_PTRC1_LVTPTOC3_Ctrl": tk.IntVar(value=0),
            "TOFFLVLGC_1_PTRC1_EnaDis": tk.IntVar(value=0),
            "TOFFLVLGC_1_RBRE1_EnaDis": tk.IntVar(value=0),
            "TOFFLVLGC_1_RBRE1_PVOC2_Ctrl": tk.IntVar(value=0),
            "TOFFLVLGC_1_RBRE1_PVOC3_Ctrl": tk.IntVar(value=0),
            "TOFFLVLGC_1_LVCBRBLC1_EnaDis": tk.IntVar(value=0),
            "TOFFLVLGC_1_LVCBRBLC1_PVOC2_Ctrl": tk.IntVar(value=0),
            "TOFFLVLGC_1_LVCBRBLC1_PVOC3_Ctrl": tk.IntVar(value=0),
            "Номинальный ток входа": tk.IntVar(value=5),           
        }
        self.settings = {
            "T_LVTOC_1_PTOC1_Top": tk.DoubleVar(value=1),
            "T_LVTOC_1_PTOC1_Iop": tk.DoubleVar(value=0.2),
            "T_AUTOVC_1_OVCPTOC1_Top": tk.DoubleVar(value=1),
            "T_AUTOVC_1_OVCPTOC1_Iop": tk.DoubleVar(value=0.2),
            "T_LVARCTOC_1_PTOC1_Iop": tk.DoubleVar(value=0.2),
            "LTCBLKTOC_1_PTOC1_Iop": tk.DoubleVar(value=0.2),
            "LVNSTOC_1_NSPTOC1_Top": tk.DoubleVar(value=1),  # Исправлено: было "LVNSTOC_1_NSPTOC1_To"
            "LVNSTOC_1_NSPTOC1_I2op": tk.DoubleVar(value=0.2),
            "LVNSTOC_1_NSPTOC1_Kasm": tk.DoubleVar(value=1),
            "TTOCLGC_UIRZ_1_PTRC1_Top": tk.DoubleVar(value=1),
        }
        self.input_vars = {
            "VYVOD": tk.IntVar(value=0),
            "IA": tk.DoubleVar(value=0),
            "dIA": tk.DoubleVar(value=0),
            "IB": tk.DoubleVar(value=0),
            "dIB": tk.DoubleVar(value=0),
            "IC": tk.DoubleVar(value=0),
            "dIC": tk.DoubleVar(value=0),                      
            "OV_ptoc1_lvtoc": tk.IntVar(value=0),
            "NaSign_ptoc1_lvtoc": tk.IntVar(value=0),
            "OV_hvptoc1_lovctoc": tk.IntVar(value=0),
            "NaOtkl_hvptoc1_lovctoc": tk.IntVar(value=0),
            "OV_ptoc1_lvarctoc": tk.IntVar(value=0),
            "mtz1_pusk": tk.IntVar(value=0),
            "mtz2_pusk": tk.IntVar(value=0),
            "mtz3_pusk": tk.IntVar(value=0),
            "OV_ptoc1_ltcblktoc": tk.IntVar(value=0),            
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




        # === ГЕНЕРАЦИЯ ПОДСКАЗОК ИЗ JSON ===
        self.tooltips = {}
        all_param_keys = (
            list(self._get_sgf_param_names()) +
            list(self._get_setting_names()) +
            list(self._get_input_names())
        )
        for key in all_param_keys:
            if self.meta_handler:
                desc = self.meta_handler.get_description_by_base_name(key)
                if desc:
                    self.tooltips[key] = desc
        

        
        # Создание интерфейса
        self.create_widgets()
    
    def _get_sgf_param_names(self):
        return list(self.sgf_params.keys())
    
    def _get_setting_names(self):
        return list(self.settings.keys())
    
    def _get_input_names(self):
        return list(self.input_vars.keys())
    
    def create_widgets(self):
        # Frame for SGF parameters
        sgf_frame = ttk.LabelFrame(self.root, text="SGF Parameters")
        sgf_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        row = 0
        col = 0
        for key, var in self.sgf_params.items():
            label = ttk.Label(sgf_frame, text=key)
            label.grid(row=row, column=col, sticky="w")
            
            # Добавляем tooltip
            tooltip = self.tooltips.get(key)
            if tooltip:
                ToolTip(label, tooltip)
            
            if key == 'Номинальный ток входа':
                ttk.Combobox(sgf_frame, textvariable=var, values=[1, 5], state="readonly").grid(row=row, column=col + 1)
            else:
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
            label = ttk.Label(settings_frame, text=key)
            label.grid(row=row, column=col, sticky="w")
            
            # Добавляем tooltip
            tooltip = self.tooltips.get(key)
            if tooltip:
                ToolTip(label, tooltip)
            
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
        # Button Load JSON
        ttk.Button(buttons_frame, text="Load JSON", command=self.load_settings_from_json).grid(row=0, column=5, padx=2, pady=5)
        # Button Save JSON
        ttk.Button(buttons_frame, text="Save JSON", command=self.save_settings_to_json).grid(row=0, column=6, padx=2, pady=5)
        
        # Поля для задания имени файла
        ttk.Label(buttons_frame, text="Функция:").grid(row=0, column=7, padx=5, pady=5)
        ttk.Entry(buttons_frame, textvariable=self.function_name, width=15).grid(row=0, column=8, padx=5, pady=5)
        ttk.Label(buttons_frame, text="Режим:").grid(row=0, column=9, padx=5, pady=5)
        ttk.Entry(buttons_frame, textvariable=self.mode_name, width=15).grid(row=0, column=10, padx=5, pady=5)
        
        # Добавляем новый элемент (например, Label) с возможностью изменения цвета
        self.status_label = ttk.Label(buttons_frame, text="Шаг", background="green", foreground="white")
        self.status_label.grid(row=0, column=11, padx=5, pady=5)
        
        # Frame for input values
        input_frame = ttk.LabelFrame(self.root, text="Inputs")
        input_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        row = 0
        col = 0
        for key, var in self.input_vars.items():
            if isinstance(var, tk.IntVar):
                cb = ttk.Checkbutton(input_frame, text=key, variable=var)
                cb.grid(row=row, column=col, sticky="w")
                
                # Добавляем tooltip
                tooltip = self.tooltips.get(key)
                if tooltip:
                    ToolTip(cb, tooltip)
            elif isinstance(var, tk.DoubleVar):
                label = ttk.Label(input_frame, text=key)
                label.grid(row=row, column=col, sticky="w")
                
                # Добавляем tooltip
                tooltip = self.tooltips.get(key)
                if tooltip:
                    ToolTip(label, tooltip)
                
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
            SGF1_ptoc1_lvtoc=self.sgf_params["T_LVTOC_1_PTOC1_EnaDis"].get(),
            SGF2_ptoc1_lvtoc=self.sgf_params["T_LVTOC_1_PTOC1_KschemeCT"].get(),
            T1_ptoc1_lvtoc=self.settings["T_LVTOC_1_PTOC1_Top"].get(),
            Iset_ptoc1_lvtoc=self.settings["T_LVTOC_1_PTOC1_Iop"].get(),
            SGF1_hvptoc1_lovctoc=self.sgf_params["T_AUTOVC_1_OVCPTOC1_EnaDis"].get(),
            T1_hvptoc1_lovctoc=self.settings["T_AUTOVC_1_OVCPTOC1_Top"].get(),
            Iset_hvptoc1_lovctoc=self.settings["T_AUTOVC_1_OVCPTOC1_Iop"].get(),
            SGF1_ptoc1_lvarctoc=self.sgf_params["T_LVARCTOC_1_PTOC1_EnaDis"].get(),
            SGF2_ptoc1_lvarctoc=self.sgf_params["T_LVARCTOC_1_PTOC1_StrMod"].get(),
            Iset_ptoc1_lvarctoc=self.settings["T_LVARCTOC_1_PTOC1_Iop"].get(),
            SGF1_ptoc1_ltcblktoc=self.sgf_params["LTCBLKTOC_1_PTOC1_EnaDis"].get(),
            Iset_ptoc1_ltcblktoc=self.settings["LTCBLKTOC_1_PTOC1_Iop"].get(),                        
            SGF1_nsptoc1_lvnstoc=self.sgf_params["LVNSTOC_1_NSPTOC1_EnaDis"].get(),
            SGF2_nsptoc1_lvnstoc=self.sgf_params["LVNSTOC_1_NSPTOC1_AssymCtrlMod"].get(),
            T1_nsptoc1_lvnstoc=self.settings["LVNSTOC_1_NSPTOC1_Top"].get(),
            I2set_nsptoc1_lvnstoc=self.settings["LVNSTOC_1_NSPTOC1_I2op"].get(),
            RatioSet_nsptoc1_lvnstoc=self.settings["LVNSTOC_1_NSPTOC1_Kasm"].get(),
            SGF1_ptrc1_ttoclgc=self.sgf_params["TTOCLGC_UIRZ_1_PTRC1_EnaDis"].get(),
            SGF2_ptrc1_ttoclgc=self.sgf_params["TTOCLGC_UIRZ_1_PTRC1_LVTPTOC2_Ctrl"].get(),
            SGF3_ptrc1_ttoclgc=self.sgf_params["TTOCLGC_UIRZ_1_PTRC1_LVTPTOC3_Ctrl"].get(),
            T1_ptrc1_ttoclgc=self.settings["TTOCLGC_UIRZ_1_PTRC1_Top"].get(),
            SGF1_ptrc1_tofflvlgc=self.sgf_params["TOFFLVLGC_1_PTRC1_EnaDis"].get(),
            SGF1_rbre1_tofflvlgc=self.sgf_params["TOFFLVLGC_1_RBRE1_EnaDis"].get(),
            SGF2_rbre1_tofflvlgc=self.sgf_params["TOFFLVLGC_1_RBRE1_PVOC2_Ctrl"].get(),
            SGF3_rbre1_tofflvlgc=self.sgf_params["TOFFLVLGC_1_RBRE1_PVOC3_Ctrl"].get(),
            SGF1_rblc1_tofflvlgc=self.sgf_params["TOFFLVLGC_1_LVCBRBLC1_EnaDis"].get(),
            SGF2_rblc1_tofflvlgc=self.sgf_params["TOFFLVLGC_1_LVCBRBLC1_PVOC2_Ctrl"].get(),
            SGF3_rblc1_tofflvlgc=self.sgf_params["TOFFLVLGC_1_LVCBRBLC1_PVOC3_Ctrl"].get(),
            Inom=self.sgf_params["Номинальный ток входа"].get(),
        )
        print("✅ partTOKZ initialized")
    
    def start_polling(self):
        if self.part is None:
            print("⚠️ partTOKZ not initialized")
            return
        self.is_polling = True
        self.polling_thread = threading.Thread(target=self.poll_inputs, daemon=True)
        self.polling_thread.start()
    
    def stop_polling(self):
        self.is_polling = False
        if self.polling_thread and self.polling_thread.is_alive():
            self.polling_thread.join(timeout=1.0)
        print("🛑 Polling stopped")
    
    def poll_inputs(self):
        while self.is_polling:
            inputs = {key: var.get() for key, var in self.input_vars.items()}
            result = self.part.Step(**inputs)
            
            # Обновление выходных значений
            for output, value in zip(self.output_labels.keys(), result):
                label = self.output_labels[output]
                label.config(text=f"{output}: {round(value, 2)}")
                if int(value) != 0 or float(value) != 0:
                    label.config(background="red", foreground="white")
                else:
                    label.config(background="green", foreground="white")
            
            time.sleep(0.3)  # Время шага опроса
            self.status_label.config(text="Шаг", background="white", foreground="white")
            time.sleep(0.05)
            self.status_label.config(text="Шаг", background="#F0F0F0", foreground="#F0F0F0")
    
    def save_to_excel(self):
        function = self.function_name.get().strip()
        mode = self.mode_name.get().strip()
        if not function or not mode:
            print("Поля 'Функция' и 'Режим' должны быть заполнены")
            return
        output_file = f"{function}_{mode}.xlsx"

        sgf_df = pd.DataFrame({key: [var.get()] for key, var in self.sgf_params.items()})
        settings_df = pd.DataFrame({key: [var.get()] for key, var in self.settings.items()})
        inputs_df = pd.DataFrame({key: [var.get()] for key, var in self.input_vars.items()})
        outputs_df = pd.DataFrame({key: [label.cget("text").split(": ")[-1]] for key, label in self.output_labels.items()})

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            sgf_df.to_excel(writer, sheet_name="SGF_Parameters", index=False)
            settings_df.to_excel(writer, sheet_name="Settings", index=False)
            inputs_df.to_excel(writer, sheet_name="Inputs", index=False)
            outputs_df.to_excel(writer, sheet_name="Outputs", index=False)

        wb = openpyxl.load_workbook(output_file)
        red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

        def format_sheet(sheet, df):
            for col_num, column in enumerate(sheet.columns, start=1):
                sheet.column_dimensions[openpyxl.utils.get_column_letter(col_num)].width = 20
                for row_num, cell in enumerate(column, start=1):
                    if row_num == 1:
                        continue
                    try:
                        if float(cell.value) != 0:
                            cell.fill = red_fill
                    except (ValueError, TypeError):
                        pass

        for sheet_name in ["SGF_Parameters", "Settings", "Inputs", "Outputs"]:
            format_sheet(wb[sheet_name], None)

        wb.save(output_file)
        print(f"Data saved to {output_file} with formatting")
    
    def load_from_excel(self):
        file_path = askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return
        try:
            xls = pd.ExcelFile(file_path)
            for sheet_name, var_dict in [("SGF_Parameters", self.sgf_params),
                                          ("Settings", self.settings),
                                          ("Inputs", self.input_vars)]:
                if sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    for key, var in var_dict.items():
                        if key in df.columns:
                            var.set(df.at[0, key])
            print("Data loaded successfully")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    # === МЕТОДЫ ДЛЯ РАБОТЫ С JSON ФАЙЛАМИ УСТАВОК ===
    
    def load_settings_from_json(self):
        """Загружает SGF и T-параметры из JSON-файла с суффиксом _SG1."""
        file_path = askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return
        try:
            handler = SettingsHandler.from_json_file(file_path)
            if not self.meta_handler:
                messagebox.showwarning("Предупреждение", "Метаданные не загружены. Используется стандартная обработка.")
            
            # --- Обновление SGF-параметров (с _SG1) ---
            for key in self.sgf_params:
                json_key = key + "_SG1"
                value_str = handler.get_value_by_parameter(json_key)
                if value_str is None:
                    continue
                try:
                    # Определяем тип из метаданных
                    type_str = None
                    if self.meta_handler:
                        param_info = self.meta_handler.get_param_info(json_key)
                        if param_info:
                            type_str = param_info.get("type")
                            print(f"{json_key}: type={type_str}, value='{value_str}'")
                    
                    # Преобразование значения в зависимости от типа
                    if type_str == "3":  # Булевое значение
                        value_lower = str(value_str).lower().strip()
                        bool_map = {
                            "true": 1, "1": 1, "on": 1, "вкл": 1, "да": 1, "yes": 1, "enabled": 1,
                            "false": 0, "0": 0, "off": 0, "выкл": 0, "нет": 0, "no": 0, "disabled": 0
                        }
                        if value_lower in bool_map:
                            self.sgf_params[key].set(bool_map[value_lower])
                        else:
                            try:
                                num_val = float(value_str)
                                self.sgf_params[key].set(1 if num_val != 0 else 0)
                            except ValueError:
                                print(f"⚠️ Неизвестное булевое значение для {json_key}: '{value_str}'")
                                self.sgf_params[key].set(0)
                    elif type_str == "130":  # Integer
                        try:
                            value_clean = str(value_str).strip()
                            for suffix in ['%', '°', '°C', 'мс', 'с', 'м']:
                                if value_clean.endswith(suffix):
                                    value_clean = value_clean[:-len(suffix)].strip()

                            int_val = int(float(value_clean.replace(',', '.')))
                            self.sgf_params[key].set(int_val)
                        except (ValueError, TypeError) as e:
                            print(f"⚠️ Ошибка преобразования int для {json_key}: '{value_str}' - {e}")
                            self.sgf_params[key].set(0)
                    else:  # По умолчанию или неизвестный тип - пробуем как int
                        try:
                            value_clean = str(value_str).strip()
                            value_lower = value_clean.lower()
                            bool_map = {
                                "true": 1, "1": 1, "on": 1, "вкл": 1,
                                "false": 0, "0": 0, "off": 0, "выкл": 0
                            }
                            if value_lower in bool_map:
                                self.sgf_params[key].set(bool_map[value_lower])
                            else:
                                int_val = int(float(value_clean.replace(',', '.')))
                                self.sgf_params[key].set(int_val)
                        except (ValueError, TypeError) as e:
                            print(f"⚠️ Не удалось преобразовать значение для {json_key}: '{value_str}' - {e}")
                            self.sgf_params[key].set(0)
                except Exception as e:
                    print(f"❌ Ошибка при обработке {json_key}: {e}")
            
            # --- Обновление T-параметров (с _SG1) ---
            for key in self.settings:
                json_key = key + "_SG1"
                value_str = handler.get_value_by_parameter(json_key)
                if value_str is None:
                    continue
                try:
                    # Определяем тип из метаданных
                    type_str = None
                    if self.meta_handler:
                        param_info = self.meta_handler.get_param_info(json_key)
                        if param_info:
                            type_str = param_info.get("type")
                            print(f"{json_key}: type={type_str}, value='{value_str}'")
                    
                    # Для settings обычно используются float значения
                    value_clean = str(value_str).strip()
                    # Убираем единицы измерения
                    units_to_remove = ['%', '°', '°c', '°с', 'мс', 'с', 'м', 'мм', 'кг', 'кпа', 'па']
                    for unit in units_to_remove:
                        if value_clean.lower().endswith(unit):
                            value_clean = value_clean[:-len(unit)].strip()
                    
                    # Заменяем запятую на точку
                    value_clean = value_clean.replace(',', '.')
                    
                    # Пробуем преобразовать в float
                    try:
                        float_val = float(value_clean)
                        # Проверяем разумные пределы для settings
                        if abs(float_val) > 1000000:
                            print(f"⚠️ Подозрительно большое значение для {json_key}: {float_val}")
                        else:
                            self.settings[key].set(float_val)
                    except ValueError as e:
                        print(f"⚠️ Невозможно преобразовать в число: {json_key} = '{value_str}' - {e}")
                except Exception as e:
                    print(f"❌ Ошибка при обработке {json_key}: {e}")
            
            messagebox.showinfo("Успех", "Уставки успешно загружены из JSON-файла.")
            print("✅ Параметры обновлены из JSON (с суффиксом _SG1)")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл не найден: {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить уставки:\n{str(e)}")
            print(f"❌ Ошибка загрузки JSON: {e}")
    
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
            # Пытаемся загрузить существующий файл, иначе создаём пустой
            try:
                handler = SettingsHandler.from_json_file(file_path)
            except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError):
                handler = SettingsHandler([])  # пустой обработчик
            
            # --- Подготовка данных SGF ---
            for base_key in self.sgf_params:
                json_key = base_key + "_SG1"
                raw_value = self.sgf_params[base_key].get()

                # Определяем тип параметра
                param_type = "3"  # значение по умолчанию — бинарный
                if self.meta_handler:
                    param_info = self.meta_handler.get_param_info(json_key)
                    if param_info and "type" in param_info:
                        param_type = str(param_info["type"])

                # Преобразуем значение в число, если возможно
                try:
                    numeric_value = float(raw_value)
                    if not numeric_value.is_integer():
                        # Если не целое — округляем или выдаём ошибку? Решите по логике.
                        # Здесь просто конвертируем в int с округлением или обрезкой
                        numeric_value = int(round(numeric_value))
                    else:
                        numeric_value = int(numeric_value)
                except (ValueError, TypeError):
                    numeric_value = 0  # или оставить как есть? Но лучше предсказуемо

                # Форматируем в зависимости от типа
                if param_type == "3":
                    # Бинарный: только 0 или 1
                    formatted = "1" if numeric_value != 0 else "0"
                elif param_type == "130":
                    # Многопозиционный: сохраняем точное целое значение
                    formatted = str(numeric_value)
                else:
                    # Для всех остальных типов — тоже сохраняем как целое (или float, если нужно)
                    formatted = str(numeric_value)

                handler.add_or_update_parameter(json_key, formatted)
                print(f"💾 {json_key} = {formatted} (type={param_type}, raw={raw_value})")
            
            # Сохраняем
            handler.save_to_json_file(file_path)
            messagebox.showinfo("Успех", f"Уставки сохранены в:\n{file_path}")
            print(f"✅ Уставки сохранены в {file_path}")
        except Exception as e:
            error_msg = f"Ошибка при сохранении уставок:\n{str(e)}"
            messagebox.showerror("Ошибка", error_msg)
            print(f"❌ {error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PartOfTOKGUI(root)
    root.mainloop()