import asyncio
import threading
import os
from dotenv import load_dotenv
from telegram_bot import start_bot as bot_start

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter o token do bot do ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Função para iniciar o bot
async def start_bot_async():
    await bot_start()

# Função para iniciar o bot em uma nova thread
def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot_async())

# Iniciar o bot em uma thread separada
bot_thread = threading.Thread(target=start_bot)
bot_thread.start()
