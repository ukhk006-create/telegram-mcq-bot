import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Get bot token from Railway environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Simple quiz questions
QUESTIONS = [
    {
        "question": "Which is the capital of India?",
        "options": ["Mumbai", "New Delhi", "Kolkata", "Chennai"],
        "answer": 1
    },
    {
        "question": "Who is known as the Father of the Nation (India)?",
        "options": ["Bhagat Singh", "Mahatma Gandhi", "Subhas Bose", "Jawaharlal Nehru"],
        "answer": 1
    },
    {
        "question": "Which planet is called the Red Planet?",
        "options": ["Earth", "Venus", "Mars", "Jupiter"],
        "answer": 2
    }
]

# To track user progress
user_progress = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_progress[user_id] = 0
    await send_question(update, context, user_id)

async def send_question(update, context, user_id):
    q_index = user_progress[user_id]
    if q_index < len(QUESTIONS):
        question = QUESTIONS[q_index]
        keyboard = [
            [InlineKeyboardButton(opt, callback_data=str(i)) for i, opt in enumerate(question["options"])]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=user_id,
            text=question["question"],
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(chat_id=user_id, text="🎉 Quiz completed!")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    q_index = user_progress[user_id]
    question = QUESTIONS[q_index]

    if int(query.data) == question["answer"]:
        await query.edit_message_text(text=f"✅ Correct! {question['options'][question['answer']]}")
    else:
        await query.edit_message_text(
            text=f"❌ Wrong! Correct answer: {question['options'][question['answer']]}"
        )

    user_progress[user_id] += 1
    await send_question(update, context, user_id)

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
