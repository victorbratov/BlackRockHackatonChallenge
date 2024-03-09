from os import listdir, path
from types import FunctionType
import utils


def requires_message(func):
    def wrapper(message: str):
        if message is None:
            return 'Invalid command'
        return func(message)
    return wrapper


def about_command() -> str:
    return """
    This was a bot created to help you with financial education and budgeting.
    You can use it to track your expenses and income, and it will give you a report of your financial situation.
    You can read articles that will answer your questions about personal finance.
    """


@requires_message
def info_command(message: str) -> str:
    args = message.split()
    if len(args) < 2:
        response = """
        Welcome to the info pages, each of which provides information on a particular aspect of personal finance.
        To specify an info page, type "/info <page>" (replacing <page> with the page you want) and I will display it for you.
        The pages available are:
        """
        pages = [f for f in listdir("pages") if path.isfile(path.join("pages", f))]
        for page in pages:
            response += page[:-4] + "\n"
        return response
    else:
        help_page_maybe = utils.get_help_page(args[1])
        if help_page_maybe is None:
            return f"The help page \"{args[1]}\" does not exist"
        else:
            print("Error: Bad logic")
            return help_page_maybe


def ping_command() -> str:
    return 'Pong!'


@requires_message
def help_command(message: str) -> str:
    args = message.split()
    if len(args) < 2:
        response = """
        Available commands:
        /ping
        /about
        /help
        /info <page>
        """
        return response
    else:
        help_cmd = args[1]
        # TODO: Return information about each command - Move the /info help here?
        return f"You have requested help for command {help_cmd}"


def message_is_command(message: str) -> bool:
    return message.startswith('/')


def process_command(message: str) -> str:
    answer = {
        '/info': info_command,
        '/about': about_command,
        '/ping': ping_command,
        '/help': help_command
    }

    ans = answer.get(message, 'Invalid command')
    if ans is str:
        return ans
    elif ans is FunctionType:
        if requires_message(ans):
            return ans(message)
        else:
            return ans()

          