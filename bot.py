import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

messages = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message

    if user.id == ADMIN_ID:
        if msg.reply_to_message:
            original_id = messages.get(msg.reply_to_message.message_id)
            if original_id:
                await context.bot.send_message(
                    chat_id=original_id,
                    text=msg.text or ""
                )
        return

    sent = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 NYTT MEDDELANDE\n\n"
             f"Namn: {user.full_name}\n"
             f"Username: @{user.username or 'saknas'}\n"
             f"User ID: {user.id}\n\n"
             f"Meddelande:\n{msg.text or '[Meddelande utan text]'}"
    )

    messages[sent.message_id] = user.id

    await msg.reply_text("Tack! Ditt meddelande har skickats.")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))
app.run_polling()
