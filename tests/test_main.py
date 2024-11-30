import pytest
from unittest.mock import MagicMock, patch
from src.main import setup_renderer, main
from src.renderer import SyncRenderer, MultiThreadRenderer


@pytest.mark.parametrize(
    "mode, expected_renderer",
    [
        ("sync", SyncRenderer),
        ("multithread", MultiThreadRenderer),
    ],
)
def test_setup_renderer(mode, expected_renderer):
    renderer = setup_renderer(
        width=800, height=600, gamma=2.2, use_gamma=True, mode=mode
    )
    assert isinstance(renderer, expected_renderer)


@patch("src.main.IFSInitializer")
@patch("src.main.setup_renderer")
@patch("src.main.WindowConfig")
@patch("src.main.SymmetryConfig")
@patch("src.main.GammaConfig")
@patch("src.main.RenderModeConfig")
@patch("src.main.FunctionSelector")
def test_main(
    mock_function_selector,
    mock_render_mode_config,
    mock_gamma_config,
    mock_symmetry_config,
    mock_window_config,
    mock_setup_renderer,
    mock_ifs_initializer,
):
    mock_window = MagicMock()
    mock_window.width = 800
    mock_window.height = 600
    mock_window_config.return_value.initialize.return_value = mock_window

    mock_symmetry = MagicMock()
    mock_symmetry.symmetry = 2
    mock_symmetry_config.return_value.initialize.return_value = mock_symmetry

    mock_gamma = MagicMock()
    mock_gamma.use_gamma = True
    mock_gamma_config.return_value.initialize.return_value = mock_gamma

    mock_render_mode = MagicMock()
    mock_render_mode.mode = "sync"
    mock_render_mode_config.return_value.initialize.return_value = mock_render_mode

    mock_function = MagicMock()
    mock_function.selected_variations = []
    mock_function_selector.return_value.initialize.return_value = mock_function

    mock_ifs = MagicMock()
    mock_ifs_initializer.return_value.initialize.return_value = mock_ifs

    mock_renderer = MagicMock()
    mock_setup_renderer.return_value = mock_renderer

    main()

    mock_window_config.return_value.initialize.assert_called_once()
    mock_symmetry_config.return_value.initialize.assert_called_once()
    mock_gamma_config.return_value.initialize.assert_called_once()
    mock_render_mode_config.return_value.initialize.assert_called_once()
    mock_function_selector.return_value.initialize.assert_called_once()
    mock_ifs_initializer.return_value.initialize.assert_called_once()

    mock_renderer.run.assert_called_once_with(mock_ifs, points_per_frame=1000)
