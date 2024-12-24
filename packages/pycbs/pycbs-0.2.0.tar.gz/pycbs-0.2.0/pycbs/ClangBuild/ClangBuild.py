'''
Главный пакет с функциями для сборки проектов
'''

import os

from .ClangBuildParams import *
from ..Messages import Message


def ClangCommandBuild (
        # Пути к папкам с библиотеками
        includePaths: list[str] = DEFAULT,
        libsPaths: list[str] = DEFAULT,
        
        # Файлы для сборки
        libs: list[str] = DEFAULT,
        startFile: list[str] = 'main.c',
        endFile: list[str] = DEFAULT,
        
        # Настройки компиляции
        linker: Linker = DEFAULT,
        target: tuple[Arch, Vendor, OS, ABI] = DEFAULT,

        # Платформенная компиляция
        native: bool = DEFAULT,
        showConsole: bool = DEFAULT,

        # Настройки языка
        lang: Language = DEFAULT,
        targetArch: TargetArch = DEFAULT,
        optimization: OptimizationMode = DEFAULT,
        std: LangStandart = DEFAULT,
) -> str:
    Message.Log(f'начало сборки команды...')

    # Проверка на правильность указанных путей
    if includePaths and libsPaths:
        for path in includePaths + libsPaths:
            if not os.path.exists(path):
                Message.Error(f'указанный путь [green]"{path}"[/]- не существует!')
                exit(1)
    
    # Проверка на правильность файла "startFile"
    if not os.path.exists(startFile):
        Message.Error(f'startFile [green]"{startFile}"[/]- не существует!')
        exit(1)

    if not os.path.isfile(startFile):
        Message.Error(f'startFile [green]"{startFile}"[/]- не файл!')
        exit(1)
    
    # Подключения
    resultIncludePaths = ''
    resultLibsPaths = ''
    resultEndFile = ''

    if includePaths:
        temp = [f' -I"{path}"' for path in includePaths]
        resultIncludePaths = ''.join(temp)
    
    if libsPaths:
        temp = [f' -L"{path}"' for path in libsPaths]
        resultLibsPaths = ''.join(temp)
    
    if endFile:
        resultEndFile = f' -o {endFile}'
    
    # Парсинг tanget
    resultTarget = ''
    
    if target:
        resultTarget = f'{target[0]}-{target[1]}-{target[2]}'

        if target[3]:
            resultTarget += f'-{target[3]}'

        return f' --target=' + resultTarget

    # Подключение статических библиотек
    resultLibs = ''

    if libs:
        temp = [f' -l"{lib}"' for lib in libs]
        resultLibs = ''.join(temp)

    resultCommand = (
        f'clang '
        + startFile
        + resultEndFile
        + resultIncludePaths
        + resultLibsPaths
        + ( f' -fuse-ld={linker}' if linker else '' )
        + resultTarget
        + resultLibs
        + ( f' -std={std}' if std else '' )
        + ( f' -x {lang}' if lang else '' )
        + ( f' {targetArch}' if targetArch else '' )
        + ( f' {optimization}' if optimization else '' )
        + ( f' -march=native' if native else '' )
        + ( f' -mwindows' if not showConsole else '' )
    )

    Message.Log('исходная команда:')
    Message.Data(resultCommand)

    return resultCommand
