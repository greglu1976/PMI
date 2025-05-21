from iec61850 import IedServer, DataObject, DataAttribute, GoosePublisher
import time

# 1. Создаём виртуальный IED
ied = IedServer("MyIED")

# 2. Создаём Logical Device (LD) и Logical Node (LN)
ld = ied.add_logical_device("LD1")
ln = ld.add_logical_node("LLN0")

# 3. Добавляем DataSet (набор данных для GOOSE)
dataset = ln.add_dataset("dsGOOSE", ["LLN0$ST$Status", "LLN0$Oper$OpCnt"])

# 4. Создаём GOOSE-издатель
goose_pub = GoosePublisher(ied, "eth0")  # Указываем сетевой интерфейс
goose_pub.set_go_id("GOOSE1")  # Идентификатор GOOSE
goose_pub.set_dataset(dataset)  # Привязываем DataSet
goose_pub.set_app_id(1000)      # APPID (должен быть уникальным)

# 5. Запускаем сервер IED
ied.start()

# 6. Периодическая отправка GOOSE
try:
    while True:
        # Обновляем значения в DataSet (можно менять динамически)
        ln.set_value("LLN0$ST$Status", True)
        ln.set_value("LLN0$Oper$OpCnt", 42)
        
        # Отправляем GOOSE
        goose_pub.publish()
        print("GOOSE отправлен!")
        time.sleep(1)  # Период рассылки (1 сек)
except KeyboardInterrupt:
    ied.stop()