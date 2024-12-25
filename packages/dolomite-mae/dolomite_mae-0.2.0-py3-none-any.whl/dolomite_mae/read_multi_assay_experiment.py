import json
import os

import dolomite_base as dl
import h5py
from biocframe import BiocFrame
from dolomite_base.read_object import read_object_registry
from multiassayexperiment import MultiAssayExperiment

read_object_registry["multi_sample_dataset"] = (
    "dolomite_mae.read_multi_assay_experiment"
)


def read_multi_assay_experiment(
    path: str, metadata: dict, **kwargs
) -> MultiAssayExperiment:
    """Load a
    :py:class:`~multiassayexperiment.MultiAssayExperiment.MultiAssayExperiment`
    from its on-disk representation.

    This method should generally not be called directly but instead be invoked by
    :py:meth:`~dolomite_base.read_object.read_object`.

    Args:
        path:
            Path to the directory containing the object.

        metadata:
            Metadata for the object.

        kwargs:
            Further arguments.

    Returns:
        A
        :py:class:`~multiassayexperiment.MultiAssayExperiment.MultiAssayExperiment`
        with file-backed arrays in the assays.
    """

    _sample_path = os.path.join(path, "sample_data")
    _sample_data = None
    if os.path.exists(_sample_path):
        _sample_data = dl.alt_read_object(_sample_path, **kwargs)

    if _sample_data is None:
        raise RuntimeError("Cannot read 'sample_data'.")

    _srow_names = _sample_data.get_row_names()
    if _srow_names is None:
        raise RuntimeError("'sample_data' does not contain 'row_names'.")

    _expts_path = os.path.join(path, "experiments")
    _expts = {}
    _expt_names = []
    _sample_map_data = None
    if os.path.exists(_expts_path):
        with open(os.path.join(_expts_path, "names.json"), "r") as handle:
            _expt_names = json.load(handle)

        if len(_expt_names) > 0:
            _sample_map_path = os.path.join(path, "sample_map.h5")
            _shandle = h5py.File(_sample_map_path, "r")
            _sghandle = _shandle["multi_sample_dataset"]
            _primary = []
            _assay = []
            _colname = []

            for _aidx, _aname in enumerate(_expt_names):
                _expt_read_path = os.path.join(_expts_path, str(_aidx))

                try:
                    _expts[_aname] = dl.alt_read_object(_expt_read_path, **kwargs)
                except Exception as ex:
                    raise RuntimeError(
                        f"failed to load experiment '{_aname}' from '{path}'; "
                        + str(ex)
                    )

                _expt_map = dl.load_vector_from_hdf5(
                    _sghandle[str(_aidx)], expected_type=int, report_1darray=True
                )

                _assay.extend([_aname] * _expts[_aname].shape[1])
                _colname.extend(_expts[_aname].get_column_names())
                _primary.extend([_srow_names[i] for i in _expt_map])

            _sample_map_data = BiocFrame(
                {"primary": _primary, "colname": _colname, "assay": _assay}
            )

    mae = MultiAssayExperiment(
        experiments=_expts, column_data=_sample_data, sample_map=_sample_map_data
    )

    _meta_path = os.path.join(path, "other_data")
    if os.path.exists(_meta_path):
        _meta = dl.alt_read_object(_meta_path, **kwargs)
        mae = mae.set_metadata(_meta.as_dict())

    return mae
