import time
from lib._TIMERS.TIMERS import TP  # Предполагается, что класс TP у вас в этом модуле

def test_tp():
    T = TP()
    T.set_PT(2)  # Устанавливаем время импульса = 2 секунды

    print("Тест 1: Одиночный импульс при IN=True")
    T.IN = True  # Включаем вход
    start_time = time.monotonic()

    while True:
        out, elapsed_time = T.start()  # Обновляем состояние таймера
        current_time = time.monotonic() - start_time

        print(f"Время: {current_time:.1f} сек | IN: {T.IN} | Q: {out} | ET: {elapsed_time:.1f}")

        if current_time >= 5:  # Завершаем тест через 5 секунд
            break

        time.sleep(0.1)  # Задержка для удобства наблюдения

    print("\nТест 2: Импульс с преждевременным отключением IN")
    T.reset()
    T.set_PT(3)  # Новое время импульса = 3 секунды

    for i in range(50):  # 30 итераций по 0.1 сек = 3 секунды
        T.IN = (i < 10)  # IN=True только первые 10 итераций (1 сек)
        out, elapsed_time = T.start()

        current_time = i * 0.1
        print(f"Время: {current_time:.1f} сек | IN: {T.IN} | Q: {out} | ET: {elapsed_time:.1f}")

        time.sleep(0.1)

if __name__ == "__main__":
    test_tp()