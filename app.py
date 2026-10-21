import time  # Импорт библиотеки для работы со временем и задержками
import json  # Импорт библиотеки для работы с форматом данных JSON
import os    # Импорт библиотеки для работы с операционной системой и путями
from contextlib import asynccontextmanager  # Инструмент для управления жизненным циклом сервера
from fastapi import FastAPI, Form            # FastAPI для создания API и Form для обработки полей
from fastapi.responses import PlainTextResponse  # PlainTextResponse для вывода чистого текста без скобок

COMPANY_CONFIG = {}  # Глобальный словарь, куда загрузятся настройки из config.json

# Фоновый менеджер, который срабатывает строго при старте и выключении веб-сервера
@asynccontextmanager
async def lifespan(app: FastAPI):
    global COMPANY_CONFIG
    config_path = "config.json"  # Указываем имя нашего файла конфигурации
    
    # Проверяем, существует ли файл и не пустой ли он
    if os.path.exists(config_path) and os.path.getsize(config_path) > 0:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                COMPANY_CONFIG = json.load(f)  # Считываем конфигурацию компании
            print("Configuration loaded successfully.")  # Отмашка в консоль, что данные подгрузились
        except Exception:
            # Резервный вариант настроек, если файл config.json поврежден
            COMPANY_CONFIG = {"company_name": "Tricolor", "default_response": "Error loading configuration."}
    else:
        # Резервный вариант, если файла config.json вообще нет в папке
        COMPANY_CONFIG = {
            "company_name": "Tricolor Default",
            "keywords_responses": [],
            "default_response": "Config empty."
        }
    yield  # В этой точке сервер начинает принимать запросы от пользователей
    COMPANY_CONFIG.clear()  # Очищаем память от настроек при плановой остановке сервера

# Инициализируем само веб-приложение FastAPI с привязкой фонового менеджера lifespan
app = FastAPI(title="Tricolor AI Chatbot API", lifespan=lifespan)

# Создаем POST-эндпоинт чата, который принимает данные формы и возвращает чистый текст
@app.post("/api/v1/chat", response_class=PlainTextResponse)
async def process_chat_message(
    user_info: str = Form(..., description="Enter your ID and Name", example="Ivan, ID: 777"),  # Поле для ввода ID
    message: str = Form(..., description="Enter your question", example="error")  # Поле для ввода вопроса ИИ
):
    time.sleep(0.45)  # Архитектурная симуляция сверхбыстрого ответа LLM нейросети на GPU Tensor Cores
    msg_lower = message.lower()  # Принудительно переводим вопрос в нижний регистр для точного поиска
    bot_answer = None  # Сюда запишется финальный ответ ИИ-робота
    
    # Цикл перебора ключевых слов-триггеров из файла конфигурации config.json
    for item in COMPANY_CONFIG.get("keywords_responses", []):
        # Если хотя бы одно ключевое слово из списка есть в вопросе пользователя
        if any(kw.lower() in msg_lower for kw in item["keywords"]):
            bot_answer = item["bot_answer"]  # Присваиваем боту соответствующий готовый ответ
            break  # Выходим из цикла поиска, так как совпадение найдено
            
    # Если совпадений с триггерами не нашлось, выдаем стандартный ответ поддержки
    if not bot_answer:
        bot_answer = COMPANY_CONFIG.get("default_response", "Request processed.")
        
    # Формируем итоговый текстовый интерфейс ответа без каких-либо фигурных скобок и кавычек
    final_text = (
        f"Please write your ID and Name: {user_info}\n\n"  # Строка с требованием ввести ID/Имя
        f"AI Assistant [{COMPANY_CONFIG.get('company_name', 'Tricolor')}]: {bot_answer}"  # Строка с ответом ИИ
    )
    return final_text  # Отправляем плоский текст обратно в интерфейс браузера

# Запуск сервера uvicorn локально на хосте 127.0.0.1 и порту 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000)  # Запуск приложения без reload для стабильности потоков Windows