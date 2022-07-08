from email.mime import application
import logging
from datetime import datetime
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, JobQueue
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_diff_working_hours(username: str):
    
    stop_working = {
        'islamtramov': 18,
        'TikhonovD': 18,
        'rash708': 18,
        'NSIbragim': 19,
        'misha1234555': 19
    }
    
    
    if username == 'NikoGasanov':
        message = 'отдохни от доты, брат, не сегодня'
    else:
        now = datetime.now()
        stop = datetime.now().replace(hour=stop_working[username], minute=0, second=0)
        if now.time() < time(stop_working[username] - 9, 00, 00) or now.time() > time(stop_working[username], 00, 00):
            message = 'леее, куда прёшь, пора отдыхать'
        else:
            diff = stop - now
            diff_without_ms = str(diff).split(".")[0]
            message = f'до конца рабочего дня осталось: {diff_without_ms}'
    return message


def is_rashid_relaxing():
    now = datetime.now().time()
    return (now < time(9, 00, 00) or now > time(18, 00, 00))


async def end_of_work(context: CallbackContext):
    await context.bot.send_message(chat_id=context.job.chat_id, text='А Рашид закончил)))')


async def daily_job(update: Update, context: CallbackContext):
    # TODO: fix actual time - 3 hours time zone
    end_time = time(15, 00, 00)
    await context.job_queue.run_daily(end_of_work, end_time, days=tuple(range(5)), chat_id=update.message.chat_id)


async def start(update: Update, context: CallbackContext):
    start_text = f'Привет, я лысый счетовод. Я подсказываю, сколько часов осталось до конца рабочего дня (команда /hours).'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)
    

async def get_working_hours_remaining(update: Update, context: CallbackContext):
    username, first_name = update.message.from_user['username'], update.message.from_user['first_name']
    print(update.message.from_user)
    
    diff_working_hours = get_diff_working_hours(username)
    message = f'{first_name}, {diff_working_hours}'
    
    if username != 'rash708':
        # if 'отд' not in diff_working_hours:
        if not is_rashid_relaxing():
            message += f"\nА вот Рашиду {get_diff_working_hours('rash708')}"
        else:
            message += '\nА вот Рашид уже отдыхает)'
        
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ["BALD_BOOKKEEPER_BOT_TOKEN"]).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('time', get_working_hours_remaining))
    application.add_handler(CommandHandler('notify', daily_job))

    application.run_polling()