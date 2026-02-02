# combined_gui.py — полная версия с редактированием, выпадающими списками и валидацией

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
import re
from InOutsMatrixHandler import InOutsMatrixHandler
from MainConfigHandler import MainConfigHandler


class MatrixEditorApp:
    def __init__(self, root: tk.Tk, inouts_handler: InOutsMatrixHandler, config_handler: MainConfigHandler, matrix_file_path: str):
        self.root = root
        self.inouts_handler = inouts_handler
        self.config_handler = config_handler
        self.matrix_file_path = matrix_file_path

        # === Настройка диапазонов (можно менять) ===
        self.ins = ["8-14", "9-2"]   # формат: "банк-количество"
        self.outs = ["3-8", "4-8"]

        # Генерация допустимых значений
        self.discrete_options = ["-"] + self._generate_from_ranges(self.ins, letter="B")
        self.relay_options = ["-"] + self._generate_from_ranges(self.outs, letter="K")

        self.root.title("Редактор матрицы входов/выходов")
        self.root.geometry("950x600")

        # Кнопка сохранения
        save_btn = tk.Button(root, text="💾 Сохранить в JSON", command=self.save_changes)
        save_btn.pack(pady=5)

        # Таблица
        columns = ("param_desc", "discrete", "digital", "relay")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=25)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        headings = {
            "param_desc": "Параметр (описание)",
            "discrete": "Дискр.Вход",
            "digital": "Двоич.Вход",
            "relay": "Вых. Реле"
        }
        self.sort_states = {col: False for col in columns}

        for col, text in headings.items():
            self.tree.heading(col, text=text, command=lambda c=col: self.sort_by_column(c))
            width = 300 if col == "param_desc" else 150
            self.tree.column(col, width=width)

        self.tree.bind("<Double-1>", self.on_double_click)

        vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.item_param_map = {}
        self.load_data_into_tree()

    def _generate_from_ranges(self, ranges: List[str], letter: str) -> List[str]:
        """Генерирует список адресов по шаблонам вида ['8-8', '9-14'] с указанной буквой (B или K)."""
        result = []
        for r in ranges:
            if '-' not in r:
                continue
            try:
                bank_str, count_str = r.split('-', 1)
                bank = int(bank_str)
                count = int(count_str)
                for i in range(1, count + 1):
                    result.append(f"{bank}{letter}{i}")
            except ValueError:
                continue  # игнорируем некорректные записи
        return result

    def load_data_into_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.item_param_map.clear()

        for param_name in self.inouts_handler.get_all_parameter_names():
            param_info = self.config_handler.get_param_info(param_name)
            description = param_info.get("description", param_name) if param_info else param_name

            disc = ", ".join(self.inouts_handler.get_discrete_inputs(param_name)) or "-"
            digi = ", ".join(self.inouts_handler.get_digital_inputs(param_name)) or "-"
            rel  = ", ".join(self.inouts_handler.get_output_relays(param_name)) or "-"

            iid = self.tree.insert("", "end", values=(description, disc, digi, rel))
            self.item_param_map[iid] = param_name

    def on_double_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)

        if column == "#1":  # описание — только для чтения
            return

        col_index = int(column.replace("#", "")) - 1
        if col_index not in (1, 2, 3):
            return

        current_value = self.tree.item(row, "values")[col_index]
        if current_value == "-":
            current_value = ""

        x, y, width, height = self.tree.bbox(row, column)

        # === Выбор редактора в зависимости от столбца ===
        if col_index == 1:  # Дискр.Вход → Combobox
            widget = ttk.Combobox(self.tree, values=self.discrete_options, state="readonly")
            widget.set(current_value if current_value in self.discrete_options else "-")
        elif col_index == 3:  # Вых. Реле → Combobox
            widget = ttk.Combobox(self.tree, values=self.relay_options, state="readonly")
            widget.set(current_value if current_value in self.relay_options else "-")
        else:  # Двоич.Вход → обычное поле
            widget = ttk.Entry(self.tree)
            widget.insert(0, current_value)
            widget.select_range(0, tk.END)

        widget.place(x=x, y=y, width=width, height=height)
        widget.focus()

        def save_edit(_):
            if isinstance(widget, ttk.Combobox):
                new_val = widget.get()
            else:
                new_val = widget.get().strip()
            values = list(self.tree.item(row, "values"))
            values[col_index] = new_val if new_val else "-"
            self.tree.item(row, values=values)
            widget.destroy()

            param_name = self.item_param_map[row]
            self.update_inouts_data(param_name, values[1], values[2], values[3])

        widget.bind("<Return>", save_edit)
        widget.bind("<FocusOut>", save_edit)
        widget.bind("<Escape>", lambda _: widget.destroy())

        if isinstance(widget, ttk.Combobox):
            widget.bind("<<ComboboxSelected>>", save_edit)

    def parse_input_list(self, s: str) -> List[str]:
        if not s or s == "-":
            return []
        return [part.strip() for part in s.split(",") if part.strip()]

    def update_inouts_data(self, param_name: str, disc_str: str, digi_str: str, relay_str: str):
        disc = self.parse_input_list(disc_str)
        digi = self.parse_input_list(digi_str)
        relay = self.parse_input_list(relay_str)
        self.inouts_handler.update_signal_mapping(param_name, disc, digi, relay)

    def sort_by_column(self, col: str):
        items = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        def sort_key(item):
            val = item[0]
            if val == "-":
                return (0, "")
            try:
                return (1, int(val))
            except ValueError:
                return (1, val.lower())
        items.sort(key=sort_key, reverse=self.sort_states[col])
        for index, (_, child) in enumerate(items):
            self.tree.move(child, '', index)
        self.sort_states[col] = not self.sort_states[col]

    def save_changes(self):
        try:
            discrete_addresses = []
            seen_discrete = set()
            duplicate_found = False
            cyrillic_errors = []

            for item in self.tree.get_children():
                values = self.tree.item(item, "values")
                param_name = self.item_param_map[item]

                # Дискр.Вход
                disc_str = values[1]
                if disc_str != "-":
                    parts = [p.strip() for p in disc_str.split(",") if p.strip()]
                    for addr in parts:
                        if re.search(r'[А-Яа-яЁё]', addr):
                            cyrillic_errors.append(f"Дискр.Вход: {addr} (параметр: {param_name})")
                        if addr in seen_discrete:
                            duplicate_found = True
                        else:
                            seen_discrete.add(addr)
                        discrete_addresses.append(addr)

                # Вых. Реле
                relay_str = values[3]
                if relay_str != "-":
                    parts = [p.strip() for p in relay_str.split(",") if p.strip()]
                    for addr in parts:
                        if re.search(r'[А-Яа-яЁё]', addr):
                            cyrillic_errors.append(f"Вых. Реле: {addr} (параметр: {param_name})")

            error_messages = []
            if cyrillic_errors:
                error_messages.append(
                    "Обнаружены кириллические символы в адресах:\n" +
                    "\n".join(cyrillic_errors) +
                    "\n\nИспользуйте только латинские буквы (например, 'B', а не 'В')."
                )
            if duplicate_found:
                error_messages.append(
                    "Обнаружены повторяющиеся адреса в столбце 'Дискр.Вход'.\n"
                    "Каждый дискретный вход должен использоваться только один раз."
                )

            if error_messages:
                messagebox.showerror("Ошибка при сохранении", "\n\n".join(error_messages))
                return

            self.inouts_handler.save_to_json_file(self.matrix_file_path)
            messagebox.showinfo("Успех", f"Изменения успешно сохранены в:\n{self.matrix_file_path}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")


def create_editor_window(inouts_handler: InOutsMatrixHandler, config_handler: MainConfigHandler, matrix_file_path: str):
    root = tk.Tk()
    app = MatrixEditorApp(root, inouts_handler, config_handler, matrix_file_path)
    root.mainloop()


if __name__ == "__main__":
    METADATA_FILE = "meta.json"
    MATRIX_FILE = "ЮНИТ-М319 Т Матрица входов и выходных реле 2026-02-02 14_32_56.json"

    try:
        config_handler = MainConfigHandler.from_json_file(METADATA_FILE)
        inouts_handler = InOutsMatrixHandler.from_json_file(MATRIX_FILE)
        create_editor_window(inouts_handler, config_handler, MATRIX_FILE)
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        input("Нажмите Enter для выхода...")