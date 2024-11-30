import logging
import platform

from src.initializers import WindowConfig, SymmetryConfig, GammaConfig, RenderModeConfig, FunctionSelector, \
    IFSInitializer
from src.renderer import MultiThreadRenderer, SyncRenderer

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def setup_renderer(width, height, gamma, use_gamma, mode):
    if mode == "multithread":
        print("Выбран многопоточный режим рендера.")
        return MultiThreadRenderer(width, height, gamma=gamma, use_gamma=use_gamma, num_threads=20)
    else:
        print("Выбран однопоточный режим рендера.")
        return SyncRenderer(width, height, gamma=gamma, use_gamma=use_gamma)


if __name__ == "__main__":
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
        mode=render_mode_config.mode
    )
    renderer.run(ifs, points_per_frame=1000)
