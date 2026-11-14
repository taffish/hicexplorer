#!/usr/bin/env python3
"""Offline packaging checks using synthetic matrices, never scientific acceptance."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

VERSION = "4.0.0"
TOOLS = """hicexplorer hicFindRestSite hicAggregateContacts hicBuildMatrix
hicBuildMatrixMicroC hicCorrectMatrix hicCorrelate hicFindTADs hicMergeMatrixBins
hicPlotMatrix hicPlotDistVsCounts hicSumMatrices hicInfo hicQC hicCompareMatrices
hicPCA hicTransform hicPlotViewpoint chicViewpointBackgroundModel chicPlotViewpoint
chicViewpoint chicAggregateStatistic chicDifferentialTest chicQualityControl
chicSignificantInteractions hicConvertFormat hicAdjustMatrix hicNormalize
hicAverageRegions hicPlotAverageRegions hicDetectLoops hicValidateLocations
hicMergeLoops hicCompartmentalization hicQuickQC hicPlotSVL hicCreateThresholdFile
hicHyperoptDetectLoops hicHyperoptDetectLoopsHiCCUPS hicMergeDomains hicDifferentialTAD
chicExportData hicInterIntraTAD chicChicagoBackgroundModel chicChicagoScores
chicChicagoSignificantInteractions chicChicagoPlotViewpoint hicDifferentialAnalysis
hicDetectStripes hicArrowhead hicMatrixQC hicMergeTADbins hicPrepareQCreport""".split()


def run(*argv, ok=True):
    result = subprocess.run(list(map(str, argv)), text=True, capture_output=True, timeout=150)
    print("$", " ".join(map(str, argv)), "=>", result.returncode, flush=True)
    if (ok and result.returncode != 0) or (not ok and result.returncode not in (1, 2)):
        raise AssertionError(result.stdout + "\n" + result.stderr)
    return result


def fixture(name="tiny.cool", scale=1):
    import cooler
    import numpy as np
    import pandas as pd
    bins = pd.DataFrame({
        "chrom": ["chrToyA"] * 24 + ["chrToyB"] * 24,
        "start": list(range(0, 24000, 1000)) * 2,
        "end": list(range(1000, 25000, 1000)) * 2,
    })
    pixels = []
    for i in range(48):
        for j in range(i, 48):
            same = i // 24 == j // 24
            value = (40 // (j - i + 1) + 2) if same else 1
            if same and i // 8 == j // 8:
                value += 10
            pixels.append((i, j, value * scale))
    frame = pd.DataFrame(pixels, columns=["bin1_id", "bin2_id", "count"])
    cooler.create_cooler(name, bins, frame, ordered=True, dtypes={"count": np.int32})
    return sum(x[2] for x in pixels)


def identity():
    run(sys.executable, "-m", "pip", "check")
    assert importlib.metadata.version("HiCExplorer") == VERSION
    from hicexplorer import _hicx
    import cooler, hicmatrix, pysam, pybedtools, pyBigWig, matplotlib, graphviz
    assert callable(_hicx.utilities.genomicRegion)
    for tool in TOOLS:
        assert shutil.which(tool), tool
        # Upstream intentionally defines only -h for this command.
        result = run(tool, "-h" if tool == "hicCompartmentalization" else "--help")
        assert tool in result.stdout + result.stderr, tool
    for tool in ("hicInfo", "hicBuildMatrix", "hicPlotMatrix", "hicMatrixQC"):
        result = run(tool, "--version")
        assert re.search(r"(?<![\d.])4\.0\.0(?![\d.])", result.stdout + result.stderr), tool
    for removed in ("hicPlotTADs", "hicTADClassifier", "hicTrainTADClassifier"):
        assert shutil.which(removed) is None, removed
    assert "samtools 1.23.1" in run("samtools", "--version").stdout
    assert "v2.31.1" in run("bedtools", "--version").stdout
    assert "graphviz" in run("dot", "-V").stderr.lower()
    assert os.environ.get("TAFFISH_ENV") == "TAFFISH"
    assert os.environ.get("TAFFISH_NAME") == "hicexplorer"


def matrix():
    import cooler
    import numpy as np
    fixture()
    original = cooler.Cooler("tiny.cool").matrix(balance=False)[:]
    run("hicInfo", "-m", "tiny.cool")
    run("hicConvertFormat", "--matrices", "tiny.cool", "--inputFormat", "cool",
        "--outputFormat", "h5", "--outFileName", "tiny.h5")
    run("hicConvertFormat", "--matrices", "tiny.h5", "--inputFormat", "h5",
        "--outputFormat", "cool", "--outFileName", "roundtrip.cool")
    np.testing.assert_array_equal(original, cooler.Cooler("roundtrip.cool").matrix(balance=False)[:])
    run("hicSumMatrices", "--matrices", "tiny.cool", "tiny.cool", "--outFileName", "sum.cool")
    np.testing.assert_array_equal(original * 2, cooler.Cooler("sum.cool").matrix(balance=False)[:])
    run("hicMergeMatrixBins", "--matrix", "tiny.cool", "--numBins", "2", "--outFileName", "merged.cool")
    assert cooler.Cooler("merged.cool").info["nbins"] == 24
    run("hicTransform", "--matrix", "tiny.cool", "--method", "obs_exp", "--outFileName", "expected.cool")
    assert np.isfinite(cooler.Cooler("expected.cool").matrix(balance=False)[:]).all()
    run("hicCorrectMatrix", "correct", "--matrix", "tiny.cool", "--correctionMethod", "KR",
        "--outFileName", "balanced.cool")
    assert Path("balanced.cool").stat().st_size > 0
    run("hicPCA", "--matrix", "tiny.cool", "--outputFileName", "pc1.bedgraph",
        "--whichEigenvectors", "1", "--format", "bedgraph")
    assert Path("pc1.bedgraph").stat().st_size > 0


def build():
    import cooler
    Path("genome.fa").write_text(">chrToyA\nAAAAGATCAAAAGATCTTTT\n")
    run("hicFindRestSite", "--fasta", "genome.fa", "--searchPattern", "GATC", "--outFile", "sites.bed")
    assert Path("sites.bed").read_text().count("chrToyA") == 2
    lines = [
        "## pairs format v1.0", "#chromsize: chrToyA 24000", "#chromsize: chrToyB 24000",
        "#columns: readID chrom1 pos1 chrom2 pos2 strand1 strand2 pair_type mapq1 mapq2",
    ]
    for i in range(100):
        left = 100 + (i * 173) % 20000
        right = 200 + (i * 359) % 20000
        lines.append(f"read{i}\tchrToyA\t{left}\tchrToyB\t{right}\t+\t-\tUU\t60\t60")
    Path("reads.pairs").write_text("\n".join(lines) + "\n")
    run("hicBuildMatrix", "--pairsFile", "reads.pairs", "--binSize", "1000",
        "--outFileName", "built.cool", "--QCfolder", "builder QC", "--threads", "2")
    assert int(cooler.Cooler("built.cool").pixels()[:]["count"].sum()) == 100
    assert Path("builder QC/QC.log").stat().st_size > 0
    assert Path("builder QC/hicQC.html").stat().st_size > 0
    run("hicMatrixQC", "-m", "built.cool", "-o", "built statistics.html", "--threads", "2")
    assert "100" in Path("built statistics.tsv").read_text()


def plots():
    fixture()
    for suffix in ("png", "svg", "pdf"):
        target = f"matrix with spaces.{suffix}"
        run("hicPlotMatrix", "--matrix", "tiny.cool", "--outFileName", target,
            "--title", "Synthetic matrix", "--region", "chrToyA:0-24000")
        blob = Path(target).read_bytes()
        assert len(blob) > 500
        if suffix == "png":
            assert blob.startswith(b"\x89PNG\r\n\x1a\n")
        elif suffix == "pdf":
            assert blob.startswith(b"%PDF-")
        else:
            assert b"<svg" in blob
    run("hicCorrelate", "--matrices", "tiny.cool", "tiny.cool", "--method", "pearson",
        "--outFileNameHeatmap", "correlation.png", "--outFileNameScatter", "scatter.png")
    assert Path("correlation.png").stat().st_size > 500
    Path("tracks.ini").write_text("[matrix]\nfile = tiny.cool\ntitle = Synthetic contacts\nfile_type = hic_matrix\n")
    run("pyGenomeTracks", "--tracks", "tracks.ini", "--region", "chrToyA:0-24000",
        "--outFileName", "tracks.png")
    assert Path("tracks.png").stat().st_size > 500


def bam():
    import cooler
    import pysam
    header = {"HD": {"VN": "1.6", "SO": "queryname"},
              "SQ": [{"SN": "chrToyA", "LN": 24000}, {"SN": "chrToyB", "LN": 24000}]}
    with pysam.AlignmentFile("r1.bam", "wb", header=header) as left, \
            pysam.AlignmentFile("r2.bam", "wb", header=header) as right:
        for i in range(100):
            positions = [100 + (i * 173) % 20000, 200 + (i * 359) % 20000]
            for mate, dest in enumerate((left, right)):
                read = pysam.AlignedSegment(dest.header)
                read.query_name = f"read{i:04d}"
                read.query_sequence = "N" * 50
                read.flag = 65 if mate == 0 else 145
                read.reference_id = mate
                read.reference_start = positions[mate]
                read.mapping_quality = 60
                read.cigarstring = "50M"
                read.next_reference_id = 1 - mate
                read.next_reference_start = positions[1 - mate]
                read.query_qualities = pysam.qualitystring_to_array("I" * 50)
                dest.write(read)
    Path("restriction.bed").write_text("".join(
        f"{chrom}\t{p}\t{p + 4}\n" for chrom in ("chrToyA", "chrToyB") for p in range(0, 24000, 1000)))
    run("hicBuildMatrix", "--samFiles", "r1.bam", "r2.bam", "--binSize", "1000",
        "--restrictionCutFile", "restriction.bed", "--restrictionSequence", "GATC",
        "--danglingSequence", "GATC", "--outFileName", "bam.cool", "--QCfolder", "bam qc",
        "--outBam", "accepted.bam", "--threads", "2")
    run("samtools", "quickcheck", "accepted.bam")
    assert cooler.Cooler("bam.cool").pixels()[:]["count"].sum() > 0
    run("hicBuildMatrixMicroC", "--samFiles", "r1.bam", "r2.bam", "--binSize", "1000",
        "--outFileName", "microc.cool", "--QCfolder", "microc qc", "--threads", "2")
    assert cooler.Cooler("microc.cool").pixels()[:]["count"].sum() > 0


def report():
    total = fixture()
    label = "Toy <tag> & \"quotes\""
    for threads in ("1", "2"):
        run("hicMatrixQC", "-m", "tiny.cool", "-o", f"matrix qc {threads}.html",
            "--labels", label, "--threads", threads)
        text = Path(f"matrix qc {threads}.html").read_text()
        assert "<script" not in text.lower()
        assert "<tag>" not in text
        assert "&lt;tag&gt;" in text
        values = dict(line.split("\t", 1) for line in Path(f"matrix qc {threads}.tsv").read_text().splitlines())
        assert int(values["contacts.total"]) == total
    assert Path("matrix qc 1.tsv").read_bytes() == Path("matrix qc 2.tsv").read_bytes()


def new_tools():
    fixture()
    run("hicArrowhead", "-m", "tiny.cool", "-o", "domains.bedpe")
    assert "uVarScore" in Path("domains.bedpe").read_text()
    run("hicDetectStripes", "-m", "tiny.cool", "--norm", "None", "-t", "2", "-o", "stripes.tsv")
    assert Path("stripes.tsv").is_file()
    fixture("replicate.cool", scale=2)
    Path("domains.bed").write_text("".join(
        f"{chrom}\t{start}\t{start+8000}\n" for chrom in ("chrToyA", "chrToyB")
        for start in (0, 8000, 16000)))
    run("hicDifferentialAnalysis", "tads", "--conditionA", "tiny.cool", "replicate.cool",
        "--conditionB", "tiny.cool", "replicate.cool", "--domains", "domains.bed",
        "--outFilePrefix", "differential", "--threads", "2")
    assert Path("differential_tads.tsv").stat().st_size > 0
    assert Path("differential_boundaries.tsv").stat().st_size > 0
    for tool in ("chicChicagoBackgroundModel", "chicChicagoScores", "chicChicagoSignificantInteractions",
                 "chicChicagoPlotViewpoint", "hicDifferentialAnalysis"):
        result = run(tool, "--help-json")
        spec = json.loads(result.stdout)
        assert spec["tool"] == tool


def negative():
    fixture()
    before = hashlib.sha256(Path("tiny.cool").read_bytes()).hexdigest()
    run("hicInfo", "-m", "missing.cool", ok=False)
    run("hicMatrixQC", "-m", "missing.cool", "-o", "missing.html", ok=False)
    assert not Path("missing.html").exists()
    run("hicMatrixQC", "-m", "tiny.cool", "-o", "bad labels.html", "--labels", "a", "b", ok=False)
    assert not Path("bad labels.html").exists()
    run("hicArrowhead", "-m", "missing.cool", "-o", "missing.bedpe", ok=False)
    assert not Path("missing.bedpe").exists()
    run("hicBuildMatrix", "--pairsFile", "missing.pairs", "-o", "missing-built.cool",
        "--QCfolder", "missing-qc", "--binSize", "1000", ok=False)
    assert not Path("missing-built.cool").exists()
    assert hashlib.sha256(Path("tiny.cool").read_bytes()).hexdigest() == before


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("case", choices=("identity", "matrix", "build", "bam", "plots", "report", "new_tools", "negative"))
    parser.add_argument("--keep", type=Path, help="Create a new persistent evidence directory.")
    args = parser.parse_args()
    if args.keep:
        args.keep.mkdir(parents=True, exist_ok=False)
        work = args.keep.resolve()
        temporary = None
    else:
        temporary = tempfile.TemporaryDirectory(prefix="taf-hicexplorer-")
        work = Path(temporary.name)
    os.chdir(work)
    os.environ["MPLCONFIGDIR"] = str(work / "mpl-cache")
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["OMP_NUM_THREADS"] = "2"
    try:
        globals()[args.case]()
        print("PASS", args.case)
    finally:
        if temporary:
            temporary.cleanup()
