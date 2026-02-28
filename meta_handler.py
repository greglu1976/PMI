


from MainConfigHandler import MainConfigHandler



meta_path = "meta.json"
config_handler = MainConfigHandler.from_json_file(meta_path)

#pars = config_handler.find_parameters_starting_with("T_HVTCBOFF")

#for par in pars:
    #if par["group"] == "setting":
        #print(par["name"] , par["description"], par["fullDescription"], par["appliedDescription"])



# Поиск значений по имени
par_info = config_handler.get_param_info("LVTTOC_1_PTOC1_VolMod") # 1 - 1/2
print(par_info)




keys = [
    "T_LVCBSUP_1_RCBF1_EnaDis",
    "T_LVCBSUP_1_RCBF1_BlkToClsFrmLowIsol",
    "T_LVCBSUP_1_RCBF1_BlkFrmCBPosFault",
    "T_LVCBSUP_1_RCBF1_RstFrmCLS",
    "T_LVCBSUP_1_RCBF1_OCcircuitFailureCtrl",
    "T_LVCBSUP_1_RCBF1_ConditionForElmgLaunchFault",
    "T_LVCBSUP_1_RCBF1_KnobCtrl",
    "T_LVCBSUP_1_RCBF1_BlkCtrlFrmInsAlm",
    "T_SWCTRL_1_SWCTRL_EnaDis",
    "T_SWCTRL_1_CBCSWI1_EnaDis",
    "T_SWCTRL_1_CBCSWI1_BlkToClsFrmFailureTrip",
    "T_HVBCTRL_1_CBCSWI1_EnaDis",
    "T_SwitchDevice_1_SD_EnaDis",
    "T_SwitchDevice_1_CB1_EnaDis",
    "T_SwitchDevice_1_CB1_TPOpnResetCtrl",
    "T_SwitchDevice_1_CB1_CBOSoperationCtrl",
    "T_SwitchDevice_1_CB1_TPClsResetCtrl",
    "T_SwitchDevice_1_CB1_CBCSoperationCtrl",
    "T_TPBRF_1_GENRBRF1_EnaDis",
    "T_TPBRF_1_GENRBRF1_BlkToOpnSpeedUp",
    "T_TPBRF_1_GENRBRF1_CurrentPickUp",
    "T_TPBRF_1_GENRBRF1_CBOSTypeCtrl",
    "T_TPBRF_1_GENRBRF1_ActUpSwitch",
    "T_TPBRF_1_GENRBRF1_TypeOfCtrlCurrent",
    "T_HVTCBOFF_1_HVCBPTRC1_EnaDis",
    "T_LVALH_1_CALH1_GASSign_Ctl",
    "T_LVALH_1_CALH1_LowIsolGAS_Ctl",
    "T_LVALH_1_CALH1_GASBlock_Ctl",
    "T_LVALH_1_CALH1_TECHSign_Ctl",
    "T_LVALH_1_CALH1_LowIsolTECH_Ctl",
    "T_LVALH_1_CALH1_TECHBlock_Ctl",
    "T_LVALH_1_CALH1_ALMSign_Ctl",
    "T_LVALH_1_CALH1_OCSign_Ctl",
    "T_LVALH_1_CALH1_OCnnSign_Ctl",
    "T_LVALH_1_CALH1_OpExt_Ctl",
    "T_LVALH_1_CALH1_CtlCir_Ctl",
    "T_LVALH_1_CALH1_TestBlock_Ctl",
    "T_LVALH_1_CALH1_SwOperExcTim_Ctl",
    "T_LVALH_1_CALH1_ExtSignGen_Ctl"
]
for key in keys:
    par_info = config_handler.get_param_info(key)
    #print(par_info["defaultValue"], par_info["minValue"], par_info["maxValue"])