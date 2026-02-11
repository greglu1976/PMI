


from MainConfigHandler import MainConfigHandler



meta_path = "meta.json"
config_handler = MainConfigHandler.from_json_file(meta_path)

pars = config_handler.find_parameters_starting_with("LVNSTOC_1_NSPTOC1")

for par in pars:
    if par["group"] == "setting":
        print(par["name"] , par["description"], par["fullDescription"], par["appliedDescription"])


