import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8951559500:AAEO-zEeUmgabpQWmIs7aFigeXEOFIFfGSU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Murojaat holati uchun FSM
class MurojaatState(StatesGroup):
    waiting_for_text = State()

# Rasmiy asosiy menyu tugmalari
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Murojaat yuborish"), KeyboardButton(text="📞 Bog‘lanish")],
        [KeyboardButton(text="📍 Manzilimiz"), KeyboardButton(text="ℹ️ Texnikum haqida")]
    ],
    resize_keyboard=True
)

# /start komandasi (Rasmiy kutib olish)
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    text = (
        "🏢 <b>Paxtaobod tuman 1-son texnikumi</b>\n\n"
        "Rasmiy murojaatlar botiga xush kelibsiz!\n\n"
        "Kerakli bo'limni tanlang:"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu)

# "Murojaat yuborish" tugmasi bosilganda
@dp.message(F.text == "📝 Murojaat yuborish")
async def ask_murojaat(message: types.Message, state: FSMContext):
    text = (
        "✍️ <b>Murojaat yuborish tartibi:</b>\n\n"
        "Murojaatingiz, taklifingiz yoki shikoyatingizni batafsil yozib yuboring. "
        "Xabaringiz belgilangan tartibda mas’ul xodimlarga yetkaziladi."
    )
    await message.answer(text, parse_mode="HTML")
    await state.set_state(MurojaatState.waiting_for_text)

# Murojaat matnini qabul qilish
@dp.message(MurojaatState.waiting_for_text)
async def process_murojaat(message: types.Message, state: FSMContext):
    await message.answer(
        "✅ Murojaatingiz muvaffaqiyatli qabul qilindi.\n"
        "O'rnatilgan tartibda ko'rib chiqilib, tez orada javob qaytariladi.",
        reply_markup=main_menu
    )
    await state.clear()

# "Bog'lanish" bo'limi (Siz ko'rsatgan raqam bilan)
@dp.message(F.text == "📞 Bog‘lanish")
async def contact_us(message: types.Message):
    text = (
        "📞 <b>Biz bilan bog'lanish:</b>\n\n"
        "• Ishonch telefoni: <code>+998 93 671 06 01</code>\n"
        "• Murojaatlar uchun mas'ul bo'lim\n"
        "• Ish vaqti: Dushanba — Shanba (08:00 dan 17:00 gacha)"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu)

# "Manzilimiz" bo'limi
@dp.message(F.text == "📍 Manzilimiz")
async def location_us(message: types.Message):
    text = (
        "📍 <b>Texnikum manzili:</b>\n\n"
        "Andijon viloyati, Paxtaobod tumani.\n"
        "1-son texnikumi binosi."
    )
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu)

# "Texnikum haqida" bo'limi
@dp.message(F.text == "ℹ️ Texnikum haqida")
async def about_us(message: types.Message):
    text = (
        "ℹ️ <b>Paxtaobod tuman 1-son texnikumi haqida:</b>\n\n"
        "Texnikumimiz yoshlarga zamonaviy kasb-hunarlar, "
        "texnologiyalar va xorijiy tillarni o'rgatish hamda ularni "
        "malakali mutaxassis qilib tayyorlashga ixtisoslashgan."
    )
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())