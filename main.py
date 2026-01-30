
from MainConfigHandler import MainConfigHandler
from SettingsHandler import SettingsHandler



meta = MainConfigHandler.from_json_file("meta.json")

set = meta.find_parameter_name_by_rus_name_and_full_desc_in_settings("ЛЗТ", "Ввод функции в работу",1)

print(set[0])
print(meta.get_param_info(set[0]))



# Загрузка
handler = SettingsHandler.from_json_file("ЮНИТ-М319 Т Уставки РЗиА 2026-01-30 14_37_56.json")

found = handler.get_value_by_parameter(set[0])
print(found)


handler.set_value_to_parameter(set[0], "True")

print(handler.get_value_by_parameter(set[0]))

# Изменение
#handler.set_value_to_parameter("TLTCGASLGC_1_PTRC1_EnaDis_SG1", "False")

# Сохранение в том же формате
handler.save_to_json_file("updated_settings.json")