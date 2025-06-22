import json
import random
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

with open("questions.json", "r") as f:
    QUESTIONS = json.load(f)

asked_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏏 Welcome to Cricket Quiz King!

Type /quiz to get your first question.")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_questions = asked_users.get(user_id, [])
    available_questions = [q for q in QUESTIONS if q["question"] not in user_questions]

    if not available_questions:
        await update.message.reply_text("🎉 You've answered all available questions!")
        return

    question = random.choice(available_questions)
    asked_users.setdefault(user_id, []).append(question["question"])
    options = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(question["options"])])
    await update.message.reply_text(f"{question['question']}\n\n{options}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.run_polling()