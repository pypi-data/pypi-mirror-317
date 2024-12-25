import os

import dolomite_base as dl
from dolomite_base.read_object import read_object_registry
from summarizedexperiment import RangedSummarizedExperiment
from .read_summarized_experiment import read_summarized_experiment

read_object_registry["ranged_summarized_experiment"] = (
    "dolomite_se.read_ranged_summarized_experiment"
)


def read_ranged_summarized_experiment(
    path: str, metadata: dict, **kwargs
) -> RangedSummarizedExperiment:
    """Load a
    :py:class:`~summarizedexperiment.RangedSummarizedExperiment.RangedSummarizedExperiment`
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
        :py:class:`~summarizedexperiment.RangedSummarizedExperiment.RangedSummarizedExperiment`
        with file-backed arrays in the assays.
    """

    # We don't try to respect application overrides when loading the base
    # instance. Application developers should just pretend that we copied the
    # code from read_summarized_experiment, rather than trying to inject in
    # custom code at this point, which gets too complicated - see the
    # associated commentary for save_ranged_summarized_experiment.
    se = read_summarized_experiment(path, metadata=metadata, **kwargs)

    rse = RangedSummarizedExperiment(
        assays=se.get_assays(),
        row_data=se.get_row_data(),
        column_data=se.get_column_data(),
        metadata=se.get_metadata(),
    )

    _ranges_path = os.path.join(path, "row_ranges")
    if os.path.exists(_ranges_path):
        _ranges = dl.alt_read_object(_ranges_path, **kwargs)
        rse = rse.set_row_ranges(_ranges)

    return rse
