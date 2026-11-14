# syntax=docker/dockerfile:1
# Source identity and Conda artifact hashes are fixed. The official archive and
# Conda channels are still external services: artifacts can disappear. Debian
# package metadata/security updates can also drift. This is not an offline or
# bit-for-bit rebuild guarantee; revalidate successors instead of changing tags.
ARG MAMBA_BASE=mambaorg/micromamba:latest@sha256:e1476182cd40eb1f7c0cfae4adec9bfd78f3d7f05c61368306abfdc8939c1198
FROM scratch AS upstream
ADD --checksum=sha256:06f25fe092b7bc9beaf89dd31407abd26d9b5371f8c638d43e3210c450764c46 https://codeload.github.com/deeptools/HiCExplorer/tar.gz/d8ed7103fd7c51c784f787f1bdb9c17facb66453 /source.tar.gz

FROM ${MAMBA_BASE} AS environment
USER root
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG TARGETARCH
COPY docker/locks/linux-64.lock docker/locks/linux-aarch64.lock /usr/local/share/taffish/hicexplorer/locks/
RUN set -eu; \
    case "$TARGETARCH" in amd64) platform=linux-64 ;; arm64) platform=linux-aarch64 ;; *) exit 64 ;; esac; \
    micromamba create --yes --no-rc --prefix /opt/hic \
      --file "/usr/local/share/taffish/hicexplorer/locks/${platform}.lock"; \
    micromamba clean --all --yes
ENV PATH="/opt/hic/bin:${PATH}" \
    PYTHONNOUSERSITE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MPLBACKEND=Agg

FROM environment AS build
COPY docker/locks/build-linux-64.lock docker/locks/build-linux-aarch64.lock /usr/local/share/taffish/hicexplorer/locks/
# Debian packages are resolved at rebuild time; the base is digest-pinned, but
# its live apt repository is not a snapshot. Keep compilation tools out of runtime.
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential cmake ninja-build ca-certificates \
    && rm -rf /var/lib/apt/lists/*
ARG TARGETARCH
RUN set -eu; \
    case "$TARGETARCH" in amd64) platform=linux-64 ;; arm64) platform=linux-aarch64 ;; *) exit 64 ;; esac; \
    micromamba install --yes --no-rc --prefix /opt/hic \
      --file "/usr/local/share/taffish/hicexplorer/locks/build-${platform}.lock"; \
    micromamba clean --all --yes
ARG BUILD_JOBS=2
# The source remains unmodified. Large upstream fixtures stay in the build
# stage; the wheel excludes tests. Native builds use upstream's own SIMD rules.
RUN --mount=from=upstream,source=/source.tar.gz,target=/tmp/source.tar.gz,ro \
    set -eu; \
    printf '%s  %s\n' 06f25fe092b7bc9beaf89dd31407abd26d9b5371f8c638d43e3210c450764c46 /tmp/source.tar.gz | sha256sum --check -; \
    mkdir /src /wheels; \
    tar -xzf /tmp/source.tar.gz --strip-components=1 -C /src; \
    cd /src; \
    CMAKE_ARGS="-DCMAKE_PREFIX_PATH=/opt/hic -DPython_EXECUTABLE=/opt/hic/bin/python" \
    CMAKE_BUILD_PARALLEL_LEVEL="$BUILD_JOBS" \
      python -m pip wheel --no-deps --no-build-isolation --wheel-dir /wheels .; \
    mkdir -p /licenses; \
    cp LICENSE cpp/THIRD_PARTY_NOTICES.md /licenses/; \
    cp cpp/third_party/spectra/LICENSE /licenses/Spectra-LICENSE

FROM environment AS runtime
RUN --mount=from=build,source=/wheels,target=/wheels,ro \
    python -m pip install --no-deps --no-cache-dir /wheels/*.whl
COPY --from=build /licenses/ /usr/local/share/licenses/hicexplorer/
COPY tests/check.py /usr/local/share/taffish/hicexplorer/check.py
# Only lightweight identity/import checks belong in a native build. Plotting,
# numerical fixtures and read-only/non-root checks run after the image is built.
RUN python -c 'import importlib.metadata as m; assert m.version("HiCExplorer") == "4.0.0"; from hicexplorer import _hicx' \
    && hicInfo --version
ENV TAFFISH_ENV=TAFFISH \
    TAFFISH_NAME=hicexplorer
WORKDIR /tmp
ENTRYPOINT []
CMD ["/bin/bash"]
