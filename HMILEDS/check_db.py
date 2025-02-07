import redis

def check_redis(host='192.168.11.49', port=6379):
    try:
        # Подключаемся к Redis-серверу
        r = redis.Redis(host=host, port=port, decode_responses=True)

        # Проверяем статус сервера
        if r.ping():
            print("Redis-сервер доступен и работает!")
            # Выполним тестовую команду, чтобы убедиться, что сервер отвечает
            r.set("test_key", "Hello, Redis!")
            print("Тестовое значение успешно установлено:", r.get("test_key"))
        else:
            print("Не удалось подключиться к Redis-серверу.")
    
    except redis.ConnectionError:
        print("Не удалось подключиться к Redis-серверу. Проверьте адрес и порт.")
    except Exception as e:
        print("Произошла ошибка:", str(e))

# Вызов функции, передайте IP-адрес и порт вашего Redis-сервера
check_redis(host='192.168.11.49', port=6379)  # Замените на IP-адрес вашего сервера
