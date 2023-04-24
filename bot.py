import telebot
from googletrans import Translator

translator = Translator()
bot = telebot.TeleBot('6119236097:AAFpyKKhllPd3evv3AgkH50i4qSkamfS1Uk')

LANGUAGES = {
    'sq': 'Albanian',
    'ar': 'Arabic',
    'be': 'Belarusian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'zh-CN': 'Chinese_simplified',
    'zh-TW': 'Chinese_traditional',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'gl': 'Galician',
    'de': 'German',
    'el': 'Greek',
    'iw': 'Hebrew',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'mk': 'Macedonian',
    'ms': 'Malay',
    'mt': 'Maltese',
    'no': 'Norwegian',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sr': 'Serbian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'es': 'Spanish',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'yi': 'Yiddish',
}

user_language = {}

language_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
for code, name in LANGUAGES.items():
    language_menu.add(telebot.types.KeyboardButton(name))


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_photo(message.chat.id, photo=open('beginning.jpg', 'rb'), caption=
    "Welcome to the Translator Bot!\n\n"
    "To use this bot, first select your preferred language by typing /select_language or clicking the button below.\n"
    "Then send any message you want to translate.",
                   reply_markup=language_menu,
                   )


@bot.message_handler(commands=["select_language"])
def select_language(message):
    bot.reply_to(
        message,
        "Please select your preferred language:",
        reply_markup=language_menu,
    )


@bot.message_handler(func=lambda message: message.text in LANGUAGES.values())
def set_language(message):
    language_code = [code for code, name in LANGUAGES.items() if name == message.text][0]
    user_language[message.chat.id] = language_code

    bot.reply_to(message, f"Language set to {message.text}.", reply_markup=language_menu)


@bot.message_handler(func=lambda message: True)
def translate_message(message):
    try:
        language_code = user_language[message.chat.id]
    except KeyError:
        bot.reply_to(
            message,
            "Please select a language first by typing /select_language or clicking the button below.",
            reply_markup=language_menu,
        )
        return

    if translator.detect(message.text).lang == language_code:
        bot.reply_to(message, "You are already translating to that language.")
        return

    translation = translator.translate(message.text, dest=language_code)
    bot.reply_to(message, translation.text)


bot.polling()
