import os import telebot from telebot import types from datetime import datetime import pytz

Ambil token dan owner ID dari environment

BOT_TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = int(os.getenv("OWNER_ID"))

bot = telebot.TeleBot(BOT_TOKEN)

LANGUAGES = { "id": "Bahasa Indonesia", "en": "English" }

user_lang = {} user_balance = {}  # saldo pengguna dalam satoshi

Sistem pembagian hasil 70:30

OWNER_SHARE = 0.7 USER_SHARE = 0.3

Waktu aktif bot (12:00 - 24:00 WIB)

ACTIVE_HOURS = (12, 24) TZ = pytz.timezone("Asia/Jakarta")

Pesan multibahasa

MESSAGES = { "start": { "id": "Selamat datang di SatStorm! Dapatkan satoshi gratis setiap hari. Pilih bahasa kamu:", "en": "Welcome to SatStorm! Get free satoshi daily. Please choose your language:" }, "balance": { "id": "Saldo kamu saat ini adalah {satoshi} satoshi.", "en": "Your current balance is {satoshi} satoshi." }, "not_active": { "id": "Bot hanya aktif antara pukul 12:00 hingga 24:00 WIB.", "en": "Bot is only active between 12:00 and 24:00 WIB." }, "set_lang": { "id": "Bahasa disetel! Ketik /saldo untuk melihat saldo kamu.", "en": "Language set! Type /balance to see your balance." } }

def translate(user_id, key, **kwargs): lang = user_lang.get(user_id, "en") return MESSAGES[key][lang].format(**kwargs)

def is_bot_active(): now = datetime.now(TZ).hour return ACTIVE_HOURS[0] <= now < ACTIVE_HOURS[1]

@bot.message_handler(commands=['start']) def start_handler(message): if not is_bot_active(): bot.send_message(message.chat.id, translate(message.chat.id, "not_active")) return markup = types.ReplyKeyboardMarkup(resize_keyboard=True) for code, name in LANGUAGES.items(): markup.add(types.KeyboardButton(name)) bot.send_message(message.chat.id, translate(message.chat.id, "start"), reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in LANGUAGES.values()) def set_language(message): for code, name in LANGUAGES.items(): if message.text == name: user_lang[message.chat.id] = code break user_balance[message.chat.id] = 0 bot.send_message(message.chat.id, translate(message.chat.id, "set_lang"))

@bot.message_handler(commands=['saldo', 'balance']) def check_balance(message): if not is_bot_active(): bot.send_message(message.chat.id, translate(message.chat.id, "not_active")) return satoshi = user_balance.get(message.chat.id, 0) bot.send_message(message.chat.id, translate(message.chat.id, "balance", satoshi=satoshi))

if name == 'main': bot.infinity_polling()

