import logging
import re
import speech_recognition as sr

from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, ContextTypes, CommandHandler,
                          CallbackQueryHandler, CallbackContext,
                          MessageHandler, filters)
from pydub import AudioSegment

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


async def handle_text_or_voice_message(update: Update,
                                       context: CallbackContext) -> None:
    """Обрабатывает текстовые и голосовые сообщения."""
    if update.message.text:
        text = update.message.text.lower()
    elif update.message.voice:
        # ffmpeg_path = which("ffmpeg")
        # AudioSegment.converter = ffmpeg_path

        voice = update.message.voice
        file = await context.bot.get_file(voice.file_id)

        # Download the audio file using the 'download_to_drive' method
        file_path = "voice.ogg"
        await file.download_to_drive(custom_path=file_path)

        # Конвертируем в формат WAV
        wav_file_path = "voice.wav"
        AudioSegment.from_ogg(file_path).export(wav_file_path, format="wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile('voice.wav') as source:
            audio_text = recognizer.record(source)

        text = recognizer.recognize_google(audio_text, language='ru-RU')
    else:
        await update.message.reply_text("Извините, я не понимаю ваш запрос. "
                                        "Пожалуйста, выберите команду из "
                                        "предложенного списка.")
        return

    # Handle commands based on recognized or entered text
    if re.search(r"селфи|последнее", text):
        await get_photo(update, str(SELFIE))
    elif re.search(r"фото|школ", text):
        await get_photo(update, str(HIGH_SCHOOL_PHOTO))
    elif re.search(r"хобби|увлечение", text):
        await get_text(update, str(ABOUT_HOBBY))
    elif re.search(r"ссылка|репозиторий|репо", text):
        await get_text(update, str(REPO))
    elif re.search(r"рассказ|gpt", text):
        await get_voice(update, str(GPT))
    elif re.search(r"разница|sql|nosql", text):
        await get_voice(update, str(SQL))
    elif re.search(r"история|первой|любви|первая|любовь", text):
        await get_voice(update, str(LOVE_STORY))
    else:
        await update.message.reply_text("Извините, я не понимаю ваш запрос. "
                                        "Пожалуйста, выберите команду из "
                                        "предложенного списка.")


# ОБРАБОТКА КНОПОЧНЫХ КОММАНД #

# ГЛАВНЫЙ ОБРАБОТЧИК ВХОДЯЩИХ СООБЩЕНИЙ #
def handle_incoming_message() -> None:
    """Обработывает входящие сообщения."""

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("commands", commands))
    application.add_handler(CallbackQueryHandler(handle_buttons))
    application.add_handler(
        MessageHandler(filters.TEXT | filters.VOICE,
                       handle_text_or_voice_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
