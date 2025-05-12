# rnabam2cov - Library-type aware generation of strand-specific per-base coverage tracks from RNA-seq BAM files

[![DOI](https://zenodo.org/badge/957922139.svg)](https://doi.org/10.5281/zenodo.15390037)

A convenient wrapper around bedtools genomecov to compute library-type aware, strand-specific per-base coverage from RNA-seq BAM files.

## Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installation Instructions](#installation-instructions)
- [Usage](#usage)
  - [Command Line Usage](#command-line-usage)
  - [Python API Usage](#python-api-usage)
- [Notes](#notes)

## Installation

### Prerequisites

- [Conda](https://docs.conda.io/en/latest/) or [Mamba](https://mamba.readthedocs.io/en/latest/)

### Installation Instructions

```bash
# Clone the repository
git clone https://github.com/SamBryce-Smith/rnabam2cov.git
cd rnabam2cov
```

For regular use, use the `rnabam2cov.yaml` environment file:

```bash
# Create and activate the environment using mamba
mamba env create -f rnabam2cov.yaml
mamba activate rnabam2cov

# Verify installation
rnabam2cov --help
```

For development, please use the `rnabam2cov_dev.yaml` file (for editable install and development dependencies):

```bash
# Create and activate the development environment
mamba env create -f rnabam2cov_dev.yaml
mamba activate rnabam2cov_dev
```

It is also possible to install via `pip install` / `uv pip install` directly from github, although this is not recommended because it will not install bedtools:

```bash
# for installing at specific commit/release tag, suffix the URL with @<commit hash/tag>
pip install git+https://github.com/SamBryce-Smith/rnabam2cov
# verify bedtools is installed
python -c "import rnabam2cov, pybedtools; a = pybedtools.example_bedtool('a.bed'); b = pybedtools.example_bedtool('b.bed'); print(a.intersect(b))"
chr1    155     200     feature2        0       +
chr1    155     200     feature3        0       -
chr1    900     901     feature4        0       +
```

## Usage

### Command Line Usage

To generate strand-specific RNA-seq coverage files (in BedGraph format) from a BAM file:

```bash
rnabam2cov -i tests/data/example.forward.bam --libtype forward -o output/coverage
```

This will produce two BedGraph files (one per strand) - `output/coverage.plus.bedgraph` and `output/coverage.minus.bedgraph`

To generate coverage for only for a single specific strand, set the `--strand` argument with `+` or `-`. For example, to just generate coverage on the plus strand:

```bash
rnabam2cov -i tests/data/example.forward.bam --libtype forward -o output/coverage --strand +
```

This will produce only one file: `output/coverage.plus.bedgraph`

the `--libtype` argument allows you to specify between the two strand-specific library types used for strand-specific RNA-seq:

- `forward` (FR): The aligned strand of the first mate (leftmost) in a read pair corresponds to the transcribed strand of origin. Common with ligation-based methods
- `reverse` (RF): The aligned strand of the second mate (rightmost) in a read pair corresponds to the transcribed strand of origin. Common with dUTP-based methods (most Illumina RNA-seq kits)

This tool does not check that the provided libtype is corroborated in the input BAM file. If you don't know the library type, there are tools to infer it from FASTQs (e.g. [how_are_we_stranded_here](https://github.com/signalbash/how_are_we_stranded_here)) or BAM files (e.g. [RSeQC's infer_experiment.py](https://rseqc.sourceforge.net/#infer-experiment-py)). For more details, I recommend the [Griffith lab's guide](https://rnabio.org/module-09-appendix/0009/12/01/StrandSettings/).

By default, the following bedtools genomecov options are enabled to match preferences for RNA-seq data:

- `--split`: Read the CIGAR string to compute splice/gap-aware coverage
- `--du`: Change strand of mate read so both reads contribute to coverage on the same strand
- `--bg`: Report coverage in BedGraph format (non-zero positions only)

These and all other bedtools genomecov arguments (as of v2.31.0) can be toggled at the command line (see the help message):

```bash
# any of the following options work
rnabam2cov --help
rnabam2cov -h
rnabam2cov
```

### Python API Usage

You can also use rnabam2cov directly in your Python code:

```python
from rnabam2cov.cli import rnabam2cov

# Generate coverage files for both strands (default behavior)
output_files = rnabam2cov(
    bam_path="tests/data/example.forward.bam",
    libtype="forward",
    output_prefix="output/coverage"
)

# Print the paths to the generated files
print(output_files)
# ['output/coverage.plus.bedgraph', 'output/coverage.minus.bedgraph']

# Generate coverage for only the plus strand
plus_only = rnabam2cov(
    bam_path="tests/data/example.forward.bam",
    libtype="forward",
    output_prefix="output/coverage_plus_only",
    strands=["+"]
)

print(plus_only)
# ['output/coverage_plus_only.plus.bedgraph']
```

## Notes

- It appears that bedtools genomecov includes secondary alignments in the computed coverage ([GitHub issue 1061](https://github.com/arq5x/bedtools2/issues/1061)), although it's unclear exactly how the counting is done. If you want to compute coverage of primary alignments only, you will need to prefilter the BAM file.
- The `-pc` and `-split` flag are currently incompatible - cigar strings (i.e. splicing) is ignored when the `-pc` flag is passed (I reproduced this, but initially reported in [GitHub issue 516](https://github.com/arq5x/bedtools2/issues/516)). Although I want to double-check, I expect this means that positions in fragments that are covered by both mates will be double-counted (i.e. coverage is per-read, not per-fragment). I do not see an obvious way to get around this without a non-bedtools implementation.
- This package calls bedtools genomecov via pybedtools - this will mean use of temporary files (by default under `/tmp`). pybedtools provides a way to set the temporary directory for the session, but I haven't exposed this to the CLI yet.
