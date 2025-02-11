# Логика тестирования ФСУ ДЗТ2 в части логики отключения от газовых защит 

import time

from TECHPTRC import TECHPTRC
from lib.TECHPTRC_2.TECHPTRC_2 import TECHPTRC_2
from TJNTPTRC import TJNTPTRC
from DZT2_SignAssembly import DZT2_SignAssembly
from DZT2_LVALH import DZT2_LVALH
# Инициализация функций


# Создаем модель устройства
LO_GZotkl = TECHPTRC(SGF1 = 1, SGF2 = 1, T=0)
LO_GZsign = TECHPTRC_2(SGF1 = 1, SGF2 = 1, T=0)
LO_GZ_RPN = TECHPTRC(SGF1 = 1, SGF2 = 1, T=0)
LO_T = TJNTPTRC(SGF1=1)
ZAPV_T = TJNTPTRC(SGF1=1)
PS = DZT2_LVALH(SGF1=1, SGF2=1, SGF3=1) # Разрешаем контролировать сигналы от ГЗ
SS = DZT2_SignAssembly()


try:
    while True:
        # Здесь можно задать значения для входных параметров
        ##### ОБЩИЕ ПАРАМЕТРЫ 
        VYVOD = 0           # Вывод терминала
        Sbros = 0           # Сброс блок. ГЗ,ТЗ
        ###### Параметры ЛО ГЗоткл
        OVGZotkl = 0        # ОВ ГЗоткл
        GZotklNaSign = 0    # ГЗоткл на сигн
        otklKontGazRele = 0 # Откл.конт.газ. реле
        srabKIGZotkl = 0    # Сраб. КИ ГЗ_откл
        ###### Параметры ЛО ГЗсигн
        OVGZsign = 0        # ОВ ГЗоткл
        GZsignNaOtkl = 0    # ГЗсигн на сигн
        signKontGazRele = 0 # Сигн.конт.газ. реле
        srabKIGZsign = 0    # Сраб. КИ ГЗсигн
        ###### Параметры ЛО ГЗ РПН
        OVGZRPN = 0         # ОВ ГЗ РПН
        GZRPNnaSign = 0     # ГЗ РПН на сигн
        KontStruiRele = 0   # конт.струйн.газ.
        srabKIRPN = 0       # Сраб. КИ ГЗ РПН
        ###### Параметры ЛО Т

        # Выполнить шаг PLC
        GZotkl_vvod, GZotkl_oper_vyvod, GZotkl_srab, GZotkl_srabsign, GZotkl_zablok, GZotkl_ET = LO_GZotkl.Step(VYVOD = VYVOD, Sbros = Sbros, OV = OVGZotkl, NaSign = GZotklNaSign, srabKont = otklKontGazRele, srabKI = srabKIGZotkl)

        GZsign_vvod, GZsign_oper_vyvod, GZsign_srab, GZsign_srabsign, GZsign_zablok, GZsign_ET = LO_GZsign.Step(VYVOD = VYVOD, Sbros = Sbros, OV = OVGZsign, NaOtkl = GZsignNaOtkl, srabKont = signKontGazRele, srabKI = srabKIGZsign)

        GZRPN_vvod, GZRPN_oper_vyvod, GZRPN_srab, GZRPN_srabsign, GZRPN_zablok, GZRPN_ET = LO_GZ_RPN.Step(VYVOD = VYVOD, Sbros = Sbros, OV = OVGZRPN, NaSign = GZRPNnaSign, srabKont = KontStruiRele, srabKI = srabKIRPN)

        LO_T_vvod, LO_T_oper_vyvod, LO_T_srab, LO_T_pusk = LO_T.Step(OPVYVOD = (VYVOD,), ARGS = (GZotkl_srab, GZsign_srab, GZRPN_srab))
        ZAPV_T_vvod, ZAPV_T_oper_vyvod, ZAPV_T_srab, ZAPV_T_pusk = ZAPV_T.Step(OPVYVOD = (VYVOD,) , ARGS = (LO_T_pusk,))

        SS_GZsign, SS_NizkIsolGZ, SS_GZzablok, SS_TZsign, SS_NizkIsolTZ, SS_TZzablok, SS_TSsign, SS_VneshOtkl, SS_VyhZepiRazobr, SS_BIvyved, SS_OTsign, SS_NeispOTGZ, SS_NeispOTTZ, SS_OTNNsign, SS_VneshSign = SS.Step(VYVOD = VYVOD, GZsign = (otklKontGazRele, signKontGazRele, KontStruiRele), NizkIsolGZ = (srabKIGZotkl, srabKIGZsign, srabKIRPN), GZzablok = (GZotkl_zablok, GZsign_zablok, GZRPN_zablok))

        PS_pusk = PS.Step(VYVOD = VYVOD,  COMM_SIGN = (GZotkl_srabsign ,GZsign_srabsign, GZRPN_srabsign,), sgf1_sign = SS_GZsign , sgf2_sign = SS_NizkIsolGZ , sgf3_sign = SS_GZzablok )


        print("Выходы:", 'ПС: Пуск>',  PS_pusk)  # Печать выходных значений
        print("Выходы:", 'ЛО_Т: Срабатывание>',  LO_T_srab)  # Печать выходных значений        
        time.sleep(1)  # Задержка на 1 секунду для имитации циклической работы
except KeyboardInterrupt:
    print("Остановка....")