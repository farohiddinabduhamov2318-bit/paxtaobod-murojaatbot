import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web

TOKEN = "8951559500:AAEO-zEeUmgabpQWmIs7aFigeXEOFIFfGSU"
ADMIN_ID = 8140009811  # Sizning Admin ID raqamingiz

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

# /start komandasi
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    text = (
        "<b>Bu bot nimalar qila oladi?</b>\n"
        "Paxtaobod tumani 1-son texnikumining murojaatlar bilan ishlash uchun yaratilgan rasmiy murojaat boti.\n\n"
        "<b>XURMALI O'QUVCHI YOSHLAR!</b> Sizda o'quv jarayoni, korrupsion holatlar, "
        "guruh rahbari faoliyati, dars sifati va samaradorligi, kutubxona faoliyati, "
        "texnikum moddiy-texnik bazasi va boshqa savollar yoki muammolar bo'lsa, "
        "texnikum rasmiy botiga murojaat yuboring.\n\n"
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

# Murojaat matnini qabul qilib adminga yuborish
@dp.message(MurojaatState.waiting_for_text)
async def process_murojaat(message: types.Message, state: FSMContext):
    user_name = message.from_user.full_name
    user_username = f"@{message.from_user.username}" if message.from_user.username else "Username yo'q"
    murojaat_matni = message.text

    admin_xabari = (
        "📨 <b>Yangi murojaat keldi!</b>\n\n"
        f"👤 <b>Kimdan:</b> {user_name} ({user_username})\n"
        f"🆔 <b>ID:</b> <code>{message.from_user.id}</code>\n\n"
        f"💬 <b>Murojaat matni:</b>\n{murojaat_matni}"
    )
    
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=admin_xabari, parse_mode="HTML")
    except Exception as e:
        print(f"Adminga yuborishda xato: {e}")

    await message.answer(
        "✅ Murojaatingiz muvaffaqiyatli qabul qilindi va mas'ul xodimlarga yuborildi.\n"
        "O'rnatilgan tartibda ko'rib chiqilib, tez orada javob qaytariladi.",
        reply_markup=main_menu
    )
    await state.clear()

# Admindan kelgan javobni foydalanuvchiga yo'naltirish
@dp.message(F.from_user.id == ADMIN_ID)
async def admin_reply(message: types.Message):
    if message.reply_to_message:
        reply_text = message.reply_to_message.text
        try:
            if "🆔 ID:" in reply_text:
                for line in reply_text.split("\n"):
                    if "🆔 ID:" in line:
                        target_user_id = int(line.replace("🆔 ID:", "").replace("<code>", "").replace("</code>", "").strip())
                        
                        await bot.send_message(
                            chat_id=target_user_id,
                            text=f"💬 <b>Texnikum ma'muriyatidan javob:</b>\n\n{message.text}",
                            parse_mode="HTML"
                        )
                        await message.reply("✅ Javob foydalanuvchiga muvaffaqiyatli yuborildi!")
                        return
        except Exception as e:
            await message.reply(f"❌ Xatolik yuz berdi: {e}")

# "Bog'lanish" bo'limi
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

# Render uchun soxta veb-server (24/7 ishlashi uchun)
async def handle(request):
    return web.Response(text="Bot ishlayapti!")

app = web.Application()
app.router.add_get("/", handle)

async def web_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

async def main():
    await web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
