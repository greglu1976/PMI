import time
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.dimensions import ColumnDimension

from b_MTZ import partOfFsuInTOC

# Создаем экземпляр класса
part = partOfFsuInTOC(SGF1=0, 
SGF1_ptoc1=1, SGF2_ptoc1=0, SGF3_ptoc1=0, SGF4_ptoc1=0, SGF5_ptoc1=1, SGF6_ptoc1=0, SGF7_ptoc1=0, T1_ptoc1=0.23, Iset_ptoc1=3, Icoarse_ptoc1=5,
SGF1_ptoc2=0, SGF2_ptoc2=0, SGF3_ptoc2=0, SGF4_ptoc2=0, SGF5_ptoc2=0, SGF6_ptoc2=0, SGF7_ptoc2=0, T1_ptoc2=0, Iset_ptoc2=1, Icoarse_ptoc2=2,
SGF1_ptoc3=0, SGF2_ptoc3=0, SGF3_ptoc3=0, SGF4_ptoc3=0, SGF5_ptoc3=0, SGF6_ptoc3=0, SGF7_ptoc3=0, T1_ptoc3=0, Iset_ptoc3=1, Icoarse_ptoc3=2,
SGF1_ptuv1=1, Uop_ptuv1=40, U2op_ptuv1=5,
SGF1_ptuv2=0, Uop_ptuv2=40, U2op_ptuv2=5,
SGF1_phar1=0, Imax_phar1=3, Ratio_phar1=0.4,
SGF1_rblc1=0, 
SGF1_lvrbvtr1=0, SGF2_lvrbvtr1=0, u_min_lvrbvtr1=40, u2_max_lvrbvtr1=5, t1_lvrbvtr1=0,
SGF1_lvrbvtr2=0, SGF2_lvrbvtr2=0, u_min_lvrbvtr2=40, u2_max_lvrbvtr2=5, t1_lvrbvtr2=0,
SGF1_ptrc1_tofflvlgc=0, SGF1_rbre1_tofflvlgc=0, SGF2_rbre1_tofflvlgc=0, SGF3_rbre1_tofflvlgc=0, SGF1_rblc1_tofflvlgc=0, SGF2_rblc1_tofflvlgc=0, SGF3_rblc1_tofflvlgc=0,
SGF1_lvalv=0, SGF2_lvalv=0, SGF3_lvalv=0, SGF4_lvalv=0, SGF5_lvalv=0, SGF6_lvalv=0, SGF7_lvalv=0, SGF8_lvalv=0, SGF9_lvalv=0, SGF10_lvalv=0, SGF11_lvalv=0, SGF12_lvalv=0, SGF13_lvalv=0
)

# Определяем возможные входные значения для тестирования

input_values = {
    "VYVOD": [0, ],
    "OV_lvttoc": [0, ],
    "OVst_ptoc1": [0,],
    "OVst_ptoc2": [0,],
    "OVst_ptoc3": [0,],        
    "NaSign_ptoc1": [0,],
    "NaSign_ptoc2": [0,], 
    "NaSign_ptoc3": [0,],       
    "SV1vkl": [0,],
    "SV2vkl": [0,],
    "IA": [1, ],
    "IAB": [5,],
    "IB": [0,],
    "IBC": [0,],
    "IC": [0, ],
    "ICA": [0,],
    "UAB_ptuv1": [50,],
    "UBC_ptuv1": [50,],
    "UCA_ptuv1": [50,],
    "U2_ptuv1": [0, 10],
    "UAB_ptuv2": [0,],
    "UBC_ptuv2": [0,],
    "UCA_ptuv2": [0,],
    "U2_ptuv2": [0, ],
    "KPONvnesh_ptuv1": [0, ],
    "KPONvnesh_ptuv2": [0, ],
    "IA2harm": [0,],
    "IB2harm": [0,],
    "IC2harm": [0,],
    "VNN1vkl": [0,],
    "VNN2vkl": [0,],
    "OV_lvrbvtr1": [0,],
    "vnesh_bnn_srab_lvrbvtr1": [0,],
    "OV_lvrbvtr2": [0,],
    "vnesh_bnn_srab_lvrbvtr2": [0,],
    "OVlot": [0,],    
    "OVlo": [0,],
    "OVzapv": [0,],
    "OVzavr": [0,],           
}

import itertools

# Создаем DataFrame для хранения результатов
columns = list(input_values.keys()) + [
"vvod_lvrbvtr1", "oper_vyvod_lvrbvtr1", "u_lin_pusk_lvrbvtr1", "u2_pusk_lvrbvtr1", "pusk_lvrbvtr1", "neispr_zn_lvrbvtr1", 
        "vvod_lvrbvtr2", "oper_vyvod_lvrbvtr2", "u_lin_pusk_lvrbvtr2", "u2_pusk_lvrbvtr2", "pusk_lvrbvtr2", "neispr_zn_lvrbvtr2",
        "vvod_ptoc1_lvttoc", "oper_vyvod_ptoc1_lvttoc", "mtzA_pusk_ptoc1_lvttoc", "mtzB_pusk_ptoc1_lvttoc", "mtzC_pusk_ptoc1_lvttoc", "gen_pusk_ptoc_lvttoc", "mtz_srabsign_ptoc1_lvttoc", "mtz_srab_ptoc1_lvttoc", "io_A_ptoc1_lvttoc", "io_B_ptoc1_lvttoc", "io_C_ptoc1_lvttoc", "vvod_ptoc2_lvttoc", "oper_vyvod_ptoc2_lvttoc", "mtzA_pusk_ptoc2_lvttoc", "mtzB_pusk_ptoc2_lvttoc", "mtzC_pusk_ptoc2_lvttoc", "gen_pusk_ptoc2_lvttoc", "mtz_srabsign_ptoc2_lvttoc", "mtz_srab_ptoc2_lvttoc", "io_A_ptoc2_lvttoc", "io_B_ptoc2_lvttoc", "io_C_ptoc2_lvttoc", "vvod_ptoc3_lvttoc", "oper_vyvod_ptoc3_lvttoc", "mtzA_pusk_ptoc3_lvttoc", "mtzB_pusk_ptoc3_lvttoc", "mtzC_pusk_ptoc3_lvttoc", "gen_pusk_ptoc3_lvttoc", "mtz_srabsign_ptoc3_lvttoc", "mtz_srab_ptoc3_lvttoc", "io_A_ptoc3_lvttoc", "io_B_ptoc3_lvttoc", "io_C_ptoc3_lvttoc", "kpon_pusk_ptuv1_lvttoc", "kpon_pusk_ptuv2_lvttoc", "ia_start_out_phar1_lvttoc", "ib_start_out_phar1_lvttoc", "ic_start_out_phar1_lvttoc", "start_phar1_lvttoc", "blok_rblc1_lvttoc", "mtz_pusk_lvttoc", "vvod_ptrc1", "oper_vyvod_ptrc1", "pusk_ptrc1", "srab_ptrc1", "vvod_rblc1", "oper_vyvod_rblc1", "zapret_rblc1", "vvod_rbre1", "oper_vyvod_rbre1", "zapret_rbre1", "pusk_lvalv"  
]
results = []

# Перебираем все комбинации входных значений
for inputs in itertools.product(*input_values.values()):
    input_dict = dict(zip(input_values.keys(), inputs))
    
    # Вызываем метод Step
    result = part.Step(
        VYVOD=input_dict["VYVOD"],
        OV_lvttoc=input_dict["OV_lvttoc"],
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
        VNN1vkl=input_dict["VNN1vkl"],
        VNN2vkl=input_dict["VNN2vkl"],
        OV_lvrbvtr1=input_dict["OV_lvrbvtr1"],
        vnesh_bnn_srab_lvrbvtr1=input_dict["vnesh_bnn_srab_lvrbvtr1"],
        OV_lvrbvtr2=input_dict["OV_lvrbvtr2"],
        vnesh_bnn_srab_lvrbvtr2=input_dict["vnesh_bnn_srab_lvrbvtr2"],
        OVlot=input_dict["OVlot"],    
        OVlo=input_dict["OVlo"],
        OVzapv=input_dict["OVzapv"],
        OVzavr=input_dict["OVzavr"],  

    )
    
    # Сохраняем результаты
    results.append(list(input_dict.values()) + [int(val) for val in result])
    time.sleep(0.1)

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
        if cell.value != 0:
            cell.fill = red_fill

# Сохраняем файл
wb.save(output_file)
print(f"Результаты сохранены в файл: {output_file}")