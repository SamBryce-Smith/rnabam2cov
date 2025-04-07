import os
import pytest
from pathlib import Path
import filecmp
from rnabam2cov.coverage import get_stranded_bedgraph, get_file_extension, FileType

# Path to test data directory
DATA_DIR = Path("tests/data")

@pytest.fixture
def forward_bam():
    return DATA_DIR / "example.forward.bam"

@pytest.fixture
def reverse_bam():
    return DATA_DIR / "example.reverse.bam"

@pytest.fixture
def temp_output_dir(tmpdir):
    return Path(tmpdir)

def test_get_stranded_bedgraph_forward_plus(forward_bam, temp_output_dir):
    """Test generating bedgraph for forward-stranded BAM, plus strand."""
    output_prefix = temp_output_dir / "test.forward.plus"
    
    # Generate bedgraph with default settings
    result = get_stranded_bedgraph(
        bam_path=forward_bam,
        strand="+",
        output_prefix=output_prefix,
        split=True,
        du=True,
        bg=True
    )
    
    # Expected output file
    expected_file = DATA_DIR / "expected.forward.plus.bedgraph"
    
    # Check that the output file exists
    assert os.path.exists(result)
    
    # Compare with expected output
    assert filecmp.cmp(result, expected_file), "Generated bedgraph differs from expected"

def test_get_stranded_bedgraph_forward_minus(forward_bam, temp_output_dir):
    """Test generating bedgraph for forward-stranded BAM, minus strand."""
    output_prefix = temp_output_dir / "test.forward.minus"
    
    # Generate bedgraph with default settings
    result = get_stranded_bedgraph(
        bam_path=forward_bam,
        strand="-",
        output_prefix=output_prefix,
        split=True,
        du=True,
        bg=True
    )
    
    # Expected output file
    expected_file = DATA_DIR / "expected.forward.minus.bedgraph"
    
    # Check that the output file exists
    assert os.path.exists(result)
    
    # Compare with expected output
    assert filecmp.cmp(result, expected_file), "Generated bedgraph differs from expected"

def test_get_stranded_bedgraph_reverse_plus(reverse_bam, temp_output_dir):
    """Test generating bedgraph for reverse-stranded BAM, plus strand."""
    output_prefix = temp_output_dir / "test.reverse.plus"
    
    # Generate bedgraph with default settings
    result = get_stranded_bedgraph(
        bam_path=reverse_bam,
        strand="+",
        output_prefix=output_prefix,
        split=True,
        du=True,
        bg=True
    )
    
    # Expected output file
    expected_file = DATA_DIR / "expected.reverse.minus.bedgraph"  # Note: expected file has opposite naming
    
    # Check that the output file exists
    assert os.path.exists(result)
    
    # Compare with expected output
    assert filecmp.cmp(result, expected_file), "Generated bedgraph differs from expected"

def test_get_stranded_bedgraph_reverse_minus(reverse_bam, temp_output_dir):
    """Test generating bedgraph for reverse-stranded BAM, minus strand."""
    output_prefix = temp_output_dir / "test.reverse.minus"
    
    # Generate bedgraph with default settings
    result = get_stranded_bedgraph(
        bam_path=reverse_bam,
        strand="-",
        output_prefix=output_prefix,
        split=True,
        du=True,
        bg=True
    )
    
    # Expected output file
    expected_file = DATA_DIR / "expected.reverse.plus.bedgraph"  # Note: expected file has opposite naming
    
    # Check that the output file exists
    assert os.path.exists(result)
    
    # Compare with expected output
    assert filecmp.cmp(result, expected_file), "Generated bedgraph differs from expected"

# Testing bga option
def test_get_stranded_bedgraph_forward_plus_bga(forward_bam, temp_output_dir):
    """Test generating bedgraph with bga for forward-stranded BAM, plus strand."""
    output_prefix = temp_output_dir / "test.forward.plus.bga"
    
    # Generate bedgraph with bga settings
    result = get_stranded_bedgraph(
        bam_path=forward_bam,
        strand="+",
        output_prefix=output_prefix,
        split=True,
        du=True,
        bg=False,
        bga=True
    )
    
    # Expected output file
    expected_file = DATA_DIR / "expected.forward.plus.bga.bedgraph"
    
    # Check that the output file exists
    assert os.path.exists(result)
    
    # Compare with expected output
    assert filecmp.cmp(result, expected_file), "Generated bedgraph differs from expected"

def test_get_stranded_bedgraph_reverse_minus_bga(reverse_bam, temp_output_dir):
    """Test generating bedgraph with bga for reverse-stranded BAM, minus strand."""
    output_prefix = temp_output_dir / "test.reverse.minus.bga"
    
    # Generate bedgraph with bga settings
    result = get_stranded_bedgraph(
        bam_path=reverse_bam,
        strand="-",
        output_prefix=output_prefix,
        split=True,
        du=True,
        bg=False,
        bga=True
    )
    
    # Expected output file
    expected_file = DATA_DIR / "expected.reverse.plus.bga.bedgraph"  # Note: expected file has opposite naming
    
    # Check that the output file exists
    assert os.path.exists(result)
    
    # Compare with expected output
    assert filecmp.cmp(result, expected_file), "Generated bedgraph differs from expected"

# Test error cases
def test_invalid_strand(forward_bam, temp_output_dir):
    """Test that an invalid strand raises ValueError."""
    output_prefix = temp_output_dir / "test.invalid.strand"
    
    with pytest.raises(ValueError, match="Strand must be"):
        get_stranded_bedgraph(
            bam_path=forward_bam,
            strand="invalid",
            output_prefix=output_prefix
        )

def test_mutually_exclusive_bg_bga(forward_bam, temp_output_dir):
    """Test that using both bg and bga raises ValueError."""
    output_prefix = temp_output_dir / "test.mutually.exclusive"
    
    with pytest.raises(ValueError, match="bg and bga are mutually exclusive"):
        get_stranded_bedgraph(
            bam_path=forward_bam,
            strand="+",
            output_prefix=output_prefix,
            bg=True,
            bga=True
        )

def test_neither_bg_nor_bga(forward_bam, temp_output_dir):
    """Test that using neither bg nor bga raises ValueError."""
    output_prefix = temp_output_dir / "test.neither.bg.nor.bga"
    
    with pytest.raises(ValueError, match="Either bg or bga must be True"):
        get_stranded_bedgraph(
            bam_path=forward_bam,
            strand="+",
            output_prefix=output_prefix,
            bg=False,
            bga=False
        )

def test_mutually_exclusive_5_3_prime(forward_bam, temp_output_dir):
    """Test that using both five_prime and three_prime raises ValueError."""
    output_prefix = temp_output_dir / "test.mutually.exclusive.5.3"
    
    with pytest.raises(ValueError, match="Cannot specify both five_prime and three_prime"):
        get_stranded_bedgraph(
            bam_path=forward_bam,
            strand="+",
            output_prefix=output_prefix,
            five_prime=True,
            three_prime=True
        )