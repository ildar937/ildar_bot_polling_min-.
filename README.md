
# Мини-бот (polling) — @ildarDESIGNBOT

## Как запустить на Render (Background Worker)
1) Создайте новый публичный репозиторий на GitHub (например `ildar_bot_polling_min`).
2) Загрузите файлы из этого проекта (main.py, requirements.txt и папку assets/price.pdf).
3) На Render: **New → Background Worker → Git Provider →** выберите этот репозиторий.
4) Build Command: `pip install -r requirements.txt`
   Start Command: `python main.py`
5) Environment (переменные окружения):
   - `BOT_TOKEN` — токен бота
   - `PDF_PATH` — `assets/price.pdf` (по умолчанию)
   - `MANAGER_CHAT_ID` — добавите после запуска (узнаете командой /id)
6) Deploy. После запуска в Telegram: `/start site`, кнопка «Прайс (PDF)».
7) Узнайте свой ID командой `/id`, запишите его в `MANAGER_CHAT_ID` → Redeploy.

## Локальный запуск
```
pip install -r requirements.txt
export BOT_TOKEN=xxx
python main.py
```

## Примечания
- Это polling-бот — без FastAPI и вебхуков, поэтому работаем как Background Worker.
- Файл прайса лежит в `assets/price.pdf`. Можно заменить своим.
