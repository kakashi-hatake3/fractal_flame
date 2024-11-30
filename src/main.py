import logging

from src.initializers import (
    WindowConfig,
    SymmetryConfig,
    GammaConfig,
    RenderModeConfig,
    FunctionSelector,
    IFSInitializer,
)
from src.renderer import MultiThreadRenderer, SyncRenderer, Renderer

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def setup_renderer(
    width: int, height: int, gamma: float, use_gamma: bool, mode: str
) -> Renderer:
    """Сетапит рендерер в зависимости от выбранного режима рендера."""
    if mode == "multithread":
        print("Выбран многопоточный режим рендера.")
        return MultiThreadRenderer(
            width, height, gamma=gamma, use_gamma=use_gamma, num_threads=20
        )
    else:
        print("Выбран однопоточный режим рендера.")
        return SyncRenderer(width, height, gamma=gamma, use_gamma=use_gamma)


def main() -> None:
    """Запуск программы."""
    window_config = WindowConfig().initialize()
    symmetry_config = SymmetryConfig().initialize()
    gamma_config = GammaConfig().initialize()
    render_mode_config = RenderModeConfig().initialize()
    function_selector = FunctionSelector().initialize()

    ifs_initializer = IFSInitializer(window_config, symmetry_config, function_selector)
    ifs = ifs_initializer.initialize()

    renderer = setup_renderer(
        window_config.width,
        window_config.height,
        gamma=2.2,
        use_gamma=gamma_config.use_gamma,
        mode=render_mode_config.mode,
    )
    renderer.run(ifs, points_per_frame=1000)


if __name__ == "__main__":
    main()
