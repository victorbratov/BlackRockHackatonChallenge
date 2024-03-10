from inspect import ismethod
import inspect
from os import listdir, path

import BudgetController
import utils


def message_is_command(message: str) -> bool:
    return message.startswith('/')


class MessageProcessor:
    def __init__(self, bc: BudgetController.BudgetController):
        self.bc = bc
        self.commands = {
            '/info': self.info_command,
            '/about': self.about,
            '/ping': self.ping,
            '/add_expense': self.add_expense,
            '/use_budgeting': self.use_budgeting,
            '/stop_budgeting': self.stop_budgeting,
            '/set_monthly_budget': self.set_monthly_budget,
            '/show_commands': self.show_commands
        }

    def about(self) -> str:
        return """
        This was a bot created to help you with financial education and budgeting.
        You can use it to track your expenses and income, and it will give you a report of your financial situation.
        You can read articles that will answer your questions about personal finance.
        """

    def info_command(self, message: str) -> str:
        args = message.split()
        if len(args) < 2:
            response = """Welcome to the info info, each of which provides information on a particular aspect of personal finance.
To specify an info page, type "/info <page>" (replacing <page> with the page you want) and I will display it for you.
The info available are:"""
            pages = [f for f in listdir("info") if path.isfile(path.join("info", f))]
            for page in pages:
                response += "\n - " + page[:-4]
            return response
        else:
            help_page_maybe = utils.get_help_page(args[1])
            if help_page_maybe is None:
                return f"The info page \"{args[1]}\" does not exist"
            else:
                return help_page_maybe

    def ping(self) -> str:
        return 'Pong!'

    def add_expense(self, user_id: int, message: str) -> str:
        if self.bc.db.select("users", "uses_budgeting", f"WHERE id = {user_id}")[0][0] == 0:
            return "You are not using the budgeting feature. You can enable it by typing /use_budgeting"
        if self.bc.db.select("budgeting", "monthly_budget", f"WHERE user_id = {user_id}")[0][0] == 0:
            return "You have not set a monthly budget. You can set it by typing /set_monthly_budget"
        args = message.split(" ")[1:]
        print(args)
        if len(args) != 2:
            return "Invalid command: /add_expense <amount> <category>"
        if not args[0].isdigit() or int(args[0]) < 0:
            return "Invalid amount. must be a positive integer"
        if BudgetController.ExpenseCategory[args[1]] is None:
            return "Invalid category. Must be one of the following: FOOD, TRANSPORTATION, UTILITIES, RENT, CLOTHING, MEDICAL, ENTERTAINMENT, MISCELLANEOUS, TAX"
        if self.bc.add_expense(user_id, int(args[0]), BudgetController.ExpenseCategory[args[1]]):
            return "You have exceeded your budget"
        else:
            return "Expense added successfully"

    def use_budgeting(self, user_id: int) -> str:
        self.bc.db.update("users", "uses_budgeting = 1", f"id = {user_id}")
        self.bc.db.insert("budgeting", "user_id, monthly_budget, remaining_budget", f"{user_id}, 0, 0")
        return "You have enabled the budgeting feature"

    def stop_budgeting(self, user_id: int) -> str:
        self.bc.db.update("users", "uses_budgeting = 0", f"id = {user_id}")
        self.bc.db.delete("budgeting", f"user_id = {user_id}")
        return "You have disabled the budgeting feature"

    def set_monthly_budget(self, user_id: int, message: str) -> str:
        if self.bc.db.select("users", "uses_budgeting", f"WHERE id = {user_id}")[0][0] == 0:
            return "You are not using the budgeting feature. You can enable it by typing /use_budgeting"
        args = message.split(" ")[1:]
        if len(args) != 1:
            return "Invalid command: /set_monthly_budget <amount>"
        if not args[0].isdigit() or int(args[0]) < 0:
            return "Invalid amount. must be a positive integer"
        self.bc.db.update("budgeting", f"monthly_budget = {args[0]}, remaining_budget = {args[0]}", f"user_id = {user_id}")
        return "Monthly budget set successfully"

    def show_commands(self) -> str:
        return "\n".join(self.commands.keys())

    def process_command(self, user_id: int, message: str) -> str:
        com = message.split(" ")[0]
        ans = self.commands.get(com, 'Invalid command')
        if ans is str:
            return ans
        elif ismethod(ans):
            if inspect.signature(ans).parameters.keys().__contains__('user_id') and inspect.signature(ans).parameters.keys().__contains__('message'):
                return ans(user_id, message)
            elif inspect.signature(ans).parameters.keys().__contains__('message'):
                return ans(message)
            elif inspect.signature(ans).parameters.keys().__contains__('user_id'):
                return ans(user_id)
            else:
                return ans()
        else:
            return 'Invalid command'

    def process_message(self, user_id: int, user_name: str, message: str) -> str:
        if message_is_command(message):
            return self.process_command(user_id, message)

        if not self.bc.db.user_exists(user_id):
            self.bc.db.insert("users", "id, name, uses_budgeting", f"{user_id}, '{user_name}', 0")
            return "Welcome to the bot! You have been registered. If you want to use the budgeting feature, type /use_budgeting"

        else:
            return "I'm sorry, I don't understand that command. Type /show_commands to see the available commands."
