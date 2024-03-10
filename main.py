# bot.py
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import load_dotenv

import BudgetController
import Database
import DiscordBot
import messageProcessing

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_PATH = os.getenv('DB_PATH')
print(TOKEN)

db = Database.Database(DB_PATH)
bc = BudgetController.BudgetController(db)
mp = messageProcessing.MessageProcessor(bc)
bot = DiscordBot.DiscordBot(TOKEN, mp)
scheduler = AsyncIOScheduler()



def db_init():
    db.create_table_if_not_exists("users", "id INTEGER PRIMARY KEY, name TEXT, uses_budgeting BOOLEAN")
    db.create_table_if_not_exists("budgeting", "user_id INTEGER, monthly_budget INTEGER, remaining_budget INTEGER, FOREIGN KEY (user_id) REFERENCES users(id)")
    db.create_table_if_not_exists("expenses", "user_id INTEGER, amount INTEGER, category_id INTEGER, date TEXT ,FOREIGN KEY (user_id) REFERENCES users(id)")

def dirs_init():
    if not os.path.exists('charts'):
        os.makedirs('charts')


def init_scheduler(scheduler: AsyncIOScheduler, foo: callable):
    scheduler.add_job(foo, 'cron', second='0')
    scheduler.start()


async def reset_budgets():
    print("upd")
    db.update("budgeting", "remaining_budget = monthly_budget", "")
    users = db.select("users", "id", "")
    for user in users:
        await bot.client.get_user(user[0]).send("New month. New Budget")




if __name__ == "__main__":
    db_init()
    dirs_init()
    init_scheduler(scheduler, reset_budgets)
    bot.run()
