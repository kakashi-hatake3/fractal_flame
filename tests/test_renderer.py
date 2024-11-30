import pytest
from src.renderer import SyncRenderer, MultiThreadRenderer
from src.ifs import IFS
from src.pixel import Pixel


@pytest.fixture
def sync_renderer():
    return SyncRenderer(width=800, height=600, gamma=2.2, use_gamma=True)


@pytest.fixture
def multithread_renderer():
    return MultiThreadRenderer(width=800, height=600, gamma=2.2, use_gamma=True, num_threads=4)


@pytest.fixture
def mock_ifs():
    ifs = IFS(width=800, height=600, symmetry=1)
    ifs.generate_points = lambda _: [Pixel(100, 200, (255, 0, 0))]
    return ifs


def test_sync_renderer_initialization(sync_renderer):
    assert sync_renderer.width == 800
    assert sync_renderer.height == 600
    assert sync_renderer.gamma == 2.2
    assert sync_renderer.use_gamma is True


def test_multithread_renderer_initialization(multithread_renderer):
    assert multithread_renderer.width == 800
    assert multithread_renderer.height == 600
    assert multithread_renderer.num_threads == 4


def test_sync_renderer_render(sync_renderer, mock_ifs):
    sync_renderer.run(mock_ifs, points_per_frame=10, max_iterations=3)
    assert True


def test_multithread_renderer_generate_points(multithread_renderer, mock_ifs):
    points = multithread_renderer.generate_points_multithreaded(mock_ifs, points_per_frame=100)
    assert len(points) > 0
    assert isinstance(points[0], Pixel)


def test_multithread_renderer_run(multithread_renderer, mock_ifs):
    multithread_renderer.run(mock_ifs, points_per_frame=10, max_iterations=3)
    assert True
