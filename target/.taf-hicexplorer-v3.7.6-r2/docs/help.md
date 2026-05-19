taf-hicexplorer 3.7.6-r2

TAFFISH wrapper for HiCExplorer, a command suite for Hi-C, capture Hi-C, and
Micro-C matrix processing, analysis, conversion, QC, and visualization.

Usage:
  taf-hicexplorer [TAF-APP-OPTION]
  taf-hicexplorer -- [HICEXPLORER-OPTION]
  taf-hicexplorer hicInfo [ARGS...]
  taf-hicexplorer hicPlotMatrix [ARGS...]
  taf-hicexplorer hicBuildMatrix [ARGS...]
  taf-hicexplorer hicCorrectMatrix [SUBCOMMAND] [ARGS...]
  taf-hicexplorer COMMAND [COMMAND-ARGS...]

TAF app options:
  -h, --help       Show this help text
  -v, --version    Show package and command version
  --compile        Print generated shell code instead of running it
  --               Stop parsing TAFFISH wrapper options

Help and examples:
  taf-hicexplorer -- --help
  taf-hicexplorer -- --version
  taf-hicexplorer hicInfo --help
  taf-hicexplorer hicPlotMatrix --help
  taf-hicexplorer hicBuildMatrix --help
  taf-hicexplorer hicCorrectMatrix --help
  taf-hicexplorer hicInfo --matrices matrix.cool
  taf-hicexplorer hicPlotMatrix --matrix matrix.cool --outFileName matrix.png
  taf-hicexplorer hicFindRestSite --fasta genome.fa --searchPattern GATC --outFile sites.bed
  taf-hicexplorer hicConvertFormat --matrices matrix.cool --inputFormat cool --outputFormat h5 --outFileName matrix.h5
  taf-hicexplorer hicCorrectMatrix correct --matrix matrix.h5 --outFileName corrected.h5

Common command groups:
  Pre-processing: hicFindRestSite, hicBuildMatrix, hicBuildMatrixMicroC,
  hicQuickQC, hicQC.
  Matrix handling: hicInfo, hicCorrectMatrix, hicConvertFormat, hicNormalize,
  hicAdjustMatrix, hicMergeMatrixBins, hicSumMatrices, hicCompareMatrices.
  Analysis: hicFindTADs, hicMergeDomains, hicDifferentialTAD, hicDetectLoops,
  hicPCA, hicTransform, hicCorrelate, hicCompartmentalization.
  Visualization: hicPlotMatrix, hicPlotTADs, hicPlotDistVsCounts,
  hicPlotViewpoint, hicAggregateContacts, hicAverageRegions.
  Capture Hi-C: chicQualityControl, chicViewpoint, chicSignificantInteractions,
  chicDifferentialTest, chicPlotViewpoint, chicExportData.

Notes:
  HiCExplorer is a suite. The default hicexplorer command lists the suite and
  reports the upstream version, but real analysis should use explicit command
  mode such as taf-hicexplorer hicInfo ...
  For commands with subcommands, keep the upstream command first, for example
  taf-hicexplorer hicCorrectMatrix correct ...
  Plotting uses Matplotlib Agg for headless containers.
  Samtools, Bedtools, Graphviz, cooler, hicmatrix, hic2cool, pybedtools,
  pyBigWig, pysam, and pyGenomeTracks are included through the pinned runtime.
  Larger alignment/sorting/duplicate workflows should use dedicated apps.

Container:
  image: ghcr.io/taffish/hicexplorer:3.7.6-r2
  platforms: linux/amd64, linux/arm64

Upstream:
  docs:    https://hicexplorer.readthedocs.io/
  source:  https://github.com/deeptools/HiCExplorer
  license: GPL-3.0-or-later
  citation: Wolff et al. 2020, doi:10.1093/nar/gkaa220
