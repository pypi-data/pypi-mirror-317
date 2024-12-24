import os
import sys

from rich import print as rprint


VERSION = '0.2.0'


HELLO_TEST = f'''
[green]Привет! Это CLI сборщик на Python - PyCBS {VERSION}[/]

[yellow bold]⚠ На данный момент достуна сборка только для clang![/]
[yellow bold]⚠ На данный момент поддержка ориентированна на Windows![/]

[violet]Параметры:[/]
[grey]*[/] [bold]init[/] - [green]инициализарует файл сборки в вашей директории[/]

[green]Чтобы начать сборку проекта, просто запустите "pmake.py" файл![/]
'''[1:-1]


PMAKE_CODE = '''
from pycbs import *


command = ClangCommandBuild (
    startFile='main.c',
    endFile='hello.exe',
    
    includePaths=[
    ],
    libsPaths=[
    ],
    libs=[
    ],
)


ProjectBuild(
    Run(command)
)

'''[1:-1]


if __name__ == '__main__':
    thisPath = os.getcwd()

    match sys.argv:
        case [_, 'init']:
            if os.path.exists('pmake.py'):
                rprint('[yellow bold]В директории уже есть "pmake.py" файл! Перезаписать его?[/]')
                rprint('[grey]y или Enter - да, n - нет >> [/]', end='')

                if input() == 'n':
                    exit(0)

            with open('pmake.py', 'w', encoding='utf-8') as file:
                file.write(PMAKE_CODE)

        case _:
            rprint(HELLO_TEST)
