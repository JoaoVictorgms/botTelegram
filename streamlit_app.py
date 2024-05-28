import streamlit as st
import threading
import time
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter o token do bot do ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")

st.title("Telegram Bot Status")
st.write("O bot do Telegram está rodando em segundo plano.")

# Função para iniciar o bot
def start_bot():
    from telegram_bot import start_bot as bot_start
    bot_start()

# Iniciar o bot em uma thread separada
bot_thread = threading.Thread(target=start_bot)
bot_thread.start()
