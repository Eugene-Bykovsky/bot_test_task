import os

from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Телеграмм токен
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Определим стадии диалога с ботом
SELFIE, HIGH_SCHOOL_PHOTO, ABOUT_HOBBY, REPO, GPT, SQL, LOVE_STORY = range(7)

TEXT_LIST = {
    'hobby': "Я люблю путешествовать в разные уголки мира, открывая для себя "
             "новые страны, города и культуры. Каждое место имеет свою " 
             "уникальную атмосферу и свои особенности, которые я стараюсь "
             "понять и оценить. Я считаю, что путешествия помогают расширять "
             "горизонты и находить новые идеи и вдохновение для своей жизни.",
    'repo': "https://github.com/Eugene-Bykovsky/praktikum_test_task",
}
