


from MainConfigHandler import MainConfigHandler



meta_path = "meta.json"
config_handler = MainConfigHandler.from_json_file(meta_path)

pars = config_handler.find_parameters_starting_with("LVTCBOFF")

for par in pars:
    if par["group"] == "setting":
        print(par["name"] , par["description"], par["fullDescription"], par["appliedDescription"])

'''

# Поиск значений по имени
par_info = config_handler.get_param_info("LVTTOC_1_PTOC1_VolMod") # 1 - 1/2
print(par_info["defaultValue"], par_info["minValue"], par_info["maxValue"])

par_info = config_handler.get_param_info("LVTTOC_1_PTOC2_ExtVFlMod") #2 - 1/2
print(par_info["defaultValue"], par_info["minValue"], par_info["maxValue"])

par_info = config_handler.get_param_info("LVTTOC_1_RBLC1_StepSel") #4 1 4 БЛЗШ
print(par_info["defaultValue"], par_info["minValue"], par_info["maxValue"])

par_info = config_handler.get_param_info("T_LVARCTOC_1_PTOC1_StrMod") #0 0 3 ТК ЗДЗ !!!!!!!!!!! очень странно
print(par_info["defaultValue"], par_info["minValue"], par_info["maxValue"])

'''