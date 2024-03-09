from types import FunctionType
import utils


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


def about(message: str) -> str:
    return 'This is the about message'


def ping(message: str) -> str:
    return 'Pong!'


def message_is_command(message: str) -> bool:
    return message.startswith('/')


def process_command(message: str) -> str:
    answer = {
        '/help': help_command,
        '/about': about,
        '/ping': ping
    }

    ans = answer.get(message, 'Invalid command')
    if ans is str:
        return ans
    elif ans is FunctionType:
        return ans(message)
