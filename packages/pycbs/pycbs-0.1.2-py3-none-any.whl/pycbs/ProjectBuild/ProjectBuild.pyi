from typing import NoReturn


class Run:
    '''
    Команда сборщику: "выполни консольную команду"
    '''

    def __init__(self, command: str = ''):
        ...
    
    def Exec(self) -> NoReturn:
        ...


# Команды для сборщика
type Commands = Run


def ProjectBuild(*commands: list[Commands]) -> NoReturn:
    '''
    Сборщик проектов

    Args:
        commands (list[Commands]) - команды сборщика
    '''