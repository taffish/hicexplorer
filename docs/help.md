taf-hicexplorer 4.0.0-r1 — contact matrices, plots and offline QC

Usage:
  Start in a writable project directory.
  taf-hicexplorer --help                      Show this wrapper help
  taf-hicexplorer --version                   Show the package version
  taf-hicexplorer hicInfo --version            Show the upstream version
  taf-hicexplorer hicBuildMatrix --help         Show a tool's options
  taf-hicexplorer hicCompartmentalization -h   This tool uses short -h only
  taf-hicexplorer hicexplorer                  List available upstream tools

Inspect, plot and convert:
  taf-hicexplorer hicInfo --matrices sample.cool
  taf-hicexplorer hicPlotMatrix --matrix sample.cool --outFileName contacts.png
  taf-hicexplorer hicConvertFormat --matrices sample.cool --inputFormat cool --outputFormat h5 --outFileName sample.h5

Build from a 4DN pairs file; use a fresh output/QC directory per run:
  taf-hicexplorer hicBuildMatrix --pairsFile reads.pairs.gz --binSize 10000 --outFileName sample.cool --QCfolder build-qc --threads 4
For paired BAM input, see hicBuildMatrix --help and supply matching restriction
information. Allow sufficient memory and writable scratch space for your data.

View results:
  taf-hicexplorer hicMatrixQC --matrices sample.cool --outFileName matrix-qc.html
  taf-hicexplorer pyGenomeTracks --tracks tracks.ini --region chr1:0-100000 --outFileName tracks.png
Open the images or matrix-qc.html on your host. Keep the complete build-qc folder
when opening build-qc/hicQC.html, so linked tables stay available. These are
upstream static offline reports; no GUI service, network port or display is needed
on Docker, Podman or Apptainer. Numeric matrix-QC results are also in matrix-qc.tsv.

Reuse an administrator-prepared reference read-only:
  Use an absolute host directory without spaces; keep outputs in your own project.
  HIC_REF=/srv/references/hicexplorer/assembly-v1
  TAFFISH_CONTAINER_BACKEND=docker TAFFISH_DOCKER_RUN_ARGS="-v ${HIC_REF}:/mnt:ro" taf-hicexplorer hicFindRestSite --fasta /mnt/genome.fa --searchPattern GATC --outFile sites.bed
  TAFFISH_CONTAINER_BACKEND=podman TAFFISH_PODMAN_RUN_ARGS="-v ${HIC_REF}:/mnt:ro" taf-hicexplorer hicFindRestSite --fasta /mnt/genome.fa --searchPattern GATC --outFile sites.bed
  TAFFISH_CONTAINER_BACKEND=apptainer TAFFISH_APPTAINER_RUN_ARGS="--bind ${HIC_REF}:/mnt:ro" taf-hicexplorer hicFindRestSite --fasta /mnt/genome.fa --searchPattern GATC --outFile sites.bed
The reference must match your assembly/coordinates. Files need read permission;
parent directories need traversal permission. No reference or model is downloaded.

If a file is not found, check its path inside the container and the mount.
For a trusted filename with spaces in TAFFISH 0.11, preserve inner quotes:
  taf-hicexplorer hicInfo --matrices '"sample with spaces.cool"'
Do not use a shared read-only reference directory as the working/output directory.

hicTADClassifier and hicTrainTADClassifier were removed upstream in version 4.
Use pyGenomeTracks instead of the removed hicPlotTADs entry. Details about version
changes, resources, independent Galaxy services and provenance are in the README.
