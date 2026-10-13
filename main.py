from fastapi import FastAPI, Request

app = FastAPI()

GAME_TEXT = (
    "В игре Сердечки нужно ловить сердца, уворачиваться от пил и побеждать боссов. "
    "Доступны герои Полина, Игорь, Лена, Алина и Богдан. "
    "Поиграть можно на сайте полиночка точка рус!"
)

@app.post("/alice")
async def alice_webhook(request: Request):
    data = await request.json()
    req = data.get("request", {})
    command = req.get("command", "").lower()
    is_new = data.get("session", {}).get("new", False)

    if is_new:
        reply = (
            "Привет! Я знаю всё про игру Сердечки от Артёма. "
            "Спроси меня про героев, режимы игры, боссов или автора!"
        )
    elif any(k in command for k in ["геро", "персонаж", "богдан", "полин", "игор", "лен", "алин"]):
        reply = (
            "В игре 5 героев: Полина со щитом, Игорь с замедлением времени, "
            "Лена восстанавливает жизни, Алина расстреливает пилы, "
            "а Богдан притягивает сердечки магнитом!"
        )
    elif any(k in command for k in ["режим", "босс", "хэллоуин", "правил", "как игра"]):
        reply = (
            "Есть бесконечная классика, спринт на 60 секунд, дуэли до трёх игроков "
            "и битвы с боссами, включая Хэллоуинского короля тыкв!"
        )
    elif any(k in command for k in ["кто создал", "автор", "артём", "милок"]):
        reply = "Игру создал Артём для компании Восемнадцать есть. Сайт — полиночка точка рус."
    else:
        reply = GAME_TEXT + " Спроси про героев или режимы!"

    return {
        "version": data.get("version", "2.0"),
        "session": data.get("session", {}),
        "response": {
            "text": reply,
            "tts": reply,
            "end_session": False
        }
    }
