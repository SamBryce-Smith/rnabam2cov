"""
Helpers to map aligned strands to transcribed strands based on the input RNA-seq library type
"""
from enum import Enum
from typing import Dict


class LibraryType(Enum):
    """RNA-seq library types."""
    FORWARD = "forward"  # FR/fr-secondstrand (ligation)
    REVERSE = "reverse"  # RF/fr-firststrand (dUTP)


def get_strand_mapping(lib_type: str) -> Dict[str, str]:
    """
    Get mapping between genomic strands and transcribed strands based on library type.
    
    Args:
        lib_type: Library type, either 'forward' or 'reverse'
        
    Returns:
        Dictionary mapping genomic strands ('+', '-') to transcribed strands
        
    Raises:
        ValueError: If an unknown library type is provided
    """
    lib_type = LibraryType(lib_type.lower())
    
    if lib_type == LibraryType.FORWARD:
        # FR/fr-secondstrand: first read maps to transcription strand
        return {"+": "+", "-": "-"}
    elif lib_type == LibraryType.REVERSE:
        # RF/fr-firststrand: first read maps to opposite of transcription strand
        return {"+": "-", "-": "+"}
    else:
        raise ValueError(f"Unknown library type: {lib_type}")


def get_output_prefixes(base_prefix: str, lib_type: str) -> Dict[str, str]:
    """
    Generate output file prefixes for each strand based on library type.
    
    Maps the alignment strands to output file prefixes using strand mapping.
    - The "+" alignment strand maps to "forward" or "reverse" based on library type
    - The "-" alignment strand maps to "reverse" or "forward" based on library type
    
    Args:
        base_prefix: Base output prefix
        lib_type: Library type, either 'forward' or 'reverse'
        
    Returns:
        Dictionary mapping genomic strands to output prefixes
    """
    # Get the mapping of genomic strands to transcribed strands
    strand_mapping = get_strand_mapping(lib_type)
    
    # Map the genomic strands to output prefixes based on transcribed strands
    output_prefixes = {}
    for genomic_strand, transcribed_strand in strand_mapping.items():
        if transcribed_strand == "+":
            output_prefixes[genomic_strand] = f"{base_prefix}.plus"
        else:  # transcribed_strand == "-"
            output_prefixes[genomic_strand] = f"{base_prefix}.minus"
    
    return output_prefixes
