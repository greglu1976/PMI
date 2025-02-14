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
SGF1_ptoc1=0, SGF2_ptoc1=0, SGF3_ptoc1=0, SGF4_ptoc1=0, SGF5_ptoc1=0, SGF6_ptoc1=0, SGF7_ptoc1=0, T1_ptoc1=0, Iset_ptoc1=1, Icoarse_ptoc1=2,
SGF1_ptoc2=0, SGF2_ptoc2=0, SGF3_ptoc2=0, SGF4_ptoc2=0, SGF5_ptoc2=0, SGF6_ptoc2=0, SGF7_ptoc2=0, T1_ptoc2=0, Iset_ptoc2=1, Icoarse_ptoc2=2,
SGF1_ptoc3=0, SGF2_ptoc3=0, SGF3_ptoc3=0, SGF4_ptoc3=0, SGF5_ptoc3=0, SGF6_ptoc3=0, SGF7_ptoc3=0, T1_ptoc3=0, Iset_ptoc3=1, Icoarse_ptoc3=2,
SGF1_ptuv1=0, Uop_ptuv1=40, U2op_ptuv1=5,
SGF1_ptuv2=0, Uop_ptuv2=40, U2op_ptuv2=5,
SGF1_phar1=0, Imax_phar1=3, Ratio_phar1=0.4,
)




                    SGF1_ptuv1, Uop_ptuv1, U2op_ptuv1,
                    SGF1_ptuv2, Uop_ptuv2, U2op_ptuv2,
                    SGF1_phar1, Imax_phar1, Ratio_phar1,
                    SGF1_rblc1



# Определяем возможные входные значения для тестирования
input_values = {
    "VYVOD": [0,],
    "OV": [0, ],
    "OVst": [0,],
    "NaSign": [0,],
    "SV1vkl": [0,],
    "SV2vkl": [0,],
    "IA": [2,],
    "IAB": [0,],
    "IB": [0,],
    "IBC": [0,],
    "IC": [0, ],
    "ICA": [0,],
    "BNTpuskA": [0,],
    "BNTpuskB": [0,],
    "BNTpuskC": [0,],
    "KZN1neipr": [0, 1],
    "KPON1pusk": [0, 1],
    "VNN1vkl": [0, 1],
    "KZN2neipr": [0,],
    "KPON2pusk": [0, 1],
    "VNN2vkl": [0, 1]
}

# Генерация всех возможных комбинаций входных значений
import itertools

# Создаем DataFrame для хранения результатов
columns = list(input_values.keys()) + [
    "vvod", "oper_vyvod", "mtzA_pusk", "io_A", "mtzB_pusk", "io_B", "mtzC_pusk", "io_C",
    "gen_pusk", "mtz_srabsign", "mtz_srab", "ET", "kpon_pusk", "set_changer"
]
results = []

# Перебираем все комбинации входных значений
for inputs in itertools.product(*input_values.values()):
    input_dict = dict(zip(input_values.keys(), inputs))
    
    # Вызываем метод Step
    result = lvttoc.Step(
        VYVOD=input_dict["VYVOD"],
        OV=input_dict["OV"],
        OV=input_dict["OV"],
        OVst=input_dict["OVst"],
        NaSign=input_dict["NaSign"],
        SV1vkl=input_dict["SV1vkl"],
        SV2vkl=input_dict["SV2vkl"],
        IA=input_dict["IA"],
        IB=input_dict["IB"],
        IC=input_dict["IC"],
        BNTpuskA=input_dict["BNTpuskA"],
        BNTpuskB=input_dict["BNTpuskB"],
        BNTpuskC=input_dict["BNTpuskC"],
        KZN1neipr=input_dict["KZN1neipr"],
        KPON1pusk=input_dict["KPON1pusk"],
        VNN1vkl=input_dict["VNN1vkl"],
        KZN2neipr=input_dict["KZN2neipr"],
        KPON2pusk=input_dict["KPON2pusk"],
        VNN2vkl=input_dict["VNN2vkl"]
    )
    
    # Сохраняем результаты
    results.append(list(input_dict.values()) + list(result))
    # Добавление временной задержки между итерациями
    time.sleep(0.1)

# Создаем DataFrame из результатов
df = pd.DataFrame(results, columns=columns)

# Сохраняем результаты в файл Excel
output_file = "test_results.xlsx"
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"Результаты сохранены в файл: {output_file}")