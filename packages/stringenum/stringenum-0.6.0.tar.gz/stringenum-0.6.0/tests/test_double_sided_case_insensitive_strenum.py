from __future__ import annotations

import pytest

from stringenum import DoubleSidedCaseInsensitiveStrEnum


class Color(DoubleSidedCaseInsensitiveStrEnum):
    RED_COLOR = "Red"
    BLUE_SKY = "Blue"
    GREEN_GRASS = "Green"


def test_case_insensitive_getitem_by_name() -> None:
    assert Color["RED_COLOR"] is Color.RED_COLOR
    assert Color["red_color"] is Color.RED_COLOR
    assert Color["ReD_CoLoR"] is Color.RED_COLOR

    assert Color["BLUE_SKY"] is Color.BLUE_SKY
    assert Color["blue_sky"] is Color.BLUE_SKY
    assert Color["BlUe_SkY"] is Color.BLUE_SKY

    assert Color["GREEN_GRASS"] is Color.GREEN_GRASS
    assert Color["green_grass"] is Color.GREEN_GRASS
    assert Color["GreEn_GrAsS"] is Color.GREEN_GRASS


def test_case_insensitive_getitem_by_value() -> None:
    assert Color["Red"] is Color.RED_COLOR
    assert Color["red"] is Color.RED_COLOR
    assert Color["ReD"] is Color.RED_COLOR

    assert Color["Blue"] is Color.BLUE_SKY
    assert Color["blue"] is Color.BLUE_SKY
    assert Color["BlUe"] is Color.BLUE_SKY

    assert Color["Green"] is Color.GREEN_GRASS
    assert Color["green"] is Color.GREEN_GRASS
    assert Color["GreEn"] is Color.GREEN_GRASS


def test_membership() -> None:
    assert Color.RED_COLOR in Color
    assert "Red" in Color
    assert "red" in Color
    assert "GREEN_GRASS" in Color
    assert "GREEN_grass" in Color
    assert "pink" not in Color
    assert None not in Color
    assert object() not in Color
    assert 121212 not in Color


def test_case_insensitive_invalid_key() -> None:
    with pytest.raises(KeyError):
        Color["YELLOW"]

    with pytest.raises(KeyError):
        Color["yElLoW"]

    with pytest.raises(KeyError):
        Color[None]  # type: ignore[misc]


def test_case_insensitive_lookup_by_name() -> None:
    assert Color("red_Color") is Color.RED_COLOR
    assert Color("red_color") is Color.RED_COLOR
    assert Color("blue_SKY") is Color.BLUE_SKY
    assert Color("BLUE_SKY") is Color.BLUE_SKY
    assert Color("grEEn_GRASS") is Color.GREEN_GRASS
    assert Color("green_grass") is Color.GREEN_GRASS


def test_case_insensitive_lookup_by_value() -> None:
    assert Color("red") is Color.RED_COLOR
    assert Color("RED") is Color.RED_COLOR
    assert Color("blue") is Color.BLUE_SKY
    assert Color("BLUE") is Color.BLUE_SKY
    assert Color("green") is Color.GREEN_GRASS
    assert Color("GREEN") is Color.GREEN_GRASS


def test_value_error_on_invalid_lookup() -> None:
    with pytest.raises(ValueError):
        Color("YELLOW")

    with pytest.raises(ValueError):
        Color("yellow")

    with pytest.raises(ValueError):
        Color(None)  # type: ignore[arg-type]


def test_unique_on_each_side() -> None:
    class ValidColor(DoubleSidedCaseInsensitiveStrEnum):
        RED_COLOR = "RED_COLOR"
        BLUE_SKY = "BLUE_SKY"

    assert ValidColor.RED_COLOR is ValidColor.RED_COLOR


def test_unique_values() -> None:
    with pytest.raises(ValueError):

        class InvalidColor(DoubleSidedCaseInsensitiveStrEnum):
            RED_COLOR = "Red"
            BLUE_SKY = "Blue"
            BLUE_DUPLICATE = "Blue"


def test_unique_values_case_insensitively() -> None:
    with pytest.raises(ValueError):

        class InvalidColor(DoubleSidedCaseInsensitiveStrEnum):
            RED_COLOR = "Red"
            BLUE_SKY = "Blue"
            BLUE_DUPLICATE = "blue"


def test_unique_names() -> None:
    with pytest.raises(TypeError):

        class InvalidColor(DoubleSidedCaseInsensitiveStrEnum):
            RED = "Red"
            BLUE = "Blue"
            BLUE = "Green"  # type: ignore[misc]


def test_unique_names_case_insensitively() -> None:
    with pytest.raises(ValueError):

        class InvalidColor(DoubleSidedCaseInsensitiveStrEnum):
            RED = "Red"
            BLUE = "Blue"
            blue = "Green"
