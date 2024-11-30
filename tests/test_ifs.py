import pytest
from src.ifs import IFS
from src.pixel import Pixel
from src.transformation import Transformation
from src.variations import Variations


@pytest.fixture
def ifs_instance():
    return IFS(width=800, height=600, symmetry=2)


def test_add_transformation(ifs_instance):
    transformation = Transformation(1, 0, 0, 0, 1, 0, Variations.linear, (255, 0, 0))
    ifs_instance.add_transformation(transformation)
    assert len(ifs_instance.transformations) == 1


def test_generate_points(ifs_instance):
    transformation = Transformation(1, 0, 0, 0, 1, 0, Variations.linear, (255, 0, 0))
    ifs_instance.add_transformation(transformation)

    points = ifs_instance.generate_points(10)
    assert len(points) > 0
    assert isinstance(points[0], Pixel)
