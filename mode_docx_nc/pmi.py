from typing import Optional, List  # Для Python 3.8 и ниже

from mode import Mode

class PMI:
    """
    Класс для работы с документацией ПМИ.
    При инициализации загружает все режимы из указанной директории.
    """
    def __init__(self, modes_directory: str):
        """
        :param modes_directory: путь к директории с файлами режимов (.xlsx)
        """
        self._modes = self._load_modes(modes_directory)  # список объектов Mode
    
    def _load_modes(self, directory: str) -> List['Mode']:
        """Приватный метод для загрузки режимов из директории"""
        # Реализация загрузки и парсинга xlsx файлов
        # Возвращает список объектов Mode
        pass
    
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