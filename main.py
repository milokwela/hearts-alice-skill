from fastapi import FastAPI, Request

app = FastAPI()

GAME_TEXT = (
    "В игре Сердечки нужно ловить сердца, уворачиваться от пил и побеждать боссов. "
    "Доступны герои Полина, Игорь, Лена, Алина и Богдан. "
    "Поиграть можно на сайте полиночка точка рус!"
)

SUGGEST_BUTTONS = [
    {"title": "Герои", "hide": True},
    {"title": "Режимы игры", "hide": True},
    {"title": "Кто создал игру?", "hide": True},
    {"title": "Выход", "hide": True},
]

# Чтобы сервер не спал и отвечал 200 OK на любые проверки
@app.get("/")
@app.get("/alice")
async def health_check():
    return {"status": "ok"}

@app.post("/alice")
async def alice_webhook(request: Request):
    data = await request.json()
    req = data.get("request", {})
    command = req.get("command", "").lower().strip()
    is_new = data.get("session", {}).get("new", False)

    end_session = False
    buttons = SUGGEST_BUTTONS

    # 1. Приветствие при старте
    if is_new:
        reply = (
            "Привет! Я знаю всё про игру Сердечки от Артёма. "
            "Спроси меня про героев, режимы игры, боссов или автора!"
        )

    # 2. Обязательный выход по правилам модерации Яндекса
    elif any(k in command for k in ["хватит", "выход", "пока", "стоп", "закрой"]):
        reply = "До встречи! Заходи играть в Сердечки на сайте полиночка точка рус!"
        end_session = True
        buttons = []

    # 3. Вопросы про персонажей
    elif any(k in command for k in ["геро", "персонаж", "богдан", "полин", "игор", "лен", "алин"]):
        reply = (
            "В игре 5 героев: Полина со щитом, Игорь с замедлением времени, "
            "Лена восстанавливает жизни, Алина расстреливает пилы, "
            "а Богдан притягивает сердечки магнитом!"
        )

    # 4. Режимы игры и правила
    elif any(k in command for k in ["режим", "босс", "хэллоуин", "правил", "как игра"]):
        reply = (
            "Есть бесконечная классика, спринт на 60 секунд, дуэли до трёх игроков "
            "и битвы с боссами, включая Хэллоуинского короля тыкв!"
        )

    # 5. Создатель и игра
    elif any(k in command for k in ["кто создал", "автор", "артём", "милок", "создател"]):
        reply = "Игру Сердечки создал Артём. В неё можно сыграть на сайте полиночка точка рус!"

    # 6. Ответ по умолчанию
    else:
        reply = GAME_TEXT + " Спроси про героев или режимы!"

    return {
        "version": data.get("version", "2.0"),
        "response": {
            "text": reply,
            "tts": reply,
            "buttons": buttons,
            "end_session": end_session
        }
    }
