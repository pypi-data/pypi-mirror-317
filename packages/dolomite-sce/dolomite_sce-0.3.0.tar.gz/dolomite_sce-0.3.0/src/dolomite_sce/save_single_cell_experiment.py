import json
import os

import dolomite_base as dl
import dolomite_se as dlse
from singlecellexperiment import SingleCellExperiment
from summarizedexperiment import RangedSummarizedExperiment


@dl.save_object.register
@dl.validate_saves
def save_single_cell_experiment(
    x: SingleCellExperiment,
    path: str,
    data_frame_args: dict = None,
    assay_args: dict = None,
    rdim_args: dict = None,
    alt_expts_args: dict = None,
    **kwargs,
):
    """Method for saving
    :py:class:`~singlecellexperiment.SingleCellExperiment.SingleCellExperiment`
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

        rdim_args:
            Further arguments to pass to the ``save_object`` method for the
            reduced dimensions.

        alt_expts_args:
            Further arguments to pass to the ``save_object`` method for the
            alternative experiments.

        kwargs:
            Further arguments.

    Returns:
        ``x`` is saved to path.
    """
    if data_frame_args is None:
        data_frame_args = {}

    if assay_args is None:
        assay_args = {}

    if rdim_args is None:
        rdim_args = {}

    if alt_expts_args is None:
        alt_expts_args = {}

    # see comments in save_ranged_summarized_experiment in dolomite_se.
    dlse.save_ranged_summarized_experiment(
        x, path, data_frame_args=data_frame_args, assay_args=assay_args, **kwargs
    )

    # Modify OBJECT
    _info = dl.read_object_file(path)
    _info["single_cell_experiment"] = {"version": "1.0"}
    if x.get_main_experiment_name() is not None:
        _info["single_cell_experiment"]["main_experiment_name"] = str(
            x.get_main_experiment_name()
        )
    dl.save_object_file(path, "single_cell_experiment", _info)

    # save rdims
    _rdim_names = x.get_reduced_dim_names()
    if len(_rdim_names) > 0:
        _rdim_path = os.path.join(path, "reduced_dimensions")
        os.mkdir(_rdim_path)

        with open(os.path.join(_rdim_path, "names.json"), "w") as handle:
            json.dump(_rdim_names, handle)

        for _aidx, _aname in enumerate(_rdim_names):
            _rdim_save_path = os.path.join(_rdim_path, str(_aidx))
            try:
                dl.alt_save_object(
                    x.reduced_dim(_aname), path=_rdim_save_path, **rdim_args, **kwargs
                )
            except Exception as ex:
                raise RuntimeError(
                    "failed to stage reduced dimension '"
                    + _aname
                    + "' for "
                    + str(type(x))
                    + "; "
                    + str(ex)
                )

    # save alt expts.
    _alt_names = x.get_alternative_experiment_names()
    if len(_alt_names) > 0:
        _alt_path = os.path.join(path, "alternative_experiments")
        os.mkdir(_alt_path)

        with open(os.path.join(_alt_path, "names.json"), "w") as handle:
            json.dump(_alt_names, handle)

        for _aidx, _aname in enumerate(_alt_names):
            _alt_save_path = os.path.join(_alt_path, str(_aidx))
            try:
                dl.alt_save_object(
                    x.alternative_experiment(_aname),
                    path=_alt_save_path,
                    **alt_expts_args,
                    **kwargs,
                )
            except Exception as ex:
                raise RuntimeError(
                    "failed to stage alternative experiment '"
                    + _aname
                    + "' for "
                    + str(type(x))
                    + "; "
                    + str(ex)
                )
    return
