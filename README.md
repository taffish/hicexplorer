# hicexplorer

TAFFISH wrapper for [HiCExplorer](https://github.com/deeptools/HiCExplorer)
3.7.6, a command-line suite for processing, normalizing, analyzing,
converting, and visualizing Hi-C, capture Hi-C, and Micro-C contact matrices.

This app packages the Bioconda HiCExplorer 3.7.6 environment with its Python
runtime stack and common runtime helpers such as Samtools, Bedtools, and
Graphviz. It is intended as a portable command-level environment, not as a
workflow replacement.

## Installation

Install from the public TAFFISH Hub index:

```sh
taf install hicexplorer
```

Install the exact release:

```sh
taf install hicexplorer 3.7.6-r1
```

For local testing before publication:

```sh
taf build
./target/taf-hicexplorer-v3.7.6-r1 --help
```

## Usage

HiCExplorer is a command suite. The default command is the upstream
`hicexplorer` command, which prints the upstream command list:

```sh
taf-hicexplorer -- --help
taf-hicexplorer -- --version
```

For real work, prefer explicit command mode:

```sh
taf-hicexplorer hicInfo --matrices matrix.cool
taf-hicexplorer hicPlotMatrix --matrix matrix.cool --outFileName matrix.png
taf-hicexplorer hicCorrectMatrix correct --matrix matrix.h5 --outFileName corrected.h5
taf-hicexplorer hicConvertFormat --matrices matrix.cool --inputFormat cool --outputFormat h5 --outFileName matrix.h5
```

Because this app uses TAFFISH command mode, `taf-hicexplorer hicInfo ...` runs
`hicInfo ...` directly inside the same container. Do not shorten upstream
subcommands into `taf-hicexplorer Info ...`; use the real HiCExplorer command
name.

## Common Commands

Pre-processing and matrix construction:

```sh
taf-hicexplorer hicFindRestSite --fasta genome.fa --searchPattern GATC --outFile sites.bed
taf-hicexplorer hicBuildMatrix --samFiles reads_R1.bam reads_R2.bam --binSize 10000 --outFileName matrix.h5 --QCfolder qc
taf-hicexplorer hicBuildMatrixMicroC --help
taf-hicexplorer hicQuickQC --help
taf-hicexplorer hicQC --help
```

Matrix correction, conversion, and inspection:

```sh
taf-hicexplorer hicInfo --matrices matrix.h5
taf-hicexplorer hicCorrectMatrix correct --matrix matrix.h5 --outFileName corrected.h5
taf-hicexplorer hicConvertFormat --matrices matrix.cool --inputFormat cool --outputFormat h5 --outFileName matrix.h5
taf-hicexplorer hicNormalize --help
taf-hicexplorer hicAdjustMatrix --help
```

Analysis and visualization:

```sh
taf-hicexplorer hicPlotMatrix --matrix matrix.h5 --outFileName matrix.png
taf-hicexplorer hicPlotTADs --tracks tracks.ini --region chr1:1-1000000 --outFileName tad_tracks.png
taf-hicexplorer hicFindTADs --matrix corrected.h5 --outPrefix sample_tads
taf-hicexplorer hicDetectLoops --matrix corrected.h5 --outFileName loops.bedgraph
taf-hicexplorer hicPCA --matrix corrected.h5 --outputFileName pca1.bedgraph pca2.bedgraph
```

Capture Hi-C commands:

```sh
taf-hicexplorer chicQualityControl --help
taf-hicexplorer chicViewpointBackgroundModel --help
taf-hicexplorer chicViewpoint --help
taf-hicexplorer chicSignificantInteractions --help
taf-hicexplorer chicDifferentialTest --help
taf-hicexplorer chicPlotViewpoint --help
```

## Command List

The image includes the HiCExplorer public commands from upstream 3.7.6:

```text
hicexplorer
hicFindRestSite
hicAggregateContacts
hicBuildMatrix
hicBuildMatrixMicroC
hicCorrectMatrix
hicCorrelate
hicFindTADs
hicMergeMatrixBins
hicPlotMatrix
hicPlotDistVsCounts
hicPlotTADs
hicSumMatrices
hicInfo
hicQC
hicCompareMatrices
hicPCA
hicTransform
hicPlotViewpoint
chicViewpointBackgroundModel
chicPlotViewpoint
chicViewpoint
chicAggregateStatistic
chicDifferentialTest
chicQualityControl
chicSignificantInteractions
hicConvertFormat
hicAdjustMatrix
hicNormalize
hicAverageRegions
hicPlotAverageRegions
hicDetectLoops
hicValidateLocations
hicMergeLoops
hicCompartmentalization
hicQuickQC
hicPlotSVL
hicCreateThresholdFile
hicHyperoptDetectLoops
hicHyperoptDetectLoopsHiCCUPS
hicMergeDomains
hicDifferentialTAD
chicExportData
hicInterIntraTAD
hicTADClassifier
hicTrainTADClassifier
```

## Notes

- HiCExplorer stores matrices in formats such as `.h5`, `.cool`, `.mcool`,
  and related tabular/bedGraph outputs depending on the command.
- Plotting commands run headlessly with Matplotlib `Agg`, so PNG/PDF/SVG
  output can be generated inside containers without a display server.
- The image includes Samtools and Bedtools because they are pulled in by the
  Bioconda runtime stack and are useful for Hi-C matrix construction and
  pybedtools-backed commands. Read alignment and sorting can still be handled
  by separate TAFFISH apps such as `taf-samtools` in larger workflows.
- Commands that need large BAM files, genome assemblies, restriction-site
  annotations, or capture-Hi-C designs are supported by the environment but are
  not fully exercised by the small smoke tests.
- This app is declared for native `linux/amd64` and `linux/arm64` builds.

## Metadata

```text
name: hicexplorer
command: taf-hicexplorer
version: 3.7.6-r1
kind: tool
image: ghcr.io/taffish/hicexplorer:3.7.6-r1
platforms: linux/amd64, linux/arm64
```

## Build And Smoke

Maintainer checks:

```sh
taf check
taf build
./target/taf-hicexplorer-v3.7.6-r1 --help
./target/taf-hicexplorer-v3.7.6-r1 -- --version
TAFFISH_CONTAINER_BACKEND=docker ./target/taf-hicexplorer-v3.7.6-r1 hicInfo --version
taf publish --release --dry-run
docker build -t ghcr.io/taffish/hicexplorer:3.7.6-r1 -f docker/Dockerfile .
docker run --rm ghcr.io/taffish/hicexplorer:3.7.6-r1 hicexplorer --version
docker run --rm ghcr.io/taffish/hicexplorer:3.7.6-r1 hicPlotMatrix --version
```

The repository wrapper files are licensed under Apache-2.0. HiCExplorer is
distributed upstream under GPL-3.0-or-later; see the upstream repository and
Bioconda recipe for dependency license details.

## References

- Upstream: <https://github.com/deeptools/HiCExplorer>
- Documentation: <https://hicexplorer.readthedocs.io/>
- Bioconda recipe: <https://bioconda.github.io/recipes/hicexplorer/README.html>
- Galaxy HiCExplorer 3: <https://doi.org/10.1093/nar/gkaa220>
- HiCExplorer web server: <https://doi.org/10.1093/nar/gky504>
- High-resolution TADs paper: <https://doi.org/10.1038/s41467-017-02525-w>
