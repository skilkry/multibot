import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from bots import ocr_reader, content_downloader
from aiogram.types import FSInputFile



load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("No se ha encontrado el TELEGRAM_TOKEN en el archivo .env")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    
    """Mensaje de bienvenida que explica los comandos."""
    await message.reply(
        "¡Hola! Soy tu bot multifunción. Estas son mis habilidades:\n\n"
        "1️⃣ *Lector de Facturas:*\nEnvíame una foto de un recibo o factura y extraeré el texto.\n\n"
        "2️⃣ *Descargador de Contenido:*\nUsa el comando `/descargar <URL>` para bajar un vídeo de sitios como YouTube, Twitter, etc.",
        parse_mode="Markdown"
    )

@dp.message(lambda message: message.content_type == "photo")
async def handle_photo(message: Message):
    photo = message.photo[-1]  # Mejor calidad
    file = await bot.get_file(photo.file_id)
    
    temp_photo_path = f"temp_{photo.file_id}.jpg"
    
    with open(temp_photo_path, "wb") as f:
        await bot.download_file(file.file_path, destination=f)
    
    await message.reply("🤖 Foto recibida. Procesando con OCR...")

    texto_extraido = ocr_reader.extract_text_from_image(temp_photo_path)
    
    await message.reply(f"Texto extraído:\n```\n{texto_extraido}\n```", parse_mode="Markdown")
    
    os.remove(temp_photo_path)
    
@dp.message(Command("descargar"))
async def cmd_download(message: Message):
    """Esta función se activa al recibir /descargar <URL>."""
    try:
        url = message.text.split(" ", 1)[1]
    except IndexError:
        await message.reply("Formato incorrecto. Uso: `/descargar <URL>`")
        return

    msg_espera = await message.reply(f"🤖 Recibido. Iniciando descarga desde la URL...")
    
    result = content_downloader.download_media(url)
    
    if result["status"] == "success":
        filepath = result["filepath"]
        title = result["title"]
        print(f"Descarga exitosa: {filepath}")

        try:
            file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
            if file_size_mb > 49:
                await msg_espera.edit_text(f" Descarga completada, pero el archivo '{title}' pesa {file_size_mb:.2f} MB y es demasiado grande para enviarlo por Telegram (límite 50MB).")
                return 

            await msg_espera.edit_text(f" Descarga completada. Enviando vídeo '{title}'...")
            
            await message.reply_video(FSInputFile(filepath))
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    else:
        await msg_espera.edit_text(f" Error al descargar:\n`{result['message']}`", parse_mode="Markdown")

async def main():
    print("Iniciando bot multifunción...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())