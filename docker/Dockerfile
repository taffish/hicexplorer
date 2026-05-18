FROM mambaorg/micromamba:1.5.10-bookworm-slim AS runtime

ARG HICEXPLORER_VERSION=3.7.6

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN set -eux; \
    for attempt in 1 2 3 4 5 6; do \
      if apt-get -o Acquire::Retries=3 update \
       && apt-get -o Acquire::Retries=3 install -y --no-install-recommends \
            bash \
            ca-certificates \
            coreutils \
            procps; then \
        break; \
      fi; \
      if [ "$attempt" = "6" ]; then exit 1; fi; \
      apt-get clean; \
      rm -rf /var/lib/apt/lists/*; \
      sleep 5; \
    done; \
    rm -rf /var/lib/apt/lists/*

USER mambauser

RUN micromamba install -y -n base \
      -c conda-forge \
      -c bioconda \
      "python=3.10" \
      "hicexplorer=${HICEXPLORER_VERSION}" \
      "hicmatrix=17.2" \
      "hic2cool=1.0.1" \
      "cooler=0.10.4" \
      "pygenometracks=3.9" \
      "pysam=0.24.0" \
      "pybedtools=0.12.0" \
      "scikit-learn=1.3.2" \
      "samtools=1.23.1" \
      "bedtools=2.31.1" \
      "graphviz=14.1.2" \
 && micromamba clean -a -y

ENV PATH=/opt/conda/bin:${PATH}
ENV LD_LIBRARY_PATH=/opt/conda/lib
ENV PYTHONNOUSERSITE=1
ENV MPLBACKEND=Agg

USER root

RUN set -eux; \
    hicexplorer --version 2>&1 | grep -F "${HICEXPLORER_VERSION}" >/dev/null; \
    hicexplorer --help 2>&1 | grep -F "hicBuildMatrix" >/dev/null; \
    hicInfo --version 2>&1 | grep -F "${HICEXPLORER_VERSION}" >/dev/null; \
    hicBuildMatrix --version 2>&1 | grep -F "${HICEXPLORER_VERSION}" >/dev/null; \
    hicBuildMatrixMicroC --version 2>&1 | grep -F "${HICEXPLORER_VERSION}" >/dev/null; \
    hicConvertFormat --version 2>&1 | grep -F "${HICEXPLORER_VERSION}" >/dev/null; \
    hicPlotMatrix --version 2>&1 | grep -F "${HICEXPLORER_VERSION}" >/dev/null; \
    chicViewpoint --version 2>&1 | grep -F "${HICEXPLORER_VERSION}" >/dev/null; \
    samtools --version | grep -F "samtools 1.23.1" >/dev/null; \
    bedtools --version | grep -F "v2.31.1" >/dev/null; \
    dot -V 2>&1 | grep -F "graphviz" >/dev/null; \
    python -c "import hicexplorer, hicmatrix, cooler, pybedtools, pyBigWig, pysam, sklearn, matplotlib, graphviz"

FROM runtime AS checked

RUN set -eux; \
    mkdir -p /tmp/taf-hicexplorer-check; \
    cd /tmp/taf-hicexplorer-check; \
    printf ">chr1\nAAAAGATCAAAAGATCTTTT\n" > genome.fa; \
    hicFindRestSite --fasta genome.fa --searchPattern GATC --outFile sites.bed; \
    test -s sites.bed; \
    grep -F "chr1" sites.bed >/dev/null; \
    python -c 'import cooler, pandas as pd; bins = pd.DataFrame({"chrom": ["chr1", "chr1"], "start": [0, 1000], "end": [1000, 2000]}); pixels = pd.DataFrame({"bin1_id": [0, 0, 1], "bin2_id": [0, 1, 1], "count": [5, 2, 3]}); cooler.create_cooler("tiny.cool", bins=bins, pixels=pixels, ordered=True)'; \
    hicInfo --matrices tiny.cool | grep -F "tiny.cool" >/dev/null; \
    hicPlotMatrix --matrix tiny.cool --outFileName tiny.png >/dev/null; \
    test -s tiny.png; \
    hicConvertFormat --matrices tiny.cool --inputFormat cool --outputFormat h5 --outFileName tiny.h5 >/dev/null; \
    test -s tiny.h5; \
    hicInfo --matrices tiny.h5 | grep -F "tiny.h5" >/dev/null; \
    cd /; \
    rm -rf /tmp/taf-hicexplorer-check

WORKDIR /root

ENTRYPOINT []
CMD ["/bin/bash"]

ENV TAFFISH_ENV=TAFFISH
ENV TAFFISH_NAME=hicexplorer
