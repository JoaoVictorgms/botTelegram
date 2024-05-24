import pandas as pd
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Carregar a planilha de placas
df = pd.read_excel('placas_mercosul.xlsx')
placas = df['Placa'].tolist()


def check_placa(placa, resultado):
    resultado.append(placa in placas)


# Handler para o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Envie uma placa de carro para verificar se ela está na planilha.')


# Handler para verificar a placa
async def verificar_placa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    placa = update.message.text.strip().upper()

    if not placa:
        await update.message.reply_text('Por favor, envie uma placa válida.')
        return

    # verificar a placa
    num_threads = 10
    resultados = []
    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=check_placa, args=(placa, resultados))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if any(resultados):
        await update.message.reply_text(f'A placa {placa} está na planilha.')
    else:
        await update.message.reply_text(f'A placa {placa} não está na planilha.')


def main() -> None:

    application = Application.builder().token(BOT_TOKEN).build()

    # Adicionar o handler para o comando /start
    application.add_handler(CommandHandler("start", start))

    # Adicionar o handler para mensagens de texto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verificar_placa))

    application.run_polling()


if __name__ == '__main__':
    main()
