from concurrent.futures import ThreadPoolExecutor

import pygame
import numpy as np


class Renderer:
    """Интерфейс рендера."""

    def render(self, points) -> None:
        """Отрисовка точек."""
        pass

    def run(self, ifs, points_per_frame) -> None:
        """Запуск рендера."""
        pass


class SyncRenderer(Renderer):
    """Синхронный рендер."""

    def __init__(
        self, width: int, height: int, gamma: float = 2.2, use_gamma: bool = True
    ):
        self.width = width
        self.height = height
        self.gamma = gamma
        self.use_gamma = use_gamma
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("IFS Fractal")
        self.clock = pygame.time.Clock()
        self.buffer = np.zeros((height, width, 3), dtype=np.float64)

    def add_to_buffer(self, points) -> None:
        """Добавление точек в буфер."""
        for pixel in points:
            self.buffer[pixel.y, pixel.x] += np.array(pixel.color, dtype=np.float64)

    def apply_gamma_correction(self) -> np.ndarray:
        """Применение гамма-коррекции."""
        max_val = self.buffer.max()
        if max_val > 0:
            scaled = self.buffer / max_val
            corrected = np.power(scaled, 1 / self.gamma) * 255
            return corrected.astype(np.uint8)
        return self.buffer.astype(np.uint8)

    def render(self, points):
        self.add_to_buffer(points)
        if self.use_gamma:
            corrected_image = self.apply_gamma_correction()
        else:
            max_val = self.buffer.max()
            corrected_image = (
                (self.buffer / max_val * 255).astype(np.uint8)
                if max_val > 0
                else self.buffer.astype(np.uint8)
            )

        corrected_image = np.transpose(corrected_image, (1, 0, 2))
        pygame.surfarray.blit_array(self.screen, corrected_image)
        pygame.display.flip()

    def run(self, ifs, points_per_frame, max_iterations=None):
        iterations = 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            new_points = ifs.generate_points(points_per_frame)
            self.render(new_points)

            if max_iterations is not None:
                iterations += 1
                if iterations >= max_iterations:
                    running = False

            self.clock.tick(60)
        pygame.quit()


class MultiThreadRenderer(SyncRenderer):
    """Многопоточный рендер."""

    def __init__(self, width, height, gamma=2.2, use_gamma=True, num_threads: int = 20):
        super().__init__(width, height, gamma, use_gamma)
        self.num_threads = num_threads

    def generate_points_multithreaded(self, ifs, points_per_frame) -> list:
        """Генерация точек в многопоточном режиме."""
        points_per_thread = points_per_frame // self.num_threads
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [
                executor.submit(ifs.generate_points, points_per_thread)
                for _ in range(self.num_threads)
            ]
            results = []
            for future in futures:
                results.extend(future.result())
        return results

    def run(self, ifs, points_per_frame, max_iterations=None):
        iterations = 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            new_points = self.generate_points_multithreaded(ifs, points_per_frame)

            self.render(new_points)

            if max_iterations is not None:
                iterations += 1
                if iterations >= max_iterations:
                    running = False

            self.clock.tick(60)

        pygame.quit()
