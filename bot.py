import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BOT_TOKEN = "8314582730:AAEhmVcAJ7fitSKrTXue22d3MYrAY_aPrag"
CHANNEL_ID = "-1003411560221"

if not BOT_TOKEN or not CHANNEL_ID:
    raise ValueError("BOT_TOKEN va CHANNEL_ID muhit o'zgaruvchilarini sozlashingiz kerak!")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# FSM States
class VandalismReport(StatesGroup):
    waiting_for_photo = State()
    waiting_for_description = State()
    waiting_for_location = State()

# Temporary storage (in-memory only, cleared after forwarding)
user_data = {}

@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Botni boshlash"""
    await state.clear()
    user_data[message.from_user.id] = {}
    
    text = (
        "👋 Salom! Eco Andijon botiga xush kelibsiz!\n\n"
        "Bot sizga yordam beradi:\n"
        "1️⃣ Rasm oling va yuboring\n"
        "2️⃣ Tavsif yozing\n"
        "3️⃣ Joylashuv yuboring\n\n"
        "📸 Iltimos rasmingizni yuboring:"
    )
    
    await message.answer(text)
    await state.set_state(VandalismReport.waiting_for_photo)

@dp.message(VandalismReport.waiting_for_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    """Rasmni qabul qilish"""
    user_id = message.from_user.id
    
    # Eng yuqori sifatli rasmni olish
    photo = message.photo[-1]
    file_id = photo.file_id
    
    # Foydalanuvchi ma'lumotlarini saqlash (vaqtinchalik)
    if user_id not in user_data:
        user_data[user_id] = {}
    
    user_data[user_id]['photo_id'] = file_id
    user_data[user_id]['photo_file_unique_id'] = photo.file_unique_id
    
    await message.answer(
        "✅ Rasm qabul qilindi!\n\n"
        "📝 Iltimos, vandalizm haqida batafsil tavsif yozing:"
    )
    await state.set_state(VandalismReport.waiting_for_description)

@dp.message(VandalismReport.waiting_for_photo)
async def process_photo_invalid(message: Message):
    """Noto'g'ri rasm"""
    await message.answer(
        "❌ Iltimos, rasm yuboring!\n\n"
        "📸 Rasmingizni yuboring:"
    )

@dp.message(VandalismReport.waiting_for_description, F.text)
async def process_description(message: Message, state: FSMContext):
    """Tavsifni qabul qilish"""
    user_id = message.from_user.id
    
    if user_id not in user_data:
        await message.answer(
            "❌ Xatolik yuz berdi. /start buyrug'i bilan qayta boshlang."
        )
        await state.clear()
        return
    
    user_data[user_id]['description'] = message.text
    
    await message.answer(
        "✅ Tavsif qabul qilindi!\n\n"
        "📍 Iltimos, vandalizm joylashgan joyni yuboring (geolokatsiya):"
    )
    await state.set_state(VandalismReport.waiting_for_location)

@dp.message(VandalismReport.waiting_for_description)
async def process_description_invalid(message: Message):
    """Noto'g'ri tavsif"""
    await message.answer(
        "❌ Iltimos, matn ko'rinishida tavsif yozing!\n\n"
        "📝 Tavsifingizni yozing:"
    )

@dp.message(VandalismReport.waiting_for_location, F.location)
async def process_location(message: Message, state: FSMContext):
    """Geolokatsiyani qabul qilish va kanalga yuborish"""
    user_id = message.from_user.id
    
    if user_id not in user_data:
        await message.answer(
            "❌ Xatolik yuz berdi. /start buyrug'i bilan qayta boshlang."
        )
        await state.clear()
        return
    
    location = message.location
    user_data[user_id]['latitude'] = location.latitude
    user_data[user_id]['longitude'] = location.longitude
    
    # Kanalga yuborish
    try:
        # Rasmni yuborish
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=user_data[user_id]['photo_id'],
            caption=(
                f"📝 Tavsif:\n{user_data[user_id]['description']}\n\n"
                f"📍 Joylashuv:\n"
                f"Google maps: https://www.google.com/maps/search/?api=1&query={user_data[user_id]['latitude']},{user_data[user_id]['longitude']}\n"
                f"Yandex maps: https://yandex.com/maps/?ll={user_data[user_id]['longitude']},{user_data[user_id]['latitude']}&z=16"
            )
        )
        
        # Geolokatsiyani yuborish
        await bot.send_location(
            chat_id=CHANNEL_ID,
            latitude=user_data[user_id]['latitude'],
            longitude=user_data[user_id]['longitude']
        )
        
        await message.answer(
            "✅ Muvaffaqiyatli!\n\n"
            "📤 Barcha ma'lumotlar yuborildi.\n\n"
            "Yana bir hisobot yuborish uchun /start buyrug'ini bosing."
        )
        
    except Exception as e:
        logger.error(f"Kanalga yuborishda xatolik: {e}")
        await message.answer(
            "❌ Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring."
        )
    finally:
        # Ma'lumotlarni o'chirish (anonimlik)
        if user_id in user_data:
            del user_data[user_id]
        await state.clear()

@dp.message(VandalismReport.waiting_for_location)
async def process_location_invalid(message: Message):
    """Noto'g'ri geolokatsiya"""
    await message.answer(
        "❌ Iltimos, geolokatsiya yuboring!\n\n"
        "📍 Joylashuvni yuborish uchun 📎 tugmasini bosing va 'Joylashuv' ni tanlang:"
    )

@dp.message()
async def handle_other_messages(message: Message):
    """Boshqa xabarlarni qayta ishlash"""
    await message.answer(
        "🤖 Botni ishga tushirish uchun /start buyrug'ini bosing."
    )

async def main():
    """Botni ishga tushirish"""
    logger.info("Bot ishga tushmoqda...")
    # Webhookni o'chirish (polling uchun zarur)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook o'chirildi, polling ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

