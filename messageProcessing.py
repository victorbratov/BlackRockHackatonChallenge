from types import FunctionType
import utils


def requires_message(func):
    def wrapper(message: str):
        if message is None:
            return 'Invalid command'
        return func(message)
    return wrapper



def about() -> str:
    return """
    This was a bot created to help you with financial education and budgeting.
    You can use it to track your expenses and income, and it will give you a report of your financial situation.
    You can read articles that will answer your questions about personal finance.
    """


def help_command(message: str) -> str:
    args = message.split(" ")
    if len(args) < 2:
        initial = """
        Welcome to the help pages, each of which provides information on a particular aspect of personal finance.
        To specify a help page, type "/help <page>" (replacing <page> with the page you want) and I will display it for you.
        The pages available are:
        """
    else:
        help_page_maybe = utils.get_help_page(args[1])
        if help_page_maybe is None:
            return f"The help page \"{args[1]}\" does not exist"
        else:
            print("Error: Bad logic")
            return help_page_maybe


def ping(message: str) -> str:
    return 'Pong!'

def show_commands() -> str:
    return '/help\n/about\n/ping\n/show_commands'


def message_is_command(message: str) -> bool:
    return message.startswith('/')


def process_command(message: str) -> str:
    answer = {
        '/help': help_command,
        '/about': about,
        '/ping': ping,
        '/show_commands': show_commands
    }

    ans = answer.get(message, 'Invalid command')
    if ans is str:
        return ans
    elif ans is FunctionType:
        if requires_message(ans):
            return ans(message)
        else:
            return ans()

          