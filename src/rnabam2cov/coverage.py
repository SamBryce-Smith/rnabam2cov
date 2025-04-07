"""
Functions for extracting strand-specific coverage from RNA-seq BAM files.
"""
from enum import Enum
from pathlib import Path
from typing import Optional, Union
import pybedtools


class FileType(Enum):
    """Valid output file types and their file extensions (without the leading '.')"""
    BEDGRAPH = "bedgraph"


def get_file_extension(file_type: FileType) -> str:
    """
    Get the file extension for a given file type.
    
    Args:
        file_type: The file type
        
    Returns:
        The file extension (without leading dot)
    """
    extensions = {
        FileType.BEDGRAPH: "bedgraph"
    }
    return extensions[file_type]


def get_stranded_bedgraph(
    bam_path: Union[str, Path],
    strand: str,
    output_prefix: str,
    split: bool = True,
    pc: bool = False,
    fs: bool = False,
    du: bool = True,
    ignoreD: bool = False,
    scale: float = 1.0,
    bg: bool = True,
    bga: bool = False,
    max_depth: Optional[int] = None,
    five_prime: bool = False,
    three_prime: bool = False,
    trackline: bool = False,
    trackopts: Optional[str] = None
) -> str:
    """
    Generate a strand-specific bedgraph coverage file from a BAM file.
    
    Args:
        bam_path: Path to the input BAM file
        strand: Strand to extract ('+' or '-')
        output_prefix: Output file prefix
        split: Treat "split" BAM entries as distinct intervals when computing coverage
        pc: Calculate coverage of paired-end fragments (BAM only)
        fs: Force provided fragment size instead of read length (BAM only)
        du: Change strand of the mate read (so both reads from same strand) (BAM only)
        ignoreD: Ignore local deletions (CIGAR "D" operations) in BAM entries
        scale: Scale coverage by a constant factor
        bg: Report coverage in bedgraph format
        bga: Report coverage in bedgraph format, including regions with zero coverage
        max_depth: Combine all positions with depth >= max_depth
        five_prime: Calculate coverage of 5' positions only
        three_prime: Calculate coverage of 3' positions only
        trackline: Add UCSC track line definition
        trackopts: Additional track line parameters
        
    Returns:
        Path to the generated bedgraph file
        
    Raises:
        ValueError: If both bg and bga are True, if strand is not '+' or '-',
                   or if incompatible options are selected
    """
    if strand not in ['+', '-']:
        raise ValueError(f"Strand must be '+' or '-', got '{strand}'")
    
    if bg and bga:
        raise ValueError("bg and bga are mutually exclusive")
    
    if not bg and not bga:
        raise ValueError("Either bg or bga must be True to generate a bedgraph file")
    
    # Check for mutually exclusive 5'/3' options
    if five_prime and three_prime:
        raise ValueError("Cannot specify both five_prime and three_prime")
    
    # Initialize bedtools object with the BAM file
    bt = pybedtools.BedTool(str(bam_path))
    
    # Build the arguments for genome_coverage
    kwargs = {
        'strand': strand,
    }
    
    # Add optional arguments if they are set
    if split:
        kwargs['split'] = True
    if pc:
        kwargs['pc'] = True
    if fs:
        kwargs['fs'] = True
    if du:
        kwargs['du'] = True
    if ignoreD:
        kwargs['ignoreD'] = True
    if scale != 1.0:
        kwargs['scale'] = scale
    if bg:
        kwargs['bg'] = True
    if bga:
        kwargs['bga'] = True
    if max_depth:
        kwargs['max'] = max_depth
    if five_prime:
        kwargs['5'] = True
    if three_prime:
        kwargs['3'] = True
    if trackline:
        kwargs['trackline'] = True
    if trackopts:
        kwargs['trackopts'] = trackopts
    
    # Generate the coverage file
    result = bt.genome_coverage(**kwargs)
    
    # Define output file path
    output_path = f"{output_prefix}.{get_file_extension(FileType.BEDGRAPH)}"
    
    # Save to file
    result.saveas(output_path)
    
    return output_path

def get_stranded_coverage(
    bam_path: Union[str, Path],
    strand: str,
    output_prefix: str,
    file_type: FileType = FileType.BEDGRAPH,
    **kwargs
) -> str:
    """
    Generate strand-specific coverage file from a BAM file.
    
    This function is a wrapper around get_stranded_bedgraph that can be
    extended to support other file types in the future.
    
    Args:
        bam_path: Path to the input BAM file
        strand: Strand to extract ('+' or '-')
        output_prefix: Output file prefix
        file_type: Type of output file
        **kwargs: Additional arguments to pass to the specific file type generator (e.g. get_stranded_bedgraph)
        
    Returns:
        Path to the generated coverage file
        
    Raises:
        ValueError: If an unsupported file type is provided
    """
    # Note: when have multiple valid filetypes, switch to an 'filetype in FileType' operation
    if file_type == FileType.BEDGRAPH:
        return get_stranded_bedgraph(bam_path, strand, output_prefix, **kwargs)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")