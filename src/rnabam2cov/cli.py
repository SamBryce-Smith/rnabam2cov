"""
Command line interface for rnabam2cov.
"""
import argparse
import sys
from pathlib import Path
from typing import List, Optional

from rnabam2cov.coverage import FileType, get_stranded_coverage
from rnabam2cov.strandedness import LibraryType, get_output_prefixes


def rnabam2cov(
    bam_path: str,
    libtype: str,
    output_prefix: str,
    strands: List[str] = ["+", "-"],
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
    trackopts: Optional[str] = None,
    file_type: FileType = FileType.BEDGRAPH
) -> List[str]:
    """
    Generate strand-specific coverage files from a BAM file.
    
    Args:
        bam_path: Path to input BAM file
        libtype: Library type ('forward' or 'reverse')
        output_prefix: Prefix for output files
        strands: List of strands to process ('+' and/or '-')
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
        file_type: Type of output file
        
    Returns:
        List of paths to generated coverage files
    """
    
    assert libtype in LibraryType

    # Get output prefixes based on library type
    output_prefixes = get_output_prefixes(output_prefix, libtype)
    
    output_files = []
    
    for strand in strands:
        # Get the appropriate output prefix for this strand based on library type
        strand_prefix = output_prefixes[strand]
        
        # Generate the coverage file for this strand
        output_file = get_stranded_coverage(
            bam_path=bam_path,
            strand=strand,
            output_prefix=strand_prefix,
            file_type=file_type,
            split=split,
            pc=pc,
            fs=fs,
            du=du,
            ignoreD=ignoreD,
            scale=scale,
            bg=bg,
            bga=bga,
            max_depth=max_depth,
            five_prime=five_prime,
            three_prime=three_prime,
            trackline=trackline,
            trackopts=trackopts
        )
        
        output_files.append(output_file)
    
    return output_files


def parse_args(args=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate strand-specific coverage files from RNA-seq BAM files."
    )
    
    # Required arguments
    parser.add_argument("-i", "--input", required=True, help="Input BAM file")
    parser.add_argument(
        "--libtype", 
        required=True, 
        choices=["forward", "reverse"], 
        help="Library strandedness type (forward=FR/fr-secondstrand, reverse=RF/fr-firststrand)"
    )
    parser.add_argument(
        "-o", "--output-prefix", 
        required=True,
        help="Prefix for output files (will generate <prefix>.plus.bedgraph and <prefix>.minus.bedgraph)"
    )
    
    # Optional arguments
    parser.add_argument(
        "--strand", 
        choices=["+", "-"], 
        nargs="+", 
        default=["+", "-"],
        help="Strands to process (default: both '+' and '-')"
    )
    
    # Coverage options from get_stranded_bedgraph
    parser.add_argument(
        "--no-split", 
        action="store_false", 
        dest="split",
        help="Do not treat split BAM entries as distinct intervals when computing coverage (WARNING: NOT RECOMMENDED)"
    )
    parser.add_argument(
        "--pc", 
        action="store_true", 
        help="Calculate coverage of paired-end fragments"
    )
    parser.add_argument(
        "--fs", 
        action="store_true", 
        help="Force provided fragment size instead of read length"
    )
    parser.add_argument(
        "--no-du", 
        action="store_false", 
        dest="du",
        help="Do not change strand of the mate read (WARNING: NOT RECOMMENDED)"
    )
    parser.add_argument(
        "--ignoreD", 
        action="store_true", 
        help="Ignore local deletions (CIGAR 'D' operations) in BAM entries"
    )
    parser.add_argument(
        "--scale", 
        type=float, 
        default=1.0,
        help="Scale coverage by a constant factor (default: 1.0)"
    )
    
    # Mutually exclusive group for bedgraph options
    bg_group = parser.add_mutually_exclusive_group()
    bg_group.add_argument(
        "--bg", 
        action="store_true",
        dest="bg", 
        default=True,
        help="Report coverage in bedgraph format (default)"
    )
    bg_group.add_argument(
        "--bga", 
        action="store_true",
        dest="bga",
        help="Report coverage in bedgraph format, including regions with zero coverage"
    )
    
    parser.add_argument(
        "--max-depth", 
        type=int, 
        help="Combine all positions with depth >= max-depth"
    )
    
    # Mutually exclusive group for 5'/3' options
    end_group = parser.add_mutually_exclusive_group()
    end_group.add_argument(
        "--five-prime", 
        action="store_true", 
        help="Calculate coverage of 5' positions only"
    )
    end_group.add_argument(
        "--three-prime", 
        action="store_true", 
        help="Calculate coverage of 3' positions only"
    )
    
    parser.add_argument(
        "--trackline", 
        action="store_true", 
        help="Add UCSC track line definition"
    )
    parser.add_argument(
        "--trackopts", 
        help="Additional track line parameters (e.g. 'name=\"My Track\" visibility=2')"
    )
    
    # exit with help message if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()
    
    return parser.parse_args(args)


def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    try:
        # Convert input path to Path object
        bam_path = Path(args.input)
        if not bam_path.exists():
            raise FileNotFoundError(f"Input BAM file not found: {bam_path}")
        
        # Set bg/bga based on args
        if args.bga:
            bg = False
            bga = True
        else:
            bg = True
            bga = False
            
        # Call the wrapper function
        output_files = rnabam2cov(
            bam_path=str(bam_path),
            libtype=args.libtype,
            output_prefix=args.output_prefix,
            strands=args.strand,
            split=args.split,
            pc=args.pc,
            fs=args.fs,
            du=args.du,
            ignoreD=args.ignoreD,
            scale=args.scale,
            bg=bg,
            bga=bga,
            max_depth=args.max_depth,
            five_prime=args.five_prime,
            three_prime=args.three_prime,
            trackline=args.trackline,
            trackopts=args.trackopts
        )
        
        print(f"Generated {len(output_files)} coverage files:")
        for output_file in output_files:
            print(f"  {output_file}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()