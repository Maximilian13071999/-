from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.markdown import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

storage = MemoryStorage()

bot = Bot(token="5644768745:AAGOrfSr-ZI62Dylu6PXVgp4IBXBDFEf70U")
dp = Dispatcher(bot, storage=storage)

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

@dp.message_handler(commands=["Загрузить"], state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply("Загрузи фото")

@dp.message_handler(content_types=["photo"], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply("Теперь введи название")

btn1 = KeyboardButton("копатыч")
btn2 = KeyboardButton("ананас")
btn3 = KeyboardButton("котик")

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.row(btn1, btn2)
kb.row(btn3)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Выберите, что вы хотите?", reply_markup=kb)

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def echo_photo(message: types.Message):
    await bot.send_photo(message.chat.id,
                             photo=message.photo[-1].file_id)

@dp.message_handler(content_types=types.ContentTypes.VIDEO)
async def echo_photo(message: types.Message):
    await bot.send_video(message.chat.id,
                             video=message.video.file_id)

@dp.message_handler()
async def talk(message: types.Message):
    if message.text == "кабачок":
        await bot.send_photo(message.chat.id,
                             photo='https://vasha-teplitsa.ru/wp-content/uploads/2019/07/post_5d1d738048620.jpg')
    if message.text.lower() == "драйв":
        await bot.send_photo(message.chat.id, photo=types.InputFile(path_or_bytesio="drive_12.jpg"))

    if message.text.lower() == "котик":
        await bot.send_video(message.chat.id,
                video=types.InputFile(path_or_bytesio="video.mp4"))

    if message.text.lower() == "документ":
        await message.answer_document(open("важный документ.txt", "rb"))

    if message.text.lower() == "копатыч":
        await bot.send_sticker(message.chat.id,
                               "CAACAgIAAxkBAAEEu4digSYsTe3ixUyzM_-7eR_KlZm4cAACPgAD-tTmHXcIvh2LmyxyJAQ")
    if message.text.lower() == "ананас":
        await message.answer("<i>Я бот</i>, а не <b>ананас</b>", parse_mode="HTML")
    if message.text.lower() == "тест":
        await message.answer("<i>курсивный</i>", parse_mode="HTML")


        await message.answer("<b>жирный</b>", parse_mode="HTML")


        await message.answer("<a href='vk.com'>ссылка</a>", parse_mode="HTML")
        await message.answer("<code>if a = 500</code>", parse_mode="HTML")
        await message.answer("<del>секретная информация</del>", parse_mode="HTML")
        await message.answer("<u>секретная информация</u>", parse_mode="HTML")


executor.start_polling(dp, skip_updates=True)
