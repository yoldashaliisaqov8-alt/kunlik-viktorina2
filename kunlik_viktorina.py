# -*- coding: utf-8 -*-
"""Har kuni kanalga bitta viktorina (tugmasi bilan) yuboradi.
Railway Cron orqali har kuni 08:00 (Toshkent) da ishga tushadi va ishini tugatib to'xtaydi."""
import os, json, datetime, requests

TOKEN = os.environ.get("BOT_TOKEN", "BOT_TOKENINGIZ")
KANAL = os.environ.get("KANAL", "@yoldashaliisakov")
BOSHLANISH = datetime.date(2026, 11, 12)          # 1-savol shu kuni chiqadi
TUGMA_MATNI = os.environ.get("TUGMA_MATNI", "📚 Yana 2400+ test — bepul")
TUGMA_HAVOLA = os.environ.get("TUGMA_HAVOLA", "https://t.me/ilm_testi_bot")

papka = os.path.dirname(os.path.abspath(__file__))
savollar = json.load(open(os.path.join(papka, "savollar.json"), encoding="utf-8"))

bugun = (datetime.datetime.utcnow() + datetime.timedelta(hours=5)).date()   # Toshkent vaqti
raqam = (bugun - BOSHLANISH).days % len(savollar)
s = savollar[raqam]

data = {
    "chat_id": KANAL,
    "question": "❓ " + s["savol"],
    "options": json.dumps([{"text": v} for v in s["variantlar"]], ensure_ascii=False),
    "type": "quiz",
    "correct_option_id": s["togri"],
    "is_anonymous": True,
    "explanation": s.get("izoh", ""),
    "reply_markup": json.dumps({"inline_keyboard": [[{"text": TUGMA_MATNI, "url": TUGMA_HAVOLA}]]}, ensure_ascii=False),
}
javob = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPoll", data=data, timeout=30).json()
print(bugun, "savol #", raqam + 1, "->", "OK" if javob.get("ok") else javob.get("description"))
