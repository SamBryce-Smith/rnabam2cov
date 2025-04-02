#!/bin/bash

echo 'Forward-stranded test BAM...'
# Plus strand with bg option (default)
bedtools genomecov -ibam example.forward.bam -bg -strand + -split -du > expected.forward.plus.bedgraph

# Minus strand with bg option (default)
bedtools genomecov -ibam example.forward.bam -bg -strand - -split -du > expected.forward.minus.bedgraph

# Plus strand with bga option
bedtools genomecov -ibam example.forward.bam -bga -strand + -split -du > expected.forward.plus.bga.bedgraph

# Minus strand with bga option
bedtools genomecov -ibam example.forward.bam -bga -strand - -split -du > expected.forward.minus.bga.bedgraph

# Reverse BAMs
echo 'Reverse-stranded test BAM...'
# Plus strand with bg option (default)
bedtools genomecov -ibam example.reverse.bam -bg -strand + -split -du > expected.reverse.minus.bedgraph

# Minus strand with bg option (default)
bedtools genomecov -ibam example.reverse.bam -bg -strand - -split -du > expected.reverse.plus.bedgraph

# Plus strand with bga option
bedtools genomecov -ibam example.reverse.bam -bga -strand + -split -du > expected.reverse.minus.bga.bedgraph

# Minus strand with bga option
bedtools genomecov -ibam example.reverse.bam -bga -strand - -split -du > expected.reverse.plus.bga.bedgraph
