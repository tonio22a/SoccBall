import telebot
from config import BOT_TOKEN, DB_NAME
from logic import FootballLogic

bot = telebot.TeleBot(BOT_TOKEN)
logic = FootballLogic(DB_NAME)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "⚽ Команды:\n/teams - команды\n/match - матч\n/edit - изменить команду")

@bot.message_handler(commands=['teams'])
def teams(message):
    teams = logic.get_teams()
    text = "🏆 Команды:\n"
    for id, name, country, city, stadium in teams:
        text += f"{id}. {name} ({stadium})\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['edit'])
def edit_team(message):
    teams = logic.get_teams()
    text = "Выбери команду (номер):\n"
    for id, name, _, _, _ in teams:
        text += f"{id}. {name}\n"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, process_edit)

def process_edit(message):
    try:
        team_id = int(message.text)
        bot.send_message(message.chat.id, "Введи новое название и стадион через запятую:")
        bot.register_next_step_handler(message, update_team, team_id)
    except:
        bot.send_message(message.chat.id, "Ошибка!")

def update_team(message, team_id):
    try:
        name, stadium = message.text.split(',', 1)
        logic.update_team(team_id, name.strip(), stadium.strip())
        bot.send_message(message.chat.id, "✅ Команда обновлена!")
    except:
        bot.send_message(message.chat.id, "Ошибка формата!")

@bot.message_handler(commands=['match'])
def match(message):
    teams = logic.get_teams()
    text = "Выбери две команды (номера через пробел):\n"
    for id, name, _, _, _ in teams:
        text += f"{id}. {name}\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        if len(message.text.split()) == 2:
            a, b = map(int, message.text.split())
            home, away, stadium, score1, score2 = logic.simulate_match(a, b)
            stats = logic.get_stats()
            
            result = f"⚽ {home} {score1}-{score2} {away}\n"
            result += f"🏟️ {stadium}\n\n"
            result += f"📊 Статистика:\n"
            result += f"Удары: {stats['удары']}\n"
            result += f"Владение: {stats['владение']}\n"
            result += f"Угловые: {stats['угловые']}\n"
            result += f"Фолы: {stats['фолы']}"
            
            bot.send_message(message.chat.id, result)
    except:
        bot.send_message(message.chat.id, "Ошибка! Используй /match")

bot.polling()