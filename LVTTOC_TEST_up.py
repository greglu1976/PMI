import time
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.dimensions import ColumnDimension
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
    results.append(list(input_dict.values()) + [int(val) for val in result])
    time.sleep(0.01)

# Создаем DataFrame из результатов
df = pd.DataFrame(results, columns=columns)

# Создаем Excel-файл
output_file = "test_results.xlsx"
wb = Workbook()
ws = wb.active

# Записываем данные в Excel
for r in dataframe_to_rows(df, index=False, header=True):
    ws.append(r)

# Устанавливаем ширину столбцов
for col in ws.columns:
    column_letter = col[0].column_letter
    ws.column_dimensions[column_letter].width = 20  # Ширина столбца 15

# Определяем красный цвет для заливки
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

# Применяем условное форматирование для выделения значений '1' красным цветом
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
    for cell in row:
        if cell.value == 1:
            cell.fill = red_fill

# Сохраняем файл
wb.save(output_file)
print(f"Результаты сохранены в файл: {output_file}")