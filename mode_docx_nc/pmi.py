from typing import Optional, List  # Для Python 3.8 и ниже
import pathlib
from modes import Modes

class PMI:
    """
    Класс для работы с документацией ПМИ.
    При инициализации загружает все режимы из указанной директории.
    """
    def __init__(self, part_of_modes_dir):

        self._part_of_modes_dir = part_of_modes_dir
        self._part_of_modes_list = []

        self._load_part_of_modes()
    
    def _load_part_of_modes(self):
        """Приватный метод для загрузки режимов из директории"""
        self._part_of_modes_list = []  # Очищаем список перед загрузкой

        # Ищем все поддиректории (игнорируем файлы)
        for mode_dir in self._part_of_modes_dir.iterdir():
            if mode_dir.is_dir() and mode_dir.name.endswith('_modes'):
                try:
                    modes = Modes(mode_dir)
                    self._part_of_modes_list.append(modes)
                    print(f"Загружена группа режимов из: {mode_dir.name}")
                except Exception as e:
                    print(f"Ошибка при загрузке режимов из {mode_dir}: {str(e)}")


    def get_docx(self) -> bytes:
        """
        Генерирует отчет в формате DOCX
        :return: bytes - содержимое файла docx
        :raises: PMIReportError - если генерация не удалась
        """
        # Обязательная реализация
        pass
    
    def get_latex(self) -> Optional[bytes]:
        """
        Генерирует отчет в формате LaTeX (опционально)
        :return: bytes или None, если функционал не реализован
        """
        # Необязательная реализация
        return None

if __name__ == "__main__":

    # автоматическое построение
    current_dir = pathlib.Path(__file__).parent
    part_of_modes_dir = current_dir / "pmi_dzt" 

    pmi = PMI(part_of_modes_dir)