    def load_settings_from_json(self):
        """Загружает SGF и T-параметры из JSON-файла, добавляя '_SG1' к именам."""
        file_path = askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        try:
            handler = SettingsHandler.from_json_file(file_path)

            # --- Обновление SGF-параметров (с _SG1) ---
            for key in self.sgf_params:
                json_key = key + "_SG1"
                value_str = handler.get_value_by_parameter(json_key)
                if value_str is not None:
                    try:
                        # Обработка булевых значений и числовых
                        value_lower = str(value_str).lower().strip()
                        
                        if value_lower in ("true", "1", "on", "вкл", "да", "yes"):
                            self.sgf_params[key].set(1)
                        elif value_lower in ("false", "0", "off", "выкл", "нет", "no"):
                            self.sgf_params[key].set(0)
                        else:
                            # Пробуем преобразовать в int
                            try:
                                int_val = int(float(value_str))  # Сначала float, потом int для случаев "1.0"
                                self.sgf_params[key].set(int_val)
                                print(f"Загружено числовое значение для {json_key}: {int_val}")
                            except (ValueError, TypeError):
                                print(f"⚠️ Неизвестное значение для {json_key}: '{value_str}'")
                                # Можно установить значение по умолчанию
                                # self.sgf_params[key].set(0)
                    except Exception as e:
                        print(f"Ошибка при обработке {json_key}: {e}")

            # --- Обновление T-параметров (с _SG1) ---
            for key in self.settings:
                json_key = key + "_SG1"
                value_str = handler.get_value_by_parameter(json_key)
                if value_str is not None:
                    try:
                        # Очистка и преобразование
                        value_str_clean = str(value_str).strip()
                        
                        # Убираем лишние символы если есть
                        if value_str_clean.endswith(('%', '°', '°C', 'мс', 'с', 'м')):
                            value_str_clean = value_str_clean.rstrip('%°Cмс').strip()
                        
                        # Пробуем разные форматы чисел
                        try:
                            # Пробуем как float
                            val = float(value_str_clean)
                            self.settings[key].set(val)
                        except ValueError:
                            # Пробуем заменить запятую на точку
                            if ',' in value_str_clean:
                                val = float(value_str_clean.replace(',', '.'))
                                self.settings[key].set(val)
                            else:
                                print(f"⚠️ Невозможно преобразовать в число: {json_key} = '{value_str}'")
                                # Можно установить значение по умолчанию 1.0
                                # self.settings[key].set(1.0)
                    except Exception as e:
                        print(f"Ошибка при обработке {json_key}: {e}")

            messagebox.showinfo("Успех", "Уставки успешно загружены из JSON-файла.")
            print("Параметры обновлены из JSON (с суффиксом _SG1)")

        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл не найден: {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить уставки:\n{str(e)}")
            print(f"Ошибка загрузки JSON: {e}")