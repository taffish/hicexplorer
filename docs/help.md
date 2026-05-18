taf-hicexplorer 3.7.6-r1

TAFFISH wrapper for HiCExplorer, a command-line suite for Hi-C, capture Hi-C,
and Micro-C matrix processing, analysis, conversion, QC, and visualization.

Usage:
  taf-hicexplorer [TAF-APP-OPTION]
  taf-hicexplorer -- [HICEXPLORER-OPTION]
  taf-hicexplorer hicInfo [ARGS...]
  taf-hicexplorer hicPlotMatrix [ARGS...]
  taf-hicexplorer hicBuildMatrix [ARGS...]
  taf-hicexplorer hicCorrectMatrix [SUBCOMMAND] [ARGS...]
  taf-hicexplorer <COMMAND> [COMMAND-ARGS...]

TAF app options:
  -h, --help       Show this help text
  -v, --version    Show package and command version
  --compile        Print generated shell code instead of running it
  --               Stop parsing TAFFISH wrapper options

Upstream help:
  taf-hicexplorer -- --help
  taf-hicexplorer -- --version
  taf-hicexplorer hicInfo --help
  taf-hicexplorer hicPlotMatrix --help
  taf-hicexplorer hicBuildMatrix --help
  taf-hicexplorer hicCorrectMatrix --help
  taf-hicexplorer chicViewpoint --help

Recommended examples:
  taf-hicexplorer hicInfo --matrices matrix.cool
  taf-hicexplorer hicPlotMatrix --matrix matrix.cool --outFileName matrix.png
  taf-hicexplorer hicFindRestSite --fasta genome.fa --searchPattern GATC --outFile sites.bed
  taf-hicexplorer hicConvertFormat --matrices matrix.cool --inputFormat cool --outputFormat h5 --outFileName matrix.h5
  taf-hicexplorer hicCorrectMatrix correct --matrix matrix.h5 --outFileName corrected.h5

Common command groups:
  Pre-processing:
    hicFindRestSite
    hicBuildMatrix
    hicBuildMatrixMicroC
    hicQuickQC
    hicQC

  Matrix handling:
    hicInfo
    hicCorrectMatrix
    hicConvertFormat
    hicNormalize
    hicAdjustMatrix
    hicMergeMatrixBins
    hicSumMatrices
    hicCompareMatrices

  Analysis:
    hicFindTADs
    hicMergeDomains
    hicDifferentialTAD
    hicDetectLoops
    hicMergeLoops
    hicPCA
    hicTransform
    hicCorrelate
    hicCompartmentalization
    hicInterIntraTAD
    hicTADClassifier
    hicTrainTADClassifier

  Visualization:
    hicPlotMatrix
    hicPlotTADs
    hicPlotDistVsCounts
    hicPlotViewpoint
    hicAggregateContacts
    hicAverageRegions
    hicPlotAverageRegions
    hicPlotSVL

  Capture Hi-C:
    chicQualityControl
    chicViewpointBackgroundModel
    chicViewpoint
    chicSignificantInteractions
    chicAggregateStatistic
    chicDifferentialTest
    chicPlotViewpoint
    chicExportData

Notes:
  - HiCExplorer is a command suite. The default upstream command is
    "hicexplorer", which lists the suite and reports the upstream version.
  - For real analysis, prefer explicit command mode such as
    "taf-hicexplorer hicInfo ..." or "taf-hicexplorer hicPlotMatrix ...".
  - If an upstream command has its own subcommands, keep the upstream command
    name first, for example "taf-hicexplorer hicCorrectMatrix correct ...".
  - Plotting is configured for headless containers with Matplotlib Agg.
  - Samtools, Bedtools, Graphviz, cooler, hicmatrix, hic2cool, pybedtools,
    pyBigWig, pysam, and pyGenomeTracks are available in the image as part of
    the pinned Bioconda runtime environment.
  - Larger workflows should still use dedicated TAFFISH apps for upstream
    alignment, sorting, duplicate handling, and other command-level steps.
  - Native image platforms: linux/amd64 and linux/arm64.

Container:
  image: ghcr.io/taffish/hicexplorer:3.7.6-r1
  supported backends: apptainer, podman, docker

Upstream:
  project: HiCExplorer
  version: 3.7.6
  homepage: https://hicexplorer.readthedocs.io/
  source: https://github.com/deeptools/HiCExplorer
  license: GPL-3.0-or-later
  main citation: Wolff et al. 2020, doi: 10.1093/nar/gkaa220
