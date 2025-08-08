
import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

TOKEN = os.getenv("BOT_TOKEN", "").strip()
MANAGER_CHAT_ID = int(os.getenv("MANAGER_CHAT_ID", "0") or 0)
PDF_PATH = os.getenv("PDF_PATH", "assets/price.pdf")

bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher()

def kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Прайс (PDF)", callback_data="price")],
        [InlineKeyboardButton(text="Оставить заявку", callback_data="lead")],
    ])

@dp.message(CommandStart())
async def start(m: Message):
    payload = ""
    if m.text and " " in m.text:
        payload = m.text.split(" ", 1)[1].strip()
    src = payload or "direct"
    await m.answer(f"Привет, {m.from_user.full_name}! Я помогу с AI-дизайном.\nИсточник: <b>{src}</b>", reply_markup=kb())
    if MANAGER_CHAT_ID:
        await bot.send_message(MANAGER_CHAT_ID, f"🆕 @{m.from_user.username or '—'} · {m.from_user.full_name} · <code>{m.from_user.id}</code> · src={src}")

@dp.message(Command("id"))
async def my_id(m: Message):
    await m.answer(f"Ваш chat_id: <code>{m.from_user.id}</code>")

@dp.message(Command("price"))
async def price_cmd(m: Message):
    try:
        await m.answer_document(FSInputFile(PDF_PATH), caption="Прайс и кейсы (PDF)")
    except Exception:
        await m.answer("Прайс недоступен. Проверьте PDF_PATH на сервере.")

@dp.callback_query(F.data == "price")
async def cb_price(c):
    await c.answer()
    try:
        await c.message.answer_document(FSInputFile(PDF_PATH), caption="Прайс и кейсы (PDF)")
    except Exception:
        await c.message.answer("Прайс недоступен.")

@dp.callback_query(F.data == "lead")
async def cb_lead(c):
    await c.answer()
    await c.message.answer("Опиши задачу, желаемый стиль и срок. Можно прикрепить 1–2 фото.")

@dp.message(F.photo | F.text)
async def relay(m: Message):
    if not MANAGER_CHAT_ID:
        return
    await bot.send_message(MANAGER_CHAT_ID, f"✉️ @{m.from_user.username or '—'} · {m.from_user.full_name} · <code>{m.from_user.id}</code>")
    await m.forward(MANAGER_CHAT_ID)

async def main():
    assert TOKEN, "Установите переменную окружения BOT_TOKEN"
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
