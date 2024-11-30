import pytest
from src.initializers import (
    WindowConfig,
    SymmetryConfig,
    GammaConfig,
    RenderModeConfig,
    FunctionSelector,
    IFSInitializer,
)
from src.variations import VariationList


@pytest.mark.parametrize(
    "user_inputs, expected_width, expected_height",
    [
        (["1024", "768"], 1024, 768),
        (["800", "600"], 800, 600),
    ],
)
def test_window_config_valid(monkeypatch, user_inputs, expected_width, expected_height):
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))
    config = WindowConfig().initialize()
    assert config.width == expected_width
    assert config.height == expected_height


@pytest.mark.parametrize(
    "user_inputs",
    [
        ["abc", "600"],
        ["1024", "abc"],
        ["abc", "abc"],
    ],
)
def test_window_config_invalid(monkeypatch, user_inputs, capsys):
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))
    with pytest.raises(SystemExit):
        WindowConfig().initialize()
    captured = capsys.readouterr()
    assert "Неверный ввод!" in captured.out


@pytest.mark.parametrize(
    "user_inputs, expected_symmetry",
    [
        (["1"], 1),
        (["3"], 3),
    ],
)
def test_symmetry_config_valid(monkeypatch, user_inputs, expected_symmetry):
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))
    config = SymmetryConfig().initialize()
    assert config.symmetry == expected_symmetry


@pytest.mark.parametrize(
    "user_inputs",
    [
        ["abc"],
        ["0"],
        ["-1"],
    ],
)
def test_symmetry_config_invalid(monkeypatch, user_inputs, capsys):
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))
    with pytest.raises(SystemExit):
        SymmetryConfig().initialize()
    captured = capsys.readouterr()
    assert "Нет такой симметрии!" in captured.out


@pytest.mark.parametrize(
    "user_inputs, expected_use_gamma",
    [
        (["y"], True),
        (["n"], False),
    ],
)
def test_gamma_config(monkeypatch, user_inputs, expected_use_gamma):
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))
    config = GammaConfig().initialize()
    assert config.use_gamma == expected_use_gamma


@pytest.mark.parametrize(
    "user_inputs, expected_mode",
    [
        (["sync"], "sync"),
        (["multithread"], "multithread"),
    ],
)
def test_render_mode_config_valid(monkeypatch, user_inputs, expected_mode):
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))
    config = RenderModeConfig().initialize()
    assert config.mode == expected_mode


@pytest.mark.parametrize(
    "user_inputs",
    [
        ["invalid"],
        ["async"],
    ],
)
def test_render_mode_config_invalid(monkeypatch, user_inputs, capsys):
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))
    config = RenderModeConfig().initialize()
    assert config.mode == "sync"
    captured = capsys.readouterr()
    assert "Неверный режим, выбран sync по умолчанию." in captured.out


@pytest.mark.parametrize(
    "user_inputs, expected_variations",
    [
        (["1", "2", "g"], [VariationList.values[0][1], VariationList.values[1][1]]),
        (["1", "g"], [VariationList.values[0][1]]),
    ],
)
def test_function_selector_valid(monkeypatch, user_inputs, expected_variations):
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))
    selector = FunctionSelector().initialize()
    assert selector.selected_variations == expected_variations


@pytest.mark.parametrize(
    "user_inputs",
    [
        ["g"],
        ["99", "g"],
        ["abc", "g"],
    ],
)
def test_function_selector_invalid(monkeypatch, user_inputs, capsys):
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))
    with pytest.raises(SystemExit):
        FunctionSelector().initialize()
    captured = capsys.readouterr()
    assert "Ни одна функция не была добавлена." in captured.out


@pytest.fixture
def mock_configs():
    window_config = WindowConfig()
    window_config.width = 800
    window_config.height = 600

    symmetry_config = SymmetryConfig()
    symmetry_config.symmetry = 2

    function_selector = FunctionSelector()
    function_selector.selected_variations = [lambda x, y: (x, y)]

    return window_config, symmetry_config, function_selector


def test_ifs_initializer(mock_configs):
    window_config, symmetry_config, function_selector = mock_configs
    initializer = IFSInitializer(window_config, symmetry_config, function_selector)
    ifs = initializer.initialize()

    assert ifs.width == 800
    assert ifs.height == 600
    assert ifs.symmetry == 2
    assert len(ifs.transformations) == 1
