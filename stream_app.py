import streamlit as st
import asyncio
import threading
from telegram_bot import start_bot

# Função para iniciar a aplicação assíncrona em uma thread separada
def run_async():
    asyncio.run(start_bot())

# Iniciar o loop de eventos asyncio em uma thread separada
async_thread = threading.Thread(target=run_async)
async_thread.start()

# Interface Streamlit para mostrar logs ou informações
st.title("Telegram Bot Status")
st.write("O bot do Telegram está rodando em segundo plano.")
