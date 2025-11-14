# Telegram Reminder Bot

Oddiy aiogram + APScheduler asosida qurilgan eslatma bot. Bot guruhga qo‘shilganda chat ID ni avtomatik saqlaydi va har kuni 08:00, 08:30, 09:00 da xabar yuboradi.

## Loyiha tuzilmasi
- `bot.py` – aiogram bot, handlerlar, scheduler ishga tushirilishi
- `scheduler.py` – APScheduler triggerlari va eslatma yuborish vazifasi
- `storage.py` – chat ID larni JSON faylga saqlash/oqish
- `config.py` – sozlamalar, token, timezone, matnlar
- `data/groups.json` – guruh ID lar saqlanadigan fayl (auto yaratiladi)
- `requirements.txt` – zarur Python kutubxonalari
- `.env` (ixtiyoriy) – `BOT_TOKEN` va `TIMEZONE` ni yashirin saqlash

## O‘rnatish
```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt
```

`.env` fayl yarating:
```
BOT_TOKEN=123456:ABCDEF
TIMEZONE=Asia/Tashkent  # yoki kerakli tz nomi
```

## Ishga tushirish
```bash
python bot.py
```

Botni guruhga qo‘shganingizda `my_chat_member` hodisasi orqali `chat_id` olinadi va `data/groups.json` ichiga yoziladi. Har safar scheduler shu fayldagi barcha chatlarga xabar yuboradi.

## Chat ID qanday olinadi?
- Aiogram `@dp.my_chat_member` handler ini tinglaydi.
- Bot guruhga qo‘shilganda `event.chat.id` olinadi.
- `storage.py` yordamida ID JSON faylga yoziladi.

## Scheduler qanday ishlaydi?
- `scheduler.py` ichida `setup_scheduler` funksiyasi APScheduler yaratadi.
- Har bir vaqt (`08:00`, `08:30`, `09:00`) uchun alohida `CronTrigger`.
- Bot jarayoni ishlayotgan paytda scheduler ham doimiy ishlaydi va xabar yuboradi.

## Vaqt zonasi (UTC ↔ GMT+5)
- Default `TIMEZONE = Asia/Tashkent (GMT+5)`.
- Agar server UTC bo‘lsa ham, aynan shu timezone ni o‘rnating – cron triggerlar lokal vaqtga mos keladi.
- Agar UTC’da ish tutsangiz, `TIMEZONE=UTC` deb yozib, `REMINDER_TIMES` ni UTC ga mos qiymatlarga o‘zgartiring (masalan 03:00, 03:30, 04:00).

## Deploy bo‘yicha qisqa ko‘rsatma
1. Serverda kodni ko‘chirib oling (`git clone` yoki SCP).
2. Virtual muhit yarating va `pip install -r requirements.txt`.
3. `.env` faylga `BOT_TOKEN` qo‘ying.
4. `python bot.py` bilan test qiling.
5. Uzoq muddatli ishlashi uchun:
   - **systemd**: `ExecStart=/path/to/venv/bin/python /path/to/bot.py`, `Restart=always`.
   - **Docker**: `python:3.11` bazasi, requirements install, `CMD ["python","bot.py"]`, `--restart unless-stopped`.

Bot faqat eslatma yuboradi – tugma yo‘q, tashqi ilovalarga yo‘naltirmaydi, davomat olib bormaydi.