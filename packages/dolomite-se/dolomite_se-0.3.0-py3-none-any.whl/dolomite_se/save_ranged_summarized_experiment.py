import os

import dolomite_base as dl
from summarizedexperiment import RangedSummarizedExperiment, SummarizedExperiment
from .save_summarized_experiment import save_summarized_experiment


@dl.save_object.register
@dl.validate_saves
def save_ranged_summarized_experiment(
    x: RangedSummarizedExperiment,
    path: str,
    data_frame_args: dict = None,
    assay_args: dict = None,
    **kwargs,
):
    """Method for saving
    :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`
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

    if data_frame_args is None:
        data_frame_args = {}

    if assay_args is None:
        assay_args = {}

    # We do not respond to application overrides for the SummarizedExperiment
    # base class. Developers should just pretend that method copied all of the
    # code from the save_SE function; this call is just an implementation
    # detail, nothing special is done about the fact that it's the base class.
    #
    # This simplifies the dispatch and ensures that an override is only called
    # once. Consider the alternative - namely, casting to the next subclass and
    # then calling alt_save_object to respect the override. This would call
    # the override's SE method repeatedly for every step from the subclass to
    # SE. If the override's behavior is not idempotent, we have a problem.
    # 
    # So, if an application wants to set an override for all SEs, then it
    # should register an SE method for alt_save_object and then call it. If the
    # override is slightly different for particular SE subclasses, developers
    # should just duplicate the common override logic in the alt_save_object
    # methods for affected subclasses, rather than expecting some injection of
    # the overriding method into the save_object dispatch hierarchy.
    save_summarized_experiment(
        x, path, data_frame_args=data_frame_args, assay_args=assay_args, **kwargs
    )

    # save row_ranges
    _ranges = x.get_row_ranges()
    if _ranges is not None:
        dl.alt_save_object(_ranges, path=os.path.join(path, "row_ranges"), **kwargs)

    # modify OBJECT
    _info = dl.read_object_file(path)
    _info["ranged_summarized_experiment"] = {"version": "1.0"}
    dl.save_object_file(path, "ranged_summarized_experiment", _info)

    return
