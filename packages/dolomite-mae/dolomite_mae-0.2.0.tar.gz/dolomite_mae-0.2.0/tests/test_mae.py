import os
from random import random
from tempfile import mkdtemp

import biocframe
import dolomite_mae
import dolomite_sce
import dolomite_se
import numpy
import pandas as pd
from dolomite_base import read_object, save_object
from genomicranges import GenomicRanges
from multiassayexperiment import MultiAssayExperiment
from singlecellexperiment import SingleCellExperiment
from summarizedexperiment import SummarizedExperiment


def test_stage_mae_basic():
    x = numpy.random.rand(1000, 200)
    x2 = (numpy.random.rand(1000, 200) * 10).astype(numpy.int32)

    sce = SingleCellExperiment(
        {"logcounts": x, "counts": x2},
        main_experiment_name="aaron's secret modality",
        row_data=biocframe.BiocFrame(
            {"foo": numpy.random.rand(1000), "bar": numpy.random.rand(1000)},
            row_names=["gene_sce_" + str(i) for i in range(1000)],
        ),
        column_data=biocframe.BiocFrame(
            {"whee": numpy.random.rand(200), "stuff": numpy.random.rand(200)},
            row_names=["cell_sce" + str(i) for i in range(200)],
        ),
    )

    se = SummarizedExperiment(
        {"counts": numpy.random.rand(100, 200)},
        row_data=biocframe.BiocFrame(
            {"foo": numpy.random.rand(100), "bar": numpy.random.rand(100)},
            row_names=["gene_se_" + str(i) for i in range(100)],
        ),
        column_data=biocframe.BiocFrame(
            {"whee": numpy.random.rand(200), "stuff": numpy.random.rand(200)},
            row_names=["cell_se" + str(i) for i in range(200)],
        ),
    )

    mae = MultiAssayExperiment(experiments={"jay_expt": sce, "aarons_expt": se})

    dir = os.path.join(mkdtemp(), "mae_simple")
    save_object(mae, dir)

    roundtrip = read_object(dir)
    assert isinstance(roundtrip, MultiAssayExperiment)
    assert roundtrip.experiment("jay_expt").shape == sce.shape
    assert (
        roundtrip.experiment("aarons_expt").shape == mae.experiment("aarons_expt").shape
    )
    assert len(mae.get_column_data()) == 2
    assert len(mae.get_sample_map()) == 400
    assert list(mae.get_column_data().get_row_names()) == [
        "unknown_sample_jay_expt",
        "unknown_sample_aarons_expt",
    ]


def test_stage_mae_complex():
    nrows = 200
    ncols = 6
    counts = numpy.random.rand(nrows, ncols)
    df_gr = pd.DataFrame(
        {
            "seqnames": [
                "chr1",
                "chr2",
                "chr2",
                "chr2",
                "chr1",
                "chr1",
                "chr3",
                "chr3",
                "chr3",
                "chr3",
            ]
            * 20,
            "starts": range(100, 300),
            "ends": range(110, 310),
            "strand": ["-", "+", "+", "*", "*", "+", "+", "+", "-", "-"] * 20,
            "score": range(0, 200),
            "GC": [random() for _ in range(10)] * 20,
        }
    )

    gr = GenomicRanges.from_pandas(df_gr)

    column_data_sce = pd.DataFrame(
        {
            "treatment": ["ChIP", "Input"] * 3,
        },
        index=["sce"] * 6,
    )
    column_data_se = pd.DataFrame(
        {
            "treatment": ["ChIP", "Input"] * 3,
        },
        index=["se"] * 6,
    )

    sample_map = pd.DataFrame(
        {
            "assay": ["sce", "se"] * 6,
            "primary": ["sample1", "sample2"] * 6,
            "colname": ["sce", "se"] * 6,
        }
    )

    sample_data = pd.DataFrame(
        {"samples": ["sample1", "sample2"]}, index=["sample1", "sample2"]
    )

    tsce = SingleCellExperiment(
        assays={"counts": counts},
        row_data=df_gr,
        column_data=column_data_sce,
        row_ranges=gr,
    )

    tse2 = SummarizedExperiment(
        assays={"counts": counts.copy()},
        row_data=df_gr.copy(),
        column_data=column_data_se.copy(),
    )

    mae = MultiAssayExperiment(
        experiments={"sce": tsce, "se": tse2},
        column_data=sample_data,
        sample_map=sample_map,
        metadata={"could be": "anything"},
    )

    dir = os.path.join(mkdtemp(), "mae_simple")
    save_object(mae, dir)

    roundtrip = read_object(dir)
    assert isinstance(roundtrip, MultiAssayExperiment)
    assert roundtrip.experiment("sce").shape == mae.experiment("sce").shape
    assert roundtrip.experiment("se").shape == mae.experiment("se").shape
    assert len(mae.get_column_data()) == len(sample_data)
    assert len(mae.get_sample_map()) == len(sample_map)
    assert list(mae.get_column_data().get_row_names()) == [
        "sample1",
        "sample2",
    ]
