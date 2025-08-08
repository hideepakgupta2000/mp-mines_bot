import os
import shutil
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, ContextTypes, filters
)

from mp_fetch_data import fetch_emm11_data  

BOT_TOKEN = "YOUR_NEW_MP_BOT_TOKEN"

logging.basicConfig(level=logging.INFO)

SELECT_STATE, ASK_START, ASK_END, ASK_DISTRICT = range(4)
user_sessions = {}



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("MP", callback_data="state_mp")]]
    await update.message.reply_text("Please select a state:", reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECT_STATE

async def ask_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["start"] = int(update.message.text)
        await update.message.reply_text("Got it. Now enter the end number:")
        return ASK_END
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return ASK_START

async def ask_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["end"] = int(update.message.text)
        await update.message.reply_text("Now, please enter the district name:")
        return ASK_DISTRICT
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return ASK_END

async def ask_district(update: Update, context: ContextTypes.DEFAULT_TYPE):
    district = update.message.text
    user_id = update.effective_user.id
    start = context.user_data["start"]
    end = context.user_data["end"]

    await update.message.reply_text(f"Fetching data for MP, district: {district}...")

    user_sessions[user_id] = {"start": start, "end": end, "district": district, "data": []}

    async def send_entry(entry):
        msg = (
            f"{entry['eMM11_num']}\n"
            f"{entry['destination_district']}\n"
            f"{entry['destination_address']}\n"
            f"{entry['quantity_to_transport']}\n"
            f"{entry['generated_on']}"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        user_sessions[user_id]["data"].append(entry)

    await fetch_emm11_data(start, end, district, data_callback=send_entry)

    if user_sessions[user_id]["data"]:
        keyboard = [
            [InlineKeyboardButton("Start Again", callback_data="start_again")],
            [InlineKeyboardButton("Exit", callback_data="exit_process")]
        ]
        await context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Data fetched. What would you like to do next?", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("❌ No data found.")

    return ConversationHandler.END

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "state_mp":
        context.user_data["state"] = "MP"
        await query.edit_message_text("You selected MP. Please enter the start number:")
        return ASK_START

    if user_id not in user_sessions:
        await query.edit_message_text("⚠️ Session expired. Please type /start to begin again.")
        return ConversationHandler.END

    if query.data == "start_again":
        user_sessions.pop(user_id, None)
        await query.edit_message_text("🔁 Restarting...\nType /start")
        return ConversationHandler.END

    if query.data == "exit_process":
        user_sessions.pop(user_id, None)
        await query.edit_message_text("❌ Exiting process.")
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚫 Operation cancelled.")
    return ConversationHandler.END

async def main():
    

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_STATE: [CallbackQueryHandler(button_handler)],
            ASK_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_start)],
            ASK_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_end)],
            ASK_DISTRICT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_district)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 MP Bot is running...")
    await application.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
