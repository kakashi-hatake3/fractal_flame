from enum import StrEnum


class ThreadTypes(StrEnum):
    SYNC = "sync"
    MULTITHREAD = "multithread"


class FunctionNames(StrEnum):
    LINEAR = "Линейная"
    SINUSOIDAL = "Синусоидальная"
    SPHERICAL = "Сферическая"
    SWIRL = "Виток"
    POLAR = "Полярная"
    HEART = "Сердечник"
    DISK = "Диск"
    COSINE = "Косинусоидальная"
    FAN = "Вентилятор"
