import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import openai
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 Katalog", callback_data="menu_katalog")],
        [InlineKeyboardButton("🤖 AI Chat", callback_data="menu_ai")]
    ]
    await update.message.reply_text(
        "👋 Selamat datang di bot!
Silakan pilih menu:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- AI CHAT ---
async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":user_msg}]
    )
    reply = completion.choices[0].message["content"]
    await update.message.reply_text(reply)

# --- AUTO WELCOME ---
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"Selamat datang {member.full_name} 👋")

# --- AUTO SPAM (ADMIN ONLY) ---
async def cmd_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in [123456789]:  # ganti ID admin
        return await update.message.reply_text("❌ Kamu bukan admin.")
    try:
        text = context.args[0]
        count = int(context.args[1])
        for _ in range(count):
            await update.message.reply_text(text)
            await asyncio.sleep(0.5)
    except:
        await update.message.reply_text("Format: /spam <text> <jumlah>")

# --- CALLBACK MENU ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu_katalog":
        await query.edit_message_text("📦 Daftar katalog:
1. Produk A
2. Produk B")
    elif query.data == "menu_ai":
        await query.edit_message_text("Ketik pesan apapun untuk mulai chat dengan AI.")

# --- RUN APP ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spam", cmd_spam))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot running…")
    app.run_polling()

if __name__ == "__main__":
    main()
