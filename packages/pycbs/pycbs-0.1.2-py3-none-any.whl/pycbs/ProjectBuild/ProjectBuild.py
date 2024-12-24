import os

from ..Messages import Message


class Run:
    def __init__(self, command: str = ''):
        self.command = command
    
    def Exec(self):
        os.system(self.command)


type Commands = Run


def ProjectBuild(*commands: list[Commands]):
    Message.Thread('сборка проекта:')

    for cmd in commands:
        cmd.Exec()

    Message.Thread('сборка завершена!')
