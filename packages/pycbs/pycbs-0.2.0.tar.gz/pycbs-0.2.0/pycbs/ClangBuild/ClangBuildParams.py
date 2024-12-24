from enum import Enum


# DEFAULT - значение по умолчанию (опитимизация команды)
DEFAULT = None


class Arch(Enum):
    '''
    Архитектуры проецессоров
    '''
    # Intel / AMD
    I386 = 'i386'
    X86_64 = 'x86_64'
    
    # ARM
    ARM = 'arm'
    ARMV7 = 'armv7'
    AARCH64 = 'aarch64'
    
    # RISC-V
    RISCV32 = 'riscv32'
    RISCV64 = 'riscv64'

    # MSPS
    MIPS = 'mips'
    MIPS64 = 'mips64'

    # PowerPC
    POWERPC = 'powerpc'
    POWERPC64LE = 'powerpc64le'


class Vendor(Enum):
    '''
    Производители аппаратного обеспечения
    '''
    PC = 'pc'
    APPLE = 'apple'
    UNKNOWN = 'unknown'
    EABI = 'eabi'


class OS(Enum):
    '''
    Операционные системы
    '''
    # Стандартные системы ПК
    WINDOWS = 'windows'
    LINUX = 'linux'
    DARWIN = 'darwin'
    
    # BSD системы
    FREEBSD = 'freebsd'
    NETBSD = 'netbsd'
    OPENBSD = 'openbsd'

    # Для bare-metal приложений
    NONE = 'none'


class ABI(Enum):
    '''
    ABI интерфейсы для линковки библиотек
    '''
    MINGW = 'mingw'
    GNU = 'gnu'
    GNUEABIHF = 'gnueabihf'
    MSVC = 'msvc'
    ELF = 'elf'


# Тип цели
type Target_T = tuple[Arch, Vendor, OS, ABI]


class C_STD(Enum):
    '''
    Стандарты языка
    '''
    C89 = 'c89'
    C99 = 'c99'
    C11 = 'c11'
    C17 = 'c17'
    C23 = 'c23'


# Стандарты языков
type LangStandart = C_STD


class CompileModes(Enum):
    '''
    Что делать с файлом
    '''
    OBJECT = '-o'
    COMPILE = '-c'
    PREPROCESSING = '-E'
    ASM_CODE = '-S'


class Linker(Enum):
    '''
    Линкеры
    '''
    LLVM = 'lld'


class Language(Enum):
    '''
    Языки программирования
    '''
    C = 'c'


class TargetArch(Enum):
    '''
    Ориентация на определенную архитектуру (M32 - x32, M64 - x64)
    '''
    M32 = 'm32'
    M64 = 'm64'


class OptimizationMode(Enum):
    '''
    Оптимизация кода
    '''
    NONE = '-O0'
    LVL_1 = '-O1'
    LVL_2 = '-O2'
    LVL_3 = '-O3'
    MIN_SIZE = '-Os'
    FAST = '-Oz'
