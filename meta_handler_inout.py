


from MainConfigHandler import MainConfigHandler



meta_path = "meta.json"
config_handler = MainConfigHandler.from_json_file(meta_path)


#t = config_handler.get_param_info("T_LVCBSUP_1_RCBF1_FuncEnabled")
#print(t) lvrbvtr1

pars = config_handler.find_parameters_starting_with("T_SWCTRL_1_OpnCBFrm_ACS")

for par in pars:
    if par["group"] == "measurement": # and par["fullDescription"] == "Внешнее отключение от УРОВ НН":
        print(par)


