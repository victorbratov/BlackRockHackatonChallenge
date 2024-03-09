from types import FunctionType


def requires_message(func):
    def wrapper(message: str):
        if message is None:
            return 'Invalid command'
        return func(message)
    return wrapper


@requires_message
def help_command(message: str) -> str:
    return 'This is the help message'


def about() -> str:
    return """
    This was a bot created to help you with financial education and budgeting.
    You can use it to track your expenses and income, and it will give you a report of your financial situation.
    You can read articles that will answer your questions about personal finance.
    """


def ping() -> str:
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
