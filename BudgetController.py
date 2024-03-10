from enum import Enum
import Database


class ExpenseCategory(Enum):
    """This class is an enum that contains the categories of expenses."""
    FOOD = 1
    TRANSPORTATION = 2
    UTILITIES = 3
    RENT = 4
    CLOTHING = 5
    MEDICAL = 6
    ENTERTAINMENT = 7
    MISCELLANEOUS = 8
    TAX = 9


class BudgetController:
    """This class is responsible for handling the budgeting and expenses of the users."""

    def __init__(self, db: Database.Database):
        self.db = db

    def add_expense(self, user_id: int, expense_amount: int, expense_category: ExpenseCategory) -> bool:
        """This function adds an expense to the database and updates the remaining budget for the user. If the remaining budget is less than 0, it returns True. Otherwise, it returns False."""
        self.db.insert("expenses", "user_id, amount, category_id, date", f"{user_id}, {expense_amount}, {expense_category.value}, datetime('now')")
        self.db.update("budgeting", f"remaining_budget = remaining_budget - {expense_amount}", f"user_id = {user_id}")
        if self.db.select("budgeting", "remaining_budget", f"WHERE user_id = {user_id}")[0][0] < 0:
            return True
        return False

    def get_expenses(self, user_id: int) -> list[tuple[int, int, int, str]]:
        """This function returns all the expenses of the user by their id as a list of tuples."""
        return self.db.select("expenses", "*", f"WHERE user_id = {user_id}")

    def get_expenses_by_category(self, user_id: int, category: ExpenseCategory) -> list[tuple[int, int, int, str]]:
        """This function returns all the expenses of the user by their id and category as a list of tuples."""
        return self.db.select("expenses", "*", f"WHERE user_id = {user_id} AND category_id = {category.value}")

    def get_expenses_by_date_range(self, user_id: int, start_date: str, end_date: str) -> list[tuple[int, int, int, str]]:
        """This function returns all the expenses of the user by their id and date range as a list of tuples."""
        return self.db.select("expenses", "*", f"WHERE user_id = {user_id} AND date BETWEEN '{start_date}' AND '{end_date}'")
