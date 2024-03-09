from types import FunctionType


def help_command() -> str:
    return 'This is the help message'


def about() -> str:
    return 'This is the about message'


def ping() -> str:
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
        return ans()
