import random

from src.enums import ThreadTypes
from src.ifs import IFS
from src.transformation import Transformation
from src.variations import VariationList


class Config:
    """Интерфейс конфигурации."""

    def initialize(self):
        """Инициализация параметров."""
        pass


class WindowConfig(Config):
    """Конфигурация окна."""

    def __init__(self):
        self.width = 800
        self.height = 600

    def initialize(self) -> "WindowConfig":
        try:
            self.width = int(input("Введите ширину окна: "))
            self.height = int(input("Введите высоту окна: "))
            if self.width <= 0 or self.height <= 0:
                raise ValueError
        except ValueError:
            print("Неверный ввод!")
            exit()
        return self


class SymmetryConfig(Config):
    """Конфигурация симметрии."""

    def __init__(self):
        self.symmetry = 1

    def initialize(self) -> "SymmetryConfig":
        try:
            symmetry = int(input("Введите уровень симметрии (1 для отключения): "))
            if symmetry < 1:
                raise ValueError
            self.symmetry = symmetry
        except ValueError:
            print("Нет такой симметрии!")
            exit()
        return self


class GammaConfig(Config):
    """Конфигурация гамма-преобразования."""

    def __init__(self):
        self.use_gamma = True

    def initialize(self) -> "GammaConfig":
        use_gamma_input = input("Включить гамма-коррекцию? (y/n): ").strip().lower()
        self.use_gamma = use_gamma_input == "y"
        return self


class RenderModeConfig(Config):
    """Конфигурация режима рендера."""

    def __init__(self):
        self.mode = "sync"

    def initialize(self) -> "RenderModeConfig":
        mode = (
            input(
                f"Выберите режим рендера ({ThreadTypes.SYNC.value}/{ThreadTypes.MULTITHREAD.value}): "
            )
            .strip()
            .lower()
        )
        if mode not in [ThreadTypes.SYNC, ThreadTypes.MULTITHREAD]:
            print("Неверный режим, выбран sync по умолчанию.")
            mode = "sync"
        self.mode = mode
        return self


class FunctionSelector(Config):
    """Конфигурация выбора функций."""

    def __init__(self):
        self.selected_variations = []

    def initialize(self) -> "FunctionSelector":

        print("\nДоступные функции:")
        for i, name in enumerate(VariationList.values):
            print(f"{i + 1}. {name[0]}")

        while True:
            choice = input(
                "Введите номер функции для добавления (или 'g' для генерации): "
            ).strip()
            if choice.lower() == "g":
                break
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(VariationList.values):
                    self.selected_variations.append(VariationList.values[index][1])
                    print(f"Добавлена функция: {VariationList.values[index][0]}")
                else:
                    print("Неверный номер. Попробуйте снова.")
            else:
                print("Введите число или 'g'.")
        if not self.selected_variations:
            print("Ни одна функция не была добавлена.")
            exit()
        return self


class IFSInitializer(Config):
    """Инициализация СИФ."""

    def __init__(self, window_config, symmetry_config, function_selector):
        self.window_config = window_config
        self.symmetry_config = symmetry_config
        self.function_selector = function_selector

    def initialize(self) -> IFS:
        ifs = IFS(
            self.window_config.width,
            self.window_config.height,
            self.symmetry_config.symmetry,
        )
        for variation in self.function_selector.selected_variations:
            a, b, c = (
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(-0.5, 0.5),
            )
            d, e, f = (
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(-0.5, 0.5),
            )
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            ifs.add_transformation(Transformation(a, b, c, d, e, f, variation, color))
        return ifs
