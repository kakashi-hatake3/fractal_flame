from src.pixel import Pixel


def test_pixel_creation():
    pixel = Pixel(100, 200, (255, 0, 0))
    assert pixel.x == 100
    assert pixel.y == 200
    assert pixel.color == (255, 0, 0)
