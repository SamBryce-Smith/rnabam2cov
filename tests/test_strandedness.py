"""
Tests for the strandedness module.
"""
import pytest

from src.rnabam2cov.strandedness import (
    LibraryType,
    get_strand_mapping,
    get_output_prefixes,
)


def test_library_type_enum():
    """Test the LibraryType enum."""
    assert LibraryType.FORWARD.value == "forward"
    assert LibraryType.REVERSE.value == "reverse"


def test_get_strand_mapping_forward():
    """Test get_strand_mapping with forward strandedness."""
    mapping = get_strand_mapping("forward")
    assert mapping == {"+": "+", "-": "-"}


def test_get_strand_mapping_reverse():
    """Test get_strand_mapping with reverse strandedness."""
    mapping = get_strand_mapping("reverse")
    assert mapping == {"+": "-", "-": "+"}


def test_get_strand_mapping_case_insensitive():
    """Test get_strand_mapping is case-insensitive."""
    assert get_strand_mapping("FORWARD") == get_strand_mapping("forward")
    assert get_strand_mapping("REVERSE") == get_strand_mapping("reverse")


def test_get_strand_mapping_invalid():
    """Test get_strand_mapping with invalid strandedness."""
    with pytest.raises(ValueError):
        get_strand_mapping("invalid")


def test_get_output_prefixes_forward():
    """Test get_output_prefixes with forward strandedness."""
    prefixes = get_output_prefixes("test", "forward")
    assert prefixes == {"+": "test.plus", "-": "test.minus"}


def test_get_output_prefixes_reverse():
    """Test get_output_prefixes with reverse strandedness."""
    prefixes = get_output_prefixes("test", "reverse")
    # In reverse library type, genomic "+" strand corresponds to transcribed "-" strand
    # and genomic "-" strand corresponds to transcribed "+" strand
    assert prefixes == {"+": "test.minus", "-": "test.plus"}


def test_get_output_prefixes_with_path():
    """Test get_output_prefixes with a path in the prefix."""
    prefixes = get_output_prefixes("/path/to/test", "forward")
    assert prefixes == {"+": "/path/to/test.plus", "-": "/path/to/test.minus"}