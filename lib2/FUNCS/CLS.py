
# Контроль ресурса выключателя
# КРВ

from lib2.TIMERS.TIMERS import TOF, TP
from lib2.TRIGGERS.TRIGGERS import R_TRIG_Counter

import math


class CLS:

    def __init__(self, SGF1 = 0, Inom_V_pasp = 1000, Inom_otl_V_pasp = 31500, KRVpasp_Inom = 4000, KRVpasp_Inom_otkl = 100,
                MRVpasp = 200000, Nach_znach_KRV = 100, KRVsrab = 20, Nach_znach_MRV = 0, SGF2 = 0, T1 = 1000):

        self.SGF1 = SGF1
        self.Inom_V_pasp = Inom_V_pasp
        self.Inom_otl_V_pasp = Inom_otl_V_pasp
        self.KRVpasp_Inom = KRVpasp_Inom
        self.KRVpasp_Inom_otkl = KRVpasp_Inom_otkl
        self.MRVpasp = MRVpasp
        self.Nach_znach_KRV = Nach_znach_KRV
        self.KRVsrab = KRVsrab
        self.Nach_znach_MRV = Nach_znach_MRV 
        self.SGF2 = SGF2
        self.T1 = TP(T1)
        self.T2 = TOF(1)

        self.KRV = Nach_znach_KRV  # Заданный начальный механический ресурс
        self.MRV = Nach_znach_MRV  # Заданный начальный коммутационный ресурс

        self.current_KRV_A = Nach_znach_KRV  # Текущий механический ресурс
        self.current_KRV_B = Nach_znach_KRV  # Текущий механический ресурс
        self.current_KRV_C = Nach_znach_KRV  # Текущий механический ресурс
        self.current_MRV = Nach_znach_MRV  # Текущий коммутационный ресурс

        # Счетчик для МРВ
        self.counter = R_TRIG_Counter(Nach_znach_MRV)

        # Переменные для измерения максимального тока
        self.max_current_during_pulse_A = 0.0
        self.max_current_during_pulse_B = 0.0
        self.max_current_during_pulse_C = 0.0
        self.is_measuring = False  # Флаг измерения
        self.pending_calc = False  # Флаг ожидания расчета после импульса



    def calc_KRV(self, krv, Imax):
        power = (Imax/self.Inom_V_pasp)
        t = self.MRVpasp*(self.KRVpasp_Inom/self.MRVpasp)**power
        return krv - 100/t

    def calc_KRV_Imax(self, krv, Imax):
        power = (math.log(self.Inom_otl_V_pasp/Imax))/(math.log(self.Inom_otl_V_pasp/self.Inom_V_pasp))
        t = self.KRVpasp_Inom_otkl*(self.KRVpasp_Inom/self.KRVpasp_Inom_otkl)**power
        return krv - 100/t

    def Step(self, DI_ControllerDisable, CLS_1_CBPosCls, CLS_1_CBPosOpn, CLS_1_ResetCounter, CLS_1_OpnCB, IA, IB, IC):

        CLS_1_CLS_FuncEnabled = (not DI_ControllerDisable) and (0 if self.SGF1 == 0 else 1)

        self.T2.IN = CLS_1_CBPosCls
        srab_T2, _ = self.T2.start()
        pusk_MRV = srab_T2 and CLS_1_CBPosOpn and CLS_1_CLS_FuncEnabled # Пуск МРВ найден

        sbros = CLS_1_ResetCounter or not (0 if self.SGF1 == 0 else 1)

        ######################################################################################
        # Сбрасываем счетчик МРВ если есть Сброс
        if sbros:
            self.counter.reset(self.MRV)
        else:
            self.counter.run(pusk_MRV)
        # Механический ресурс посчитан
        ######################################################################################

        ######################################################################################
        # Обрабатываем коммутационный ресурс
        self.T1.IN = CLS_1_OpnCB
        srab_T1, ET = self.T1.start()

        # Определяем начало импульса (передний фронт)
        print(srab_T1, CLS_1_CBPosOpn, CLS_1_CLS_FuncEnabled, ET )
        if srab_T1 and CLS_1_CBPosOpn and CLS_1_CLS_FuncEnabled:
            if not self.is_measuring:
                # Начинаем измерение
                self.is_measuring = True
                self.max_current_during_pulse_A = 0.0
                self.max_current_during_pulse_B = 0.0
                self.max_current_during_pulse_C = 0.0
                self.pending_calc = False
        # Измеряем максимальный ток во время активного импульса

        if self.is_measuring:
            # Обновляем максимальный ток
            
            if IA > self.max_current_during_pulse_A:
                self.max_current_during_pulse_A = IA
            if IB > self.max_current_during_pulse_B:
                self.max_current_during_pulse_B = IB
            if IC > self.max_current_during_pulse_C:
                self.max_current_during_pulse_C = IC

            # Проверяем окончание импульса (когда TP таймер закончил работу)
            if not srab_T1:
                # Импульс закончился, выполняем расчет
                if not self.pending_calc:

                    # Используем измеренный максимальный ток ф.А для расчета
                    if self.max_current_during_pulse_A>0:
                        if self.Inom_V_pasp >= self.max_current_during_pulse_A:
                            self.current_KRV_A = self.calc_KRV(self.current_KRV_A, self.max_current_during_pulse_A)
                        if self.max_current_during_pulse_A > self.Inom_V_pasp:
                            self.current_KRV_A = self.calc_KRV_Imax(self.current_KRV_A, self.max_current_during_pulse_A)

                    # Используем измеренный максимальный ток ф.В для расчета
                    if self.max_current_during_pulse_B>0:
                        if self.Inom_V_pasp >= self.max_current_during_pulse_B:
                            self.current_KRV_B = self.calc_KRV(
                                self.current_KRV_B, 
                                self.max_current_during_pulse_B
                            )
                        if self.max_current_during_pulse_B > self.Inom_V_pasp:
                            self.current_KRV_B = self.calc_KRV_Imax(
                                self.current_KRV_B, 
                                self.max_current_during_pulse_B
                            )

                    # Используем измеренный максимальный ток ф.В для расчета
                    if self.max_current_during_pulse_C>0:
                        if self.Inom_V_pasp >= self.max_current_during_pulse_C:
                            self.current_KRV_C = self.calc_KRV(
                                self.current_KRV_C, 
                                self.max_current_during_pulse_C
                            )
                        if self.max_current_during_pulse_C > self.Inom_V_pasp:
                            self.current_KRV_C = self.calc_KRV_Imax(
                                self.current_KRV_C, 
                                self.max_current_during_pulse_C
                            )

                                      
                    self.pending_calc = True
                self.is_measuring = False
        ###############################################################################################

        # Сбрасываем значения КРВ если есть Сброс
        if sbros:
            self.current_KRV_A = self.KRV
            self.current_KRV_B = self.KRV
            self.current_KRV_C = self.KRV

        # ============ ФОРМИРОВАНИЕ ВЫХОДНЫХ СИГНАЛОВ ============

        CLS_1_CLS_MDCurrentResource = self.counter.get_count()
        CLS_1_CLS_MDResourceExcess = 0
        if not DI_ControllerDisable and CLS_1_CLS_MDCurrentResource>self.MRVpasp:
            CLS_1_CLS_MDResourceExcess = 1

        CLS_1_CLS_COMMResourceExcess  = 0
        if not DI_ControllerDisable and (self.current_KRV_A < self.KRVsrab or self.current_KRV_B < self.KRVsrab or self.current_KRV_C < self.KRVsrab):
            CLS_1_CLS_COMMResourceExcess  = 1
        
        CLS_1_CLS_CBLifeExcess = (CLS_1_CLS_MDResourceExcess if self.SGF2 == 1 else 0) or CLS_1_CLS_COMMResourceExcess 

        CLS_1_CLS_COMMCurrResourcePhsA = self.current_KRV_A
        CLS_1_CLS_COMMCurrResourcePhsB = self.current_KRV_B
        CLS_1_CLS_COMMCurrResourcePhsC = self.current_KRV_C

        return CLS_1_CLS_FuncEnabled, CLS_1_CLS_MDResourceExcess, CLS_1_CLS_CBLifeExcess, CLS_1_CLS_COMMResourceExcess, CLS_1_CLS_MDCurrentResource, CLS_1_CLS_COMMCurrResourcePhsA, CLS_1_CLS_COMMCurrResourcePhsB, CLS_1_CLS_COMMCurrResourcePhsC
                

