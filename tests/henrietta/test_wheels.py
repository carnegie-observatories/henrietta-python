import pytest

from henrietta.henrietta import Henrietta


@pytest.fixture
def henrietta():
    """Fixture to create a Henrietta instance."""
    h = Henrietta()
    h.open()
    yield h
    h.close()


def test_get_wheels(henrietta):
    """Test the get_wheels method."""
    wheels = henrietta.get_wheels()
    assert isinstance(wheels, dict)
    assert "grism" in wheels
    assert "diffuser" in wheels
    assert "filter" in wheels
    assert "moving" in wheels
    assert isinstance(wheels["moving"], bool)


def test_move_wheel(henrietta):
    """Test the move_wheel method."""
    response = henrietta.move_wheel("grism", "G1")
    assert isinstance(response, dict)
    assert response["grism"] == "G1"
    assert response["moving"] is True
