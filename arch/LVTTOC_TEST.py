# тестирование функции МТЗ из 3 ступеней, БНТ, БЛЗШ, двух КПОН

#SGF1 - Ввод_функции - Ввод функции в работу (Не предусмотрено/ Предусмотрено)
#SGF2 - Тип_КПОН - Тип пуска по напряжению (Управляющее напряжение / Вольтметровая блокировка)
#SGF3 - Реж_БНТ - Режим контроля от БНТ (Не предусмотрено/ Предусмотрено)
#SGF4 - Реж_БНН_КПОН - Режим КПОН при неисправности ЦН  (Деблокировка (Чувств. уставка)/ Блокировка (Грубая уставка))
#SGF5 - Реж_КПОН1 - Режим контроля от КПОН1 (Не предусмотрено/ Предусмотрено)
#SGF6 - Реж_КПОН2 - Режим контроля от КПОН2 (Не предусмотрено/ Предусмотрено)
#SGF7 - Контр_СВ - Режим контроля СВ НН (Не предусмотрено/ Блокировка ступени при включенном СВ/ 	Блокировка ступени при отключенном СВ)

import time
import pandas as pd
from openpyxl import Workbook
from LVTTOC_FB_MTZ import LVTTOC

# Создаем экземпляр класса LVTPTOC
lvttoc = LVTTOC(SGF1=1, 
SGF1_ptoc1=1, SGF2_ptoc1=0, SGF3_ptoc1=0, SGF4_ptoc1=0, SGF5_ptoc1=0, SGF6_ptoc1=0, SGF7_ptoc1=0, T1_ptoc1=0, Iset_ptoc1=1, Icoarse_ptoc1=2,
SGF1_ptoc2=0, SGF2_ptoc2=0, SGF3_ptoc2=0, SGF4_ptoc2=0, SGF5_ptoc2=0, SGF6_ptoc2=0, SGF7_ptoc2=0, T1_ptoc2=0, Iset_ptoc2=1, Icoarse_ptoc2=2,
SGF1_ptoc3=0, SGF2_ptoc3=0, SGF3_ptoc3=0, SGF4_ptoc3=0, SGF5_ptoc3=0, SGF6_ptoc3=0, SGF7_ptoc3=0, T1_ptoc3=0, Iset_ptoc3=1, Icoarse_ptoc3=2,
SGF1_ptuv1=0, Uop_ptuv1=40, U2op_ptuv1=5,
SGF1_ptuv2=0, Uop_ptuv2=40, U2op_ptuv2=5,
SGF1_phar1=0, Imax_phar1=3, Ratio_phar1=0.4,
SGF1_rblc1=0
)

# Определяем возможные входные значения для тестирования
input_values = {
    "VYVOD": [0, 1],
    "OV": [0, 1],
    "OVst_ptoc1": [0,],
    "OVst_ptoc2": [0,],
    "OVst_ptoc3": [0,],        
    "NaSign_ptoc1": [0,],
    "NaSign_ptoc2": [0,], 
    "NaSign_ptoc3": [0,],       
    "SV1vkl": [0,],
    "SV2vkl": [0,],
    "IA": [0,],
    "IAB": [0,],
    "IB": [0,],
    "IBC": [0,],
    "IC": [0, ],
    "ICA": [0,],
    "UAB_ptuv1": [0,],
    "UBC_ptuv1": [0,],
    "UCA_ptuv1": [0,],
    "U2_ptuv1": [0,],
    "UAB_ptuv2": [0,],
    "UBC_ptuv2": [0,],
    "UCA_ptuv2": [0,],
    "U2_ptuv2": [0,],
    "KPONvnesh_ptuv1": [0,],
    "KPONvnesh_ptuv2": [0,],
    "IA2harm": [0,],
    "IB2harm": [0,],
    "IC2harm": [0,],
    "KZN1neipr": [0,],
    "VNN1vkl": [0,],
    "KZN2neipr": [0,],
    "VNN2vkl": [0,]
}

# Генерация всех возможных комбинаций входных значений
import itertools


# Создаем DataFrame для хранения результатов
columns = list(input_values.keys()) + [
 "vvod_ptoc1", "oper_vyvod_ptoc1", "mtzA_pusk_ptoc1", "mtzB_pusk_ptoc1", "mtzC_pusk_ptoc1", "gen_pusk_ptoc1", "mtz_srabsign_ptoc1", "mtz_srab_ptoc1", "io_A_ptoc1", "io_B_ptoc1", "io_C_ptoc1", "vvod_ptoc2", "oper_vyvod_ptoc2", "mtzA_pusk_ptoc2", "mtzB_pusk_ptoc2", "mtzC_pusk_ptoc2", "gen_pusk_ptoc2", "mtz_srabsign_ptoc2", "mtz_srab_ptoc2", "io_A_ptoc2", "io_B_ptoc2", "io_C_ptoc2",             "vvod_ptoc3", "oper_vyvod_ptoc3", "mtzA_pusk_ptoc3", "mtzB_pusk_ptoc3", "mtzC_pusk_ptoc3", "gen_pusk_ptoc3", "mtz_srabsign_ptoc3", "mtz_srab_ptoc3", "io_A_ptoc3", "io_B_ptoc3", "io_C_ptoc3",            "kpon_pusk_ptuv1", "kpon_pusk_ptuv2", "ia_start_out_phar1", "ib_start_out_phar1", "ic_start_out_phar1", "start_phar1", "blok_rblc1", "mtz_pusk"  
]
results = []

# Перебираем все комбинации входных значений
for inputs in itertools.product(*input_values.values()):
    input_dict = dict(zip(input_values.keys(), inputs))
    
    # Вызываем метод Step
    result = lvttoc.Step(
        VYVOD=input_dict["VYVOD"],
        OV=input_dict["OV"],
        OVst_ptoc1=input_dict["OVst_ptoc1"],
        OVst_ptoc2=input_dict["OVst_ptoc2"],
        OVst_ptoc3=input_dict["OVst_ptoc3"],
        NaSign_ptoc1=input_dict["NaSign_ptoc1"],
        NaSign_ptoc2=input_dict["NaSign_ptoc2"],
        NaSign_ptoc3=input_dict["NaSign_ptoc3"],
        SV1vkl=input_dict["SV1vkl"],
        SV2vkl=input_dict["SV2vkl"],
        IA=input_dict["IA"],
        IB=input_dict["IB"],
        IC=input_dict["IC"],
        IAB=input_dict["IAB"],
        IBC=input_dict["IBC"],
        ICA=input_dict["ICA"],
        UAB_ptuv1=input_dict["UAB_ptuv1"],
        UBC_ptuv1=input_dict["UBC_ptuv1"],
        UCA_ptuv1=input_dict["UCA_ptuv1"],
        UAB_ptuv2=input_dict["UAB_ptuv2"],
        UBC_ptuv2=input_dict["UBC_ptuv2"],
        UCA_ptuv2=input_dict["UCA_ptuv2"],
        U2_ptuv1=input_dict["U2_ptuv1"],
        U2_ptuv2=input_dict["U2_ptuv2"],
        KPONvnesh_ptuv1=input_dict["KPONvnesh_ptuv1"],
        KPONvnesh_ptuv2=input_dict["KPONvnesh_ptuv2"],
        IA2harm=input_dict["IA2harm"],
        IB2harm=input_dict["IB2harm"],
        IC2harm=input_dict["IC2harm"],
        KZN1neipr=input_dict["KZN1neipr"],
        VNN1vkl=input_dict["VNN1vkl"],
        KZN2neipr=input_dict["KZN2neipr"],
        VNN2vkl=input_dict["VNN2vkl"]
    )
    
    # Сохраняем результаты
    #results.append(list(input_dict.values()) + list(result))
    results.append(list(input_dict.values()) + [int(val) for val in result])
    # Добавление временной задержки между итерациями
    time.sleep(0.01)

# Создаем DataFrame из результатов
df = pd.DataFrame(results, columns=columns)

# Преобразуем логические значения в числовые (0 и 1)
#for col in df.columns:
    #if df[col].dtype == bool:
        #df[col] = df[col].astype(int)

# Сохраняем результаты в файл Excel
output_file = "test_results.xlsx"
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"Результаты сохранены в файл: {output_file}")