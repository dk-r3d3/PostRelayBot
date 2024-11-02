▎Telegram Post Forwarding Bot

▎Описание проекта

Этот проект представляет собой асинхронного бота для Telegram, который предназначен для автоматической пересылки постов из заданных Telegram-каналов в указанный канал-получатель. Бот использует библиотеки aiogram, telethon и sqlalchemy, что позволяет эффективно работать с API Telegram и управлять данными.

▎Основные функции

• Асинхронная обработка: Бот работает на основе асинхронного программирования, что обеспечивает высокую производительность и отзывчивость.

• Пересылка постов: Бот может пересылать сообщения из одного канала в другой, что позволяет легко делиться контентом.

• Фильтрация по ключевым словам: Возможность настройки фильтрации постов по ключевым словам. Вы можете указать ключевые слова, и бот будет пересылать только те сообщения, которые соответствуют заданным критериям.

• Управление данными: Использование sqlalchemy для хранения настроек бота и истории пересылок, что обеспечивает надежное управление данными.

▎Установка

1. Клонируйте репозиторий:
   
   git clone https://github.com/ваш_пользователь/telegram-post-forwarding-bot.git
   

2. Установите необходимые зависимости:
   
   pip install -r requirements.txt
   

3. Настройте конфигурацию бота, указав токены и необходимые параметры в файле config.py.

▎Использование

1. Запустите бота:
   
   python bot.py
   

2. Настройте каналы и ключевые слова через интерфейс или файл конфигурации.

▎Вклад

Если вы хотите внести свой вклад в проект, пожалуйста, создайте форк репозитория и отправьте пулл-реквест с вашими изменениями.

▎Лицензия

Этот проект лицензирован под MIT License. 

---

Feel free to customize this description according to your preferences!
