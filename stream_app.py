import streamlit as st
import threading
from telegram_bot import start_bot

# Iniciar o bot em um thread separado
threading.Thread(target=start_bot).start()

# Interface Streamlit para mostrar logs ou informações
st.title("Telegram Bot Status")
st.write("O bot do Telegram está rodando em segundo plano.")
