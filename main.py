import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        apuesta = context.args[0].replace("_", " ").title()
        context.user_data["apuesta"] = apuesta
        await update.message.reply_text(
            f"⚽ Apuesta seleccionada:\n{apuesta}\n\n💰 Escribe el monto a apostar:"
        )
    else:
        await update.message.reply_text("Bienvenido. Selecciona una apuesta desde la web.")

async def monto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "apuesta" not in context.user_data:
        await update.message.reply_text("Primero selecciona una apuesta desde la web.")
        return

    cantidad = update.message.text
    apuesta = context.user_data["apuesta"]

    await update.message.reply_text(
        f"✅ Apuesta registrada\n\nEquipo: {apuesta}\nMonto: {cantidad}"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, monto))
    app.run_polling()

if __name__ == "__main__":
    main()
