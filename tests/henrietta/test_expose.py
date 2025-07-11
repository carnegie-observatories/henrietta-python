import pytest

from henrietta.henrietta import Henrietta


@pytest.fixture
def henrietta():
    """Fixture to create a Henrietta instance."""
    h = Henrietta()
    h.open()
    yield h
    h.close()


@pytest.mark.skip("Skipping test_expose as it requires a real Henrietta instance.")
def test_expose(henrietta):
    """Test the expose method."""
    assert henrietta.expose(1.0)


def test_is_exposing(henrietta):
    """Test the is_exposing property."""
    assert isinstance(henrietta.is_exposing, bool)


def test_exposure_time(henrietta):
    """Test the exposure_time method."""
    assert isinstance(henrietta.exposure_time(5.0), float)
    assert (
        henrietta.exposure_time() == 5.408
    )  # Assuming the default exposure time for 5.0 seconds is rounded to 5.408 seconds
