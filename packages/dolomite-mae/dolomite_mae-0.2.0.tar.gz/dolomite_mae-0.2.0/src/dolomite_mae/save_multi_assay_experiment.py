import json
import os

import biocutils
import dolomite_base as dl
import h5py
from multiassayexperiment import MultiAssayExperiment


@dl.save_object.register
@dl.validate_saves
def save_multi_assay_experiment(
    x: MultiAssayExperiment,
    path: str,
    data_frame_args: dict = None,
    assay_args: dict = None,
    **kwargs,
):
    """Method for saving
    :py:class:`~multiassayexperiment.MultiAssayExperiment.MultiAssayExperiment`
    objects to their corresponding file representations, see
    :py:meth:`~dolomite_base.save_object.save_object` for details.

    Args:
        x:
            Object to be staged.

        path:
            Path to a directory in which to save ``x``.

        data_frame_args:
            Further arguments to pass to the ``save_object`` method for the
            row/column data.

        assay_args:
            Further arguments to pass to the ``save_object`` method for the
            assays.

        kwargs: 
            Further arguments.

    Returns:
        ``x`` is saved to path.
    """
    os.mkdir(path)

    if data_frame_args is None:
        data_frame_args = {}

    if assay_args is None:
        assay_args = {}

    _info = {"multi_sample_dataset": {"version": "1.0"}}
    dl.save_object_file(path, "multi_sample_dataset", _info)

    # sample/column data
    _sample_path = os.path.join(path, "sample_data")
    dl.alt_save_object(x.get_column_data(), _sample_path, **data_frame_args, **kwargs)

    # save alt expts.
    _expt_names = x.get_experiment_names()
    if len(_expt_names) > 0:
        _expt_path = os.path.join(path, "experiments")
        os.mkdir(_expt_path)

        with open(os.path.join(_expt_path, "names.json"), "w") as handle:
            json.dump(_expt_names, handle)

        for _aidx, _aname in enumerate(_expt_names):
            _expt_save_path = os.path.join(_expt_path, str(_aidx))
            try:
                dl.alt_save_object(
                    x.experiment(_aname),
                    path=_expt_save_path,
                    data_frame_args=data_frame_args,
                    assay_args=assay_args,
                    **kwargs,
                )
            except Exception as ex:
                raise RuntimeError(
                    "failed to stage experiment '"
                    + _aname
                    + "' for "
                    + str(type(x))
                    + "; "
                    + str(ex)
                )
        with h5py.File(os.path.join(path, "sample_map.h5"), "w") as handle:
            ghandle = handle.create_group("multi_sample_dataset")

            _sample_map = x.get_sample_map()
            for _aidx, _aname in enumerate(_expt_names):
                _indices_to_keep = [
                    idx
                    for idx, x in enumerate(_sample_map.get_column("assay"))
                    if x == _aname
                ]

                _colnames = biocutils.subset_sequence(
                    _sample_map.get_column("colname"), _indices_to_keep
                )
                _sample = biocutils.subset_sequence(
                    _sample_map.get_column("primary"), _indices_to_keep
                )

                i = biocutils.match(_sample, x.get_column_data().get_row_names())

                if (i == -1).any():
                    raise RuntimeError(
                        "Samples in 'sample_map' not presented in 'column_data' for ",
                        f"{_aname}.",
                    )

                j = biocutils.match(x.experiment(_aname).get_column_names(), _colnames)
                if (j == -1).any():
                    raise RuntimeError(
                        f"Column names in experiment '{_aname}' not presented in 'sample_map'."
                    )

                reorder = i[j.tolist()]

                dl.write_integer_vector_to_hdf5(
                    ghandle, name=str(_aidx), h5type="u4", x=reorder
                )

    _meta = x.get_metadata()
    if _meta is not None and len(_meta) > 0:
        dl.alt_save_object(_meta, path=os.path.join(path, "other_data"), **kwargs)

    return
