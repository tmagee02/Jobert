import pytest
import scraper.shapes as shapes


@pytest.mark.parametrize(
    'sideLength, expectedArea',
    [
        (5, 25),
        (4, 16),
        (9, 81)
    ]
)
def test_multiple_square_areas(sideLength, expectedArea):
    assert shapes.Square(sideLength).area() == expectedArea