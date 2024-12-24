from rich import print as rprint


class Message:
    @staticmethod
    def Log(text: str):
        rprint(f'[cyan bold]💭 (PyCBS лог) {text}[/]')


    @staticmethod
    def Error(text: str):
        rprint(f'[red bold]❌ (PyCBS Ошибка) {text}[/]')


    @staticmethod
    def Warn(text: str):
        rprint(f'[yellow bold]⚠ (PyCBS Внимание) {text}[/]')


    @staticmethod
    def Data(text: str):
        rprint(f'[green]{text}[/]')


    @staticmethod
    def Thread(text: str):
        rprint(f'[magenta bold]▶ (PyCBS Поток) {text}[/]')
