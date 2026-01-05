import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        apuesta = context.args[0].replace("_", " ").title()
        context.user_data["apuesta"] = apuesta
        await update.message.reply_text(
            f"⚽ Apuesta seleccionada:\n{apuesta}\n\n💰 Escribe el monto a apostar:"
        )
    else:
        await update.message.reply_text("Bienvenido. Selecciona una apuesta desde la web.")

async def recibir_monto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "apuesta" not in context.user_data:
        await update.message.reply_text("Primero selecciona una apuesta desde la web.")
        return

    monto = update.message.text
    apuesta = context.user_data["apuesta"]

    await update.message.reply_text(
        f"✅ Apuesta registrada\n\nEquipo: {apuesta}\nMonto: {monto}"
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_monto)
    )
    application.run_polling()

if __name__ == "__main__":
    main()
