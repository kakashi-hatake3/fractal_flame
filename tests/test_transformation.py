from src.transformation import Transformation
from src.variations import Variations


def test_transformation_apply():
    transformation = Transformation(1, 0, 0, 0, 1, 0, Variations.linear, (255, 0, 0))
    x, y = transformation.apply(1, 2)
    assert x == 1
    assert y == 2
