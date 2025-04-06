# rnabam2cov - Library-type aware generation of strand-specific per-base coverage tracks from RNA-seq BAM files

## Installation

### Prerequisites

- [Conda](https://docs.conda.io/en/latest/) or [Mamba](https://mamba.readthedocs.io/en/latest/) (recommended)

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
