import os
from datetime import datetime
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

from vehicle_detector import run_inference
from lora_send import send_lora_count

from pathlib import Path

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "images"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Foto ricevuta. Avvio inferenza...")

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = IMAGE_DIR / f"parking_{timestamp}.jpg"

    await file.download_to_drive(str(image_path))

    try:
        count, output_path = run_inference(image_path)

        ack = send_lora_count(count)

        await update.message.reply_text(
            f"Inferenza completata.\n"
            f"Veicoli rilevati: {count}\n"
            f"Invio LoRa: {'ACK ricevuto' if ack else 'ACK non ricevuto'}"
        )

        with open(output_path, "rb") as img:
            await update.message.reply_photo(photo=img)

    except Exception as e:
        await update.message.reply_text(f"Errore: {e}")


def main():
    if TOKEN is None:
        raise RuntimeError("Token Telegram mancante nel file .env")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot avviato. Invia una foto su Telegram.")
    app.run_polling()


if __name__ == "__main__":
    main()
