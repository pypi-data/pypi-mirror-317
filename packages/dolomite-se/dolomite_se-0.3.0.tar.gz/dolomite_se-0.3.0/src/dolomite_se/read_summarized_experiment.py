import os

import dolomite_base as dl
from dolomite_base.read_object import read_object_registry
from summarizedexperiment import SummarizedExperiment

from .utils import read_common_se_props

read_object_registry["summarized_experiment"] = "dolomite_se.read_summarized_experiment"


def read_summarized_experiment(
    path: str, metadata: dict, **kwargs
) -> SummarizedExperiment:
    """Load a
    :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`
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
        :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`
        with file-backed arrays in the assays.
    """

    _row_data, _column_data, _assays = read_common_se_props(path, **kwargs)

    se = SummarizedExperiment(
        assays=_assays, row_data=_row_data, column_data=_column_data
    )

    _meta_path = os.path.join(path, "other_data")
    if os.path.exists(_meta_path):
        _meta = dl.alt_read_object(_meta_path, **kwargs)
        se = se.set_metadata(_meta.as_dict())

    return se
