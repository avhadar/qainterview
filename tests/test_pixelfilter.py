"""
Tests for class PixelFilter
"""
import pytest

from main import PixelFilter


class TestPixelFilter:
    """
    Tests for PixelFilter methods
    """
    def test_name(self):
        # Given: a PixelFilter with a specified name
        name = "MyFilter"
        filter = PixelFilter(name=name, specs=[[0, 0, 0], [100, 100, 100], [0, 0, 0]])
        # When: the name is checked
        filter_name = filter.get_name()
        # Then: the specified name is returned
        assert filter_name == name
    
    def test_apply(self):
        pass

    @pytest.mark.parametrize("hue,wavelength", 
                             [(0, 650),
                              (90, 567),
                              (270, 400)])
    def test_convert_hue_to_wavelength(self, hue, wavelength):
        # Given: a PixelFilter and a set of hue - wavelength pairs
        name = "MyFilter"
        filter = PixelFilter(name=name, specs=[[0, 0, 0], [100, 100, 100], [0, 0, 0]])
        # When: the hue is converted to wavelength
        result = filter.convert_hue_to_wavelength(hue)
        # Then: the result matches the provided wavelength
        assert result == wavelength

    @pytest.mark.parametrize("wavelength,hue", 
                             [(650, 0),
                              (567, 90),
                              (400, 270)])
    def test_convert_wavelength_to_hue(self, wavelength, hue):
        # Given: a PixelFilter and a set of wavelength - hue pairs
        name = "MyFilter"
        filter = PixelFilter(name=name, specs=[[0, 0, 0], [100, 100, 100], [0, 0, 0]])
        # When: the wavelength is converted to hue
        result = filter.convert_wavelength_to_hue(wavelength)
        # Then: the result matches the provided hue
        assert result == hue
    

   