import asyncio
import pandas as pd
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter o token do bot do ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")
logger.info(f"BOT_TOKEN: {BOT_TOKEN}")

# Função para ler apenas a coluna R do arquivo Excel e imprimir o número de linhas
def print_excel_info(file_path):
    try:
        df = pd.read_excel(file_path, usecols='R')
        num_rows = df.shape[0]
        print(f'O arquivo Excel possui {num_rows} linhas.')
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo Excel: {e}")

# Função para verificar se uma placa está na lista e retornar informações
def check_placa_info(placa):
    resultados = []
    try:
        for index, row in df_all_info.iterrows():
            if str(row.iloc[17]).strip().upper() == placa:  # Comparar a placa na coluna 18 (índice 17)
                resultados.append(row.to_dict())
                return resultados
        resultados.append(None)
        return resultados
    except Exception as e:
        logger.error(f"Erro ao verificar a placa: {e}")
        return None

# Handler para o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Recebido comando /start")
    await update.message.reply_text('Envie uma placa de carro para verificar se ela está na planilha.')

# Handler para verificar a placa
async def verificar_placa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    placa = update.message.text.strip().upper()
    logger.info(f"Placa recebida: {placa}")

    if not placa:
        await update.message.reply_text('Por favor, envie uma placa válida.')
        return

    resultados = check_placa_info(placa)
    if any(resultados):
        result = next((res for res in resultados if res is not None), None)
        if result:
            response = f'A placa {placa} está na planilha.\nInformações:\n'
            for key, value in result.items():
                response += f'{key}: {value}\n'
            await update.message.reply_text(response)
        else:
            await update.message.reply_text(f'A placa {placa} não está na planilha.')
    else:
        await update.message.reply_text(f'A placa {placa} não está na planilha.')

# Função para iniciar o bot
async def start_bot():
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verificar_placa))
        await application.run_polling()
    except Exception as e:
        logger.error(f"Erro ao iniciar o bot: {e}")

if __name__ == '__main__':
    try:
        # Carregar toda a planilha para obter todas as informações
        df_all_info = pd.read_excel('jardiel_base.xlsx')
    except Exception as e:
        logger.error(f"Erro ao carregar o arquivo Excel: {e}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
