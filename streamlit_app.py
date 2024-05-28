import asyncio
import os
from dotenv import load_dotenv
from telegram_bot import start_bot as bot_start

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter o token do bot do ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Função para iniciar o bot assincronamente
async def start_bot_async():
    await bot_start()

# Configurar o loop de eventos assíncrono na thread principal
def main():
    asyncio.run(start_bot_async())

if __name__ == "__main__":
    main()
