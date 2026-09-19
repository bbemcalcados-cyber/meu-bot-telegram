import os
import telebot

# Puxa o token de forma segura das configurações do Render
CHAVE_API = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(CHAVE_API)

@bot.message_handler(commands=['start'])
def enviar_boas_vindas(mensagem):
    bot.reply_to(mensagem, "Olá! Meu bot do Telegram está rodando de graça na nuvem pelo Render!")

# Mantém o bot ligado direto escutando o Telegram
bot.infinity_polling()
