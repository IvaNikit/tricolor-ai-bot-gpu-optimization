import json    # Импорт модуля для сохранения сгенерированных данных в JSON-файл
import random  # Импорт модуля случайных чисел для рандомизации запросов клиентов
import os      # Импорт модуля OS для проверки наличия конфигурационных файлов

# Функция для безопасной загрузки настроек компании из внешнего конфига
def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)  # Загружаем JSON, если файл существует
    # Возвращаем пустую структуру, если файла нет, чтобы скрипт не упал
    return {"company_name": "Generic", "keywords_responses": [], "products_or_services": []}

# Функция генерации рандомного обезличенного датасета для соблюдения политики конфиденциальности
def generate_dataset(num_samples=50):
    config = load_config()  # Считываем настройки триггеров
    dataset = []            # Список, куда сложатся сгенерированные диалоги
    templates = []          # Базовые шаблоны фраз, которые мы построим на основе конфига
    
    # Собираем шаблоны вопросов на основе ключевых слов-триггеров организации
    for item in config.get("keywords_responses", []):
        for kw in item["keywords"]:
            templates.append(f"Question about {kw}. Help me please.")  # Шаблон с ключевым словом
            
    # Добавляем в шаблоны названия услуг и продуктов компании
    for prod in config.get("products_or_services", []):
        templates.append(f"How to activate {prod}?")  # Шаблон активации услуги
        templates.append(f"Price for {prod} monthly?")  # Шаблон проверки стоимости тарифа

    # Защитный случай: если конфиг пустой, создаем один стандартный шаблон запроса
    if not templates:
        templates = ["Test support request"]

    # Цикл генерации 50 случайных обращений пользователей
    for i in range(num_samples):
        prompt = random.choice(templates)  # Случайно выбираем один из подготовленных шаблонов
        dataset.append({
            "request_id": f"req-{1000 + i}",  # Генерируем уникальный сквозной ID запроса
            "text": prompt,                   # Текст случайного обращения абонента
            "max_tokens": random.randint(64, 256)  # Рандомная длина ответа ИИ в токенах
        })
    return dataset  # Возвращаем заполненный датасет обращений

# Точка входа для запуска записи датасета на диск
if __name__ == "__main__":
    mock_data = generate_dataset(50)  # Запускаем генерацию ровно 50 тестовых диалогов
    # Сохраняем сгенерированный массив в файл mock_dialogues.json с правильной кодировкой
    with open("mock_dialogues.json", "w", encoding="utf-8") as f:
        json.dump(mock_data, f, ensure_ascii=False, indent=4)
    # Печатаем уведомление об успешной генерации данных без нарушения политик компании
    print("[SUCCESS] Dataset 'mock_dialogues.json' successfully generated based on config.json!")
