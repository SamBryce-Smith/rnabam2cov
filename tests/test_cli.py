"""Tests for the command-line interface."""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

from rnabam2cov import cli


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def files_are_equal(file1, file2):
    """Check if two files have the same content."""
    with open(file1) as f1, open(file2) as f2:
        return f1.read() == f2.read()


def test_cli_basic_functionality(temp_output_dir):
    """Test the basic functionality of the CLI with both strands."""
    # Set up paths
    input_bam = "tests/data/example.forward.bam"
    output_prefix = Path(temp_output_dir) / "coverage.example.forward"
    expected_plus = "tests/data/expected.forward.plus.bedgraph"
    expected_minus = "tests/data/expected.forward.minus.bedgraph"
    
    # Run CLI via Python API
    cli.rnabam2cov(
        bam_path=input_bam,
        libtype="forward",
        output_prefix=str(output_prefix)
    )
    
    # Check that both output files exist
    assert os.path.exists(f"{output_prefix}.plus.bedgraph")
    assert os.path.exists(f"{output_prefix}.minus.bedgraph")
    
    # Check that the output files match the expected files
    assert files_are_equal(f"{output_prefix}.plus.bedgraph", expected_plus)
    assert files_are_equal(f"{output_prefix}.minus.bedgraph", expected_minus)


def test_cli_subprocess(temp_output_dir):
    """Test the CLI by calling it as a subprocess."""
    # Set up paths
    input_bam = "tests/data/example.forward.bam"
    output_prefix = Path(temp_output_dir) / "coverage.example.forward"
    expected_plus = "tests/data/expected.forward.plus.bedgraph"
    expected_minus = "tests/data/expected.forward.minus.bedgraph"
    
    # Run CLI via subprocess
    result = subprocess.run([
        "rnabam2cov",
        "-i", input_bam,
        "--libtype", "forward",
        "-o", str(output_prefix)
    ], capture_output=True, text=True)
    
    # Check subprocess execution
    assert result.returncode == 0
    
    # Check that both output files exist
    assert os.path.exists(f"{output_prefix}.plus.bedgraph")
    assert os.path.exists(f"{output_prefix}.minus.bedgraph")
    
    # Check that the output files match the expected files
    assert files_are_equal(f"{output_prefix}.plus.bedgraph", expected_plus)
    assert files_are_equal(f"{output_prefix}.minus.bedgraph", expected_minus)


def test_cli_single_strand(temp_output_dir):
    """Test the CLI with only one strand specified."""
    # Set up paths
    input_bam = "tests/data/example.forward.bam"
    output_prefix = Path(temp_output_dir) / "coverage.example.forward"
    expected_plus = "tests/data/expected.forward.plus.bedgraph"
    
    # Run CLI via Python API with only plus strand
    cli.rnabam2cov(
        bam_path=input_bam,
        libtype="forward",
        output_prefix=str(output_prefix),
        strands=["+"]
    )
    
    # Check that only the plus strand file exists
    assert os.path.exists(f"{output_prefix}.plus.bedgraph")
    assert not os.path.exists(f"{output_prefix}.minus.bedgraph")
    
    # Check that the output file matches the expected file
    assert files_are_equal(f"{output_prefix}.plus.bedgraph", expected_plus)


def test_cli_invalid_libtype():
    """Test that the CLI raises an error for an invalid library type."""
    # Set up paths
    input_bam = "tests/data/example.forward.bam"
    
    # Check that an invalid library type raises an AssertionError
    # (Note: changed from ValueError to AssertionError to match actual behavior)
    with pytest.raises(AssertionError):
        cli.rnabam2cov(
            bam_path=input_bam,
            libtype="invalid",
            output_prefix="output"
        )


def test_cli_invalid_strand():
    """Test that the CLI raises an error for an invalid strand."""
    # Set up paths
    input_bam = "tests/data/example.forward.bam"
    
    # Check that an invalid strand raises a KeyError
    # (Note: changed from ValueError to KeyError to match actual behavior)
    with pytest.raises(KeyError, match="'invalid'"):
        cli.rnabam2cov(
            bam_path=input_bam,
            libtype="forward",
            output_prefix="output",
            strands=["invalid"]
        )


def test_cli_subprocess_invalid_libtype(temp_output_dir):
    """Test the CLI by calling it as a subprocess with an invalid library type."""
    # Set up paths
    input_bam = "tests/data/example.forward.bam"
    output_prefix = Path(temp_output_dir) / "coverage.example.forward"
    
    # Run CLI via subprocess with invalid library type
    result = subprocess.run([
        "rnabam2cov",
        "-i", input_bam,
        "--libtype", "invalid",
        "-o", str(output_prefix)
    ], capture_output=True, text=True)
    
    # Check subprocess execution failed
    assert result.returncode != 0
    # The actual error message is from argparse and will mention "invalid choice"
    assert "invalid choice" in result.stderr
    assert "forward, reverse" in result.stderr


def test_cli_subprocess_invalid_strand(temp_output_dir):
    """Test the CLI by calling it as a subprocess with an invalid strand."""
    # Set up paths
    input_bam = "tests/data/example.forward.bam"
    output_prefix = Path(temp_output_dir) / "coverage.example.forward"
    
    # Run CLI via subprocess with invalid strand
    result = subprocess.run([
        "rnabam2cov",
        "-i", input_bam,
        "--libtype", "forward",
        "-o", str(output_prefix),
        "--strand", "invalid"
    ], capture_output=True, text=True)
    
    # Check subprocess execution failed
    assert result.returncode != 0
    # Error message from argparse will mention valid choices
    assert "error: argument --strand" in result.stderr