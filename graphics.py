import plotly
import BudgetController

def create_expenses_pie_chart_and_as_jpg(expenses: list[tuple[int, int, int, str]], file_path: str) -> str:
    """This function creates a pie chart of the expenses and saves it as a jpeg file. It returns the path of the file."""
    categories = [BudgetController.ExpenseCategory(expense[2]).name for expense in expenses]
    amount = [expense[1] for expense in expenses]
    fig = plotly.graph_objs.Figure(data=[plotly.graph_objs.Pie(labels=categories, values=amount)])
    fig.write_image(file_path)
    return file_path

def create_cumulative_expenses_chart_and_as_jpg(expenses: list[tuple[int, int, int, str]], file_path: str) -> str:
    """This function creates a chart of the cumulative expenses and saves it as a jpeg file. It returns the path of the file."""
    dates = [expense[3] for expense in expenses]
    amount = [sum([expense[1] for expense in expenses[:i+1]]) for i in range(len(expenses))]
    fig = plotly.graph_objs.Figure(data=[plotly.graph_objs.Scatter(x=dates, y=amount, mode='lines+markers')])
    fig.write_image(file_path)
    return file_path

