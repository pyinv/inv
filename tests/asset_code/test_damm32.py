"""Test the Damm32 asset code."""

from damm32 import Damm32
from pytest import raises

from inv.asset_code.damm32 import Damm32AssetCode


def test_instantiation() -> None:
    """Test that the class instantiates correctly."""
    Damm32AssetCode("ABC", "AA")


def test_validation() -> None:
    """Test that we validate the org and prefix correctly."""
    VALID_ORGS = ["ABC", "DEF", "DDD"]
    INVALID_ORGS = ["", "AA", " AAA", "A2E", "&", "AAAA"]

    for valid in VALID_ORGS:
        Damm32AssetCode(valid, "AA")

    for invalid in INVALID_ORGS:
        with raises(ValueError):
            Damm32AssetCode(invalid, "AA")

    VALID_PREFIXES = ["AA", "A2", "ZZ", "Z3"]
    INVALID_PREFIXES = ["A9", "99", "B1", "B8", "", "AAA", "B"]

    for valid in VALID_PREFIXES:
        Damm32AssetCode("AAA", valid)

    for invalid in INVALID_PREFIXES:
        with raises(ValueError):
            Damm32AssetCode("AAA", invalid)


def test__generate_code() -> None:
    """Test that we generate valid codes."""
    d32 = Damm32()
    d32ac = Damm32AssetCode("ABC", "AA")

    single = d32ac.generate()
    assert len(single) == 1
    assert d32.verify("ABC" + single[0])

    multiple = d32ac.generate(quantity=100)
    assert len(multiple) == 100
    assert all(d32.verify(x) for x in multiple)


def test__verify_code() -> None:
    """Test that we can verify codes."""
    ORG = "SRO"
    VALID_CODES = [
        "AA3YZ2",
        "AABTTJ",
        "AAAQHA",
        "AAB3RI",
        "AAVWHB",
        "AAL5Z2",
    ]
    INVALID_CODES = [
        "A93YZ2",
        "AABTTU",
        "AA6QHA",
        "AAB3HI",
        "AAVDHB",
        "AAL542",
    ]

    d32ac = Damm32AssetCode(ORG, "AB")

    for valid in VALID_CODES:
        assert d32ac.verify(valid)

    for invalid in INVALID_CODES:
        assert not d32ac.verify(invalid)
