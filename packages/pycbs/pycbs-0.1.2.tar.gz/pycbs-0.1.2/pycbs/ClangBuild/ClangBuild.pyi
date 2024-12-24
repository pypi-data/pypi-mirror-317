from .ClangBuildParams import *


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
    '''
    Возвращает собранную консольную команду clang
    '''
