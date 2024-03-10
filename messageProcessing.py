from inspect import ismethod
import inspect
from typing import Union

import BudgetController
import utils
import graphics


def message_is_command(message: str) -> bool:
    return message.startswith('/')


class MessageProcessor:
    def __init__(self, bc: BudgetController.BudgetController):
        self.bc = bc
        self.commands = {
            '/help': self.help_command,
            '/about': self.about,
            '/ping': self.ping,
            '/add_expense': self.add_expense,
            '/use_budgeting': self.use_budgeting,
            '/stop_budgeting': self.stop_budgeting,
            '/set_monthly_budget': self.set_monthly_budget,
            '/show_this_month_expenses': self.show_this_month_expenses,
            '/chart': self.chart,
            '/show_commands': self.show_commands
        }

    def about(self) -> str:
        return """
        This was a bot created to help you with financial education and budgeting.
        You can use it to track your expenses and income, and it will give you a report of your financial situation.
        You can read articles that will answer your questions about personal finance.
        """

    def help_command(self, message: str) -> str:
        args = message.split(" ")
        if len(args) < 2:
            initial = """
            Welcome to the help pages, each of which provides information on a particular aspect of personal finance.
            To specify a help page, type "/help <page>" (replacing <page> with the page you want) and I will display it for you.
            The pages available are:
            """
            return initial
        else:
            help_page_maybe = utils.get_help_page(args[1])
            if help_page_maybe is None:
                return f"The help page \"{args[1]}\" does not exist"
            else:
                print("Error: Bad logic")
                return help_page_maybe

    def ping(self) -> str:
        return 'Pong!'

    def add_expense(self, user_id: int, message: str) -> str:
        if self.bc.db.select("users", "uses_budgeting", f"WHERE id = {user_id}")[0][0] == 0:
            return "You are not using the budgeting feature. You can enable it by typing /use_budgeting"
        if self.bc.db.select("budgeting", "monthly_budget", f"WHERE user_id = {user_id}")[0][0] == 0:
            return "You have not set a monthly budget. You can set it by typing /set_monthly_budget"
        args = message.split(" ")[1:]
        if len(args) != 2:
            return "Invalid command: /add_expense <amount> <category>"
        if not args[0].isdigit() or int(args[0]) < 0:
            return "Invalid amount. must be a positive integer"
        try:
            self.bc.add_expense(user_id, int(args[0]), BudgetController.ExpenseCategory[args[1]])
            ans = "expense added successfully\n"
            if self.bc.get_remaining_budget(user_id) < 0:
                ans += f"You have exceeded your budget. You have exceeded you budget by {str(self.bc.get_remaining_budget(user_id))[1:]}.\n"
            else:
                ans += f"Remaining budget: {self.bc.get_remaining_budget(user_id)}\n"
                ans += f"{self.bc.get_remaining_budget(user_id) / self.bc.get_monthly_budget(user_id) * 100}% of your monthly budget\n"
            return ans
        except KeyError:
            return "Invalid category. Must be one of the following: FOOD, TRANSPORTATION, UTILITIES, RENT, CLOTHING, MEDICAL, ENTERTAINMENT, MISCELLANEOUS, TAX"

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

    def show_this_month_expenses(self, user_id: int) -> (str, str):
        expenses = self.bc.get_this_month_expenses(user_id)
        file_path = f"charts/expenses_pie_chart_{user_id}.jpeg"
        graphics.create_expenses_pie_chart_and_as_jpg(expenses, file_path)
        ans = ""
        if len(expenses) == 0:
            ans = "You have no expenses this month"
        else:
            ans = "\n".join([f"Amount: {expense[1]}, Category: {BudgetController.ExpenseCategory(expense[2]).name}, Date: {expense[3]}" for expense in expenses])
        ans += f"\nRemaining budget: {self.bc.db.select('budgeting', 'remaining_budget', f'WHERE user_id = {user_id}')[0][0]}"
        return ans, file_path

    def chart(self, user_id: int, message: str) -> tuple[str, str]:
        expenses = self.bc.get_this_month_expenses(user_id)
        file_path = f"charts/expenses_cumulative_chart_{user_id}.jpeg"
        graphics.create_cumulative_expenses_chart_and_as_jpg(expenses, file_path)
        return "test", file_path

    def show_commands(self) -> str:
        return "\n".join(self.commands.keys())

    def process_command(self, user_id: int, message: str) -> Union[str, tuple[str]]:
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

    def process_message(self, user_id: int, user_name: str, message: str) -> Union[str, tuple[str]]:
        if not self.bc.db.user_exists(user_id):
            self.bc.db.insert("users", "id, name, uses_budgeting", f"{user_id}, '{user_name}', 0")
            return "Welcome to the bot! You have been registered. If you want to use the budgeting feature, type /use_budgeting"

        month = self.bc.db.select("budgeting", "month", f"WHERE user_id = {user_id}")[0][0]
        print(month, utils.get_current_month())
        if month != utils.get_current_month():
            self.bc.db.update("budgeting", "remaining_budget = monthly_budget, month = strftime('%m', 'now')", f"user_id = {user_id}")

        if message_is_command(message):
            return self.process_command(user_id, message)

        else:
            return "I'm sorry, I don't understand that command. Type /show_commands to see the available commands."
