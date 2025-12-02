# Vandalizm Aniqlash Telegram Boti

Bu bot vandalizmni aniqlash va hisobot berish uchun yaratilgan. Bot foydalanuvchilardan rasm, tavsif va geolokatsiya oladi va barcha ma'lumotlarni Telegram kanaliga yuboradi.

## Xususiyatlar

- 📸 Rasm yuborish
- 📝 Tavsif yozish
- 📍 Geolokatsiya yuborish
- 📤 Barcha ma'lumotlarni kanalga avtomatik yuborish
- 🔒 Anonim ishlash (ma'lumotlar saqlanmaydi)

## O'rnatish

1. Kerakli paketlarni o'rnating:
```bash
pip install -r requirements.txt
```

2. `.env` faylini yarating va sozlamalarni kiriting:
```
BOT_TOKEN=your_bot_token_here
CHANNEL_ID=@your_channel_username_or_channel_id
```

## Bot Token olish

1. Telegram'da [@BotFather](https://t.me/BotFather) ga yozing
2. `/newbot` buyrug'ini yuboring
3. Bot nomini va username'ni kiriting
4. Olingan token'ni `.env` fayliga qo'ying

## Kanal ID olish

1. Kanal yarating yoki mavjud kanaldan foydalaning
2. Botni kanalga admin qiling
3. Kanal username'ni yoki ID'ni `.env` fayliga qo'ying
   - Username: `@channel_username`
   - ID: `-1001234567890` (kanal ID'sini olish uchun [@userinfobot](https://t.me/userinfobot) dan foydalaning)

## Ishga tushirish

```bash
python bot.py
```

## Ishlatish

1. Botga `/start` buyrug'ini yuboring
2. Vandalizm haqidagi rasmingizni yuboring
3. Tavsif yozing
4. Geolokatsiyani yuboring
5. Barcha ma'lumotlar kanalga avtomatik yuboriladi

## Eslatma

Bot anonim ishlaydi va hech qanday ma'lumotni saqlamaydi. Barcha ma'lumotlar faqat kanalga yuboriladi va keyin o'chiriladi.

