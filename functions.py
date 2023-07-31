import logging

from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, ContextTypes, CommandHandler,
                          CallbackQueryHandler, CallbackContext)

from config import (TOKEN, SELFIE, HIGH_SCHOOL_PHOTO, ABOUT_HOBBY,
                    TEXT_LIST, REPO, GPT, SQL, LOVE_STORY)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# ОБРАБОТКА КОМАНД МЕНЮ #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает команду старт"""
    user = update.effective_user
    text = (f"Привет, {user.first_name}! Я бот, который поможет тебе "
            "лучше узнать челокека, который меня разработал. Ниже кнопки с "
            "доступными коммандами,а также ты можешь "
            "использовать текстовые команды.")
    await update.message.reply_text(text,
                                    reply_markup=get_main_menu_keyboard())


async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает команду старт"""
    await update.message.reply_text('Выберите команду\n',
                                    reply_markup=get_main_menu_keyboard())


# ОБРАБОТКА КОМАНД МЕНЮ #

# ОБРАБОТКА КНОПОЧНЫХ КОММАНД #

async def get_text(query, choice) -> None:
    """Отправляет текст"""
    print('get_text')
    if choice == str(REPO):
        await query.message.reply_text(
            f"Ссылка на репозиторий:\n {TEXT_LIST['repo']}")
        return
    await query.message.reply_text(TEXT_LIST['hobby'])


async def get_photo(query, choice) -> None:
    """Отправляет фотографию"""
    print('get_photo')
    if choice == str(SELFIE):
        await query.message.reply_photo(open('images/selfie.jpeg', 'rb'))
        return
    await query.message.reply_photo(open(
        'images/high_school_photo.jpeg', 'rb'))


async def get_voice(query, choice) -> None:
    """Отправляет звуковую запись"""
    print('get_voice')
    if choice == str(GPT):
        audio_file_path = 'voices/gpt.mp3'
    elif choice == str(SQL):
        audio_file_path = 'voices/sql_vs_nosql.mp3'
    else:
        audio_file_path = 'voices/love_story.mp3'
    try:
        await query.message.reply_audio(audio=audio_file_path)
        logger.info(
            "Аудиосообщение успешно отправлено пользователю """
            f"{query.message.chat_id}.")
    except Exception as e:
        logger.error(f"Ошибка при отправке аудиосообщения: {e}")


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Последнее селфи",
                              callback_data=str(SELFIE))],
        [InlineKeyboardButton("Фото из старшей школы",
                              callback_data=str(HIGH_SCHOOL_PHOTO))],
        [InlineKeyboardButton("Пост о главном увлечении",
                              callback_data=str(ABOUT_HOBBY))],
        [InlineKeyboardButton("Получить ссылку на репозиторий",
                              callback_data=str(REPO))],
        [InlineKeyboardButton("Аудио.Рассказ о GPT",
                              callback_data=str(GPT))],
        [InlineKeyboardButton("Аудио.Разница между SQL и NoSQL",
                              callback_data=str(SQL))],
        [InlineKeyboardButton("Аудио.История первой любви",
                              callback_data=str(LOVE_STORY))],
    ]
    return InlineKeyboardMarkup(keyboard)


async def handle_buttons(update: Update, _: CallbackContext) -> None:
    """"Обрабатывает нажатия на кнопки"""
    query = update.callback_query

    if query.data == str(SELFIE) or query.data == str(HIGH_SCHOOL_PHOTO):
        await get_photo(query, query.data)
    elif (query.data == str(GPT) or query.data == str(SQL)
          or query.data == str(LOVE_STORY)):
        await get_voice(query, query.data)
    elif query.data == str(REPO) or query.data == str(ABOUT_HOBBY):
        await get_text(query, query.data)


# ОБРАБОТКА КНОПОЧНЫХ КОММАНД #

# ГЛАВНЫЙ ОБРАБОТЧИК ВХОДЯЩИХ СООБЩЕНИЙ #
def handle_incoming_message() -> None:
    """Обработывает входящие сообщения."""

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("commands", commands))
    application.add_handler(CallbackQueryHandler(handle_buttons))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
