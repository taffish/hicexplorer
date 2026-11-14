# HiCExplorer

TAFFISH package: **4.0.0-r1**
Upstream: [HiCExplorer 4.0.0](https://github.com/deeptools/HiCExplorer/releases/tag/4.0.0)

Build, inspect, correct, compare, convert and plot Hi-C, Micro-C and capture Hi-C
contact matrices. This package includes the official C++ tools, Python API,
headless plotting, native offline QC reports and pyGenomeTracks. It supports
Linux amd64 and arm64; Docker, Podman and Linux Apptainer are the runtime backends.

## Start here

After this version is published and indexed, install it through TAFFISH:

```bash
taf update
taf install hicexplorer
```

Run in a writable project directory. Tool-specific arguments follow the command
name; `--help` alone shows the TAFFISH wrapper help.

```bash
taf-hicexplorer --help
taf-hicexplorer hicBuildMatrix --help
taf-hicexplorer hicInfo --matrices sample.cool
taf-hicexplorer hicPlotMatrix --matrix sample.cool --outFileName contacts.png
taf-hicexplorer hicMatrixQC --matrices sample.cool --outFileName matrix-qc.html
```

Use [terminal help](docs/help.md) for routine commands and backend-specific
read-only mounts. With TAFFISH 0.11, preserve inner quotes for trusted filenames
containing spaces, for example:

```bash
taf-hicexplorer hicPlotMatrix --matrix '"sample with spaces.cool"' --outFileName '"contact map.png"'
```

This syntax is for individual tool arguments. The extra container-argument
environment variables are split differently: use absolute mount-source paths
without spaces in the examples below. Do not insert untrusted text into shell
commands.

## Typical workflow

Create a matrix from paired BAMs using the matching reference/restriction
information, or use the upstream 4DN pairs-file route:

```bash
taf-hicexplorer hicBuildMatrix --pairsFile reads.pairs.gz --binSize 10000 --outFileName sample.cool --QCfolder build-qc --threads 4
taf-hicexplorer hicInfo --matrices sample.cool
taf-hicexplorer hicCorrectMatrix correct --matrix sample.cool --correctionMethod KR --outFileName balanced.cool
taf-hicexplorer hicConvertFormat --matrices sample.cool --inputFormat cool --outputFormat h5 --outFileName sample.h5
taf-hicexplorer hicMatrixQC --matrices sample.cool --outFileName matrix-qc.html
```

Consult the selected command's help for analysis parameters appropriate to your
data. The package smoke inputs are synthetic software fixtures, not recommended
biological parameters or validation of scientific results. Use a new output/QC
directory for each run and budget memory, scratch space and threads for the matrix
size. Matrix inputs and derived balancing/coordinate metadata must match.

### Plotting and reports

`hicPlotMatrix`, other upstream plotting commands and `pyGenomeTracks` write
static images (select a supported suffix such as PNG, SVG or PDF). Open them on
the host; no display forwarding, server or port is required.

`hicBuildMatrix` produces `QCfolder/hicQC.html`; retain the entire QC folder so
its associated tables and links remain available. `hicMatrixQC` writes a native
static HTML file and a TSV statistics file. These are upstream reports, not a
TAFFISH-authored viewer. They can be opened locally in a browser on all three
backends; do not expect application controls that are not present upstream.

[Galaxy HiCExplorer](https://hicexplorer.usegalaxy.eu/) and
[scHiCExplorer](https://github.com/joachimwolff/scHiCExplorer) are independent
applications, not runtime dependencies of this CLI package. This image does not
start Galaxy, Jupyter or a browser GUI service.

## References, matrices and shared use

HiCExplorer 4.0 has no bundled pretrained model or mandatory downloaded database.
FASTA, restriction BED, contact matrices, annotation tracks, bait maps and CHiCAGO
design files are user-selected inputs. There is no TAFFISH database installer,
automatic download, hidden resource discovery or READY-marker protocol.

An administrator can prepare a reference once (including any derived restriction
BED) under a versioned shared directory, then grant users read access to files
and traversal access to its directories. Record the assembly, original source,
checksums, reference version and preparation arguments. Do not mix genome builds,
restriction definitions or coordinate systems. Use only resources whose terms
permit the intended local/shared use.

Mount the selected directory read-only at `/mnt` using the three backend examples
in [help](docs/help.md). Run calculations in each user's writable project directory;
do not use the shared directory as a working/output/cache location. Changing an
input library is an explicit administrator operation: stage and validate a new
version separately, then point jobs at it. Existing input files are not migrated
or deleted by a TAFFISH resource helper.

## Changes from 3.7.6

Version 4 is an official C++ rewrite, not an accelerated fork maintained here.
Upstream adds matrix QC, Arrowhead domains, stripe detection, differential
analysis and the four `chicChicago*` tools. It also adds direct pairs-file input
and extends .hic conversion, matrix plotting and reproducibility metrics.

Upstream deliberately removed `hicTADClassifier`, `hicTrainTADClassifier` and
`hicPlotTADs`. The first two models/commands are not included. Use
`pyGenomeTracks --tracks tracks.ini --region chr1:START-END --outFileName tracks.png`
instead of the old `hicPlotTADs` forwarding entry.

Upstream corrected several calculations, including observed/expected distance
normalization and integer-matrix handling. Results from affected 3.7.6 workflows
can differ; see the [official release notes](https://github.com/deeptools/HiCExplorer/releases/tag/4.0.0)
before comparing or recomputing analyses. This packaging does not modify the
scientific algorithms and does not claim bitwise equivalence to 3.7.6.

## Build provenance and dependencies

The image builds the unmodified official source at commit
`d8ed7103fd7c51c784f787f1bdb9c17facb66453` using its CMake/scikit-build-core wheel
route. The source archive SHA256 is
`06f25fe092b7bc9beaf89dd31407abd26d9b5371f8c638d43e3210c450764c46`.
The Micromamba base is digest-pinned; architecture-specific Conda URL/SHA256 locks
are in `docker/locks/`. Compiler and build-only headers are excluded from the
final runtime stage.

The runtime retains samtools 1.23.1, bedtools 2.31.1, pysam 0.24.0, hicmatrix 17.2,
cooler 0.10.4, pyGenomeTracks 3.9 and Graphviz 14.1.2. The C++ core links the same
locked HDF5/OpenBLAS environment used by Python. HTSlib 1.23.1 is retained for
compatibility with the existing samtools/pysam tools; this is newer than the
upstream build guide's 1.21 validation range. Source code is unchanged.

Setuptools is fixed at 80.9.0 because the retained Hyperopt 0.2.7 helpers import
`pkg_resources`, which newer Setuptools no longer provides. This dependency
compatibility pin does not patch HiCExplorer or its analysis methods.
The obsolete Python hic2cool dependency is not installed: version 4's native
`hicConvertFormat` provides that conversion in its bundled C++ core. Pytest is
included because pyGenomeTracks declares it as a required dependency.

`hicHyperoptDetectLoopsHiCCUPS` is an optional driver for an external Juicer
installation. Its help/import entry is available, but Juicer's JAR, Java/GPU
runtime and the HiCCUPS workflow are not bundled or claimed as validated here.
Use a separately prepared Juicer environment for that independent integration.

Fixed hashes identify fetched artifacts; they do not guarantee perpetual
availability or a bit-for-bit rebuild. Conda repositories may remove artifacts,
and Debian's live build-tool repositories may change. The Dockerfile documents
these external drift boundaries. Large upstream test fixtures, compilers,
package caches and the source tree are not shipped in the runtime image.

## Packaging validation

The 4.0.0-r1 candidate was built natively on Linux amd64 and arm64. Offline
manifest checks and generated-wrapper workflows passed on xjp amd64 with Docker,
Podman and Apptainer, and on ARM64 with Docker and Podman. Docker/Podman checks
also passed with a read-only root filesystem and a non-root container user.
Validation covers synthetic matrices and BAMs, plotting, native HTML, CHiCAGO
regression fixtures, quoted paths, read-only shared references and failure
recovery; it is not scientific validation of production datasets. The two native
HTML report types were opened directly and checked by the maintainer.

Uncompressed Docker image sizes are approximately 1.52 GB (amd64) and 1.55 GB
(arm64). Multi-stage builds exclude compilers, source archives and build-only
headers; package caches are cleared. Most remaining space is the pinned Python,
numeric and plotting environment. Local candidate validation does not substitute
for the subsequent published Action/GHCR/Index results.

## License and citation

The TAFFISH wrapper is Apache-2.0 (see [LICENSE](LICENSE)). HiCExplorer is
GPL-3.0-or-later. Upstream licenses and third-party notices are retained in the
installed distribution and `/usr/local/share/licenses/hicexplorer/`; included
dependencies retain their own licenses. The wrapper license does not replace
those licenses or grant rights to external reference datasets.

Please cite the relevant upstream methods and:

Wolff et al. (2020), *Galaxy HiCExplorer 3*,
[doi:10.1093/nar/gkaa220](https://doi.org/10.1093/nar/gkaa220).
See the [upstream project](https://github.com/deeptools/HiCExplorer) for the complete
citation list and tool documentation.
