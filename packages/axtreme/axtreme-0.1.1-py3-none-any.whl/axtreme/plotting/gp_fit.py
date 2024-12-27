"""Plotting module for visualizing how well the GP fits the data."""

from collections.abc import Callable
from typing import TypeAlias

import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.graph_objects
import plotly.subplots
import torch
from ax.core import ObservationFeatures, RangeParameter, SearchSpace
from ax.modelbridge.torch import TorchModelBridge
from botorch.models import SingleTaskGP
from botorch.posteriors.gpytorch import GPyTorchPosterior
from matplotlib.axes import Axes
from plotly.graph_objs import Figure, Scatter3d, Surface
from scipy.stats import norm

Numpy2dArray: TypeAlias = np.ndarray[tuple[int, int], np.dtype[np.float64]]
Numpy1dArray: TypeAlias = np.ndarray[tuple[int,], np.dtype[np.float64]]


def plot_surface_over_2d_search_space(
    search_space: SearchSpace,
    funcs: list[Callable[[Numpy2dArray], Numpy1dArray]],
    colors: list[str] | None = None,
    num_points: int = 101,
) -> Figure:
    """Creates a figure with the functions in funcs ploted over the search_space.

    Note:
        Currently only support search spaces with 2 parameters.

    Args:
        search_space: The search space over which the functions are to be evaluated and plotted.
        funcs: A list of callables that take in a numpy array with shape (num_values, num_parameters=2 )
            and return a numpy array with (num_values) elements.
        colors: A list of colors to use for each function. If None, will use default Plotly colors.
        num_points: The number of points in each dimension to evaluate the functions at.
    """
    # Extract the parameter names and ranges from the search space
    assert len(search_space.parameters) == 2, "Only 2D search spaces are supported for now."  # noqa: PLR2004

    (x1_name, x1_param), (x2_name, x2_param) = list(search_space.parameters.items())

    if not (isinstance(x1_param, RangeParameter) and isinstance(x2_param, RangeParameter)):
        msg = f"""Expect search_space.parameters to all be of type RangeParameter.
         Instead got {type(x1_param) = }, and {type(x2_param) = }."""
        raise NotImplementedError(msg)

    # Generate parameter ranges using NumPy
    x1_values = np.linspace(x1_param.lower, x1_param.upper, num_points)
    x2_values = np.linspace(x2_param.lower, x2_param.upper, num_points)

    # Create a meshgrid for the parameter values

    x1_grid, x2_grid = np.meshgrid(x1_values, x2_values)
    inputs = np.column_stack((x1_grid.flatten(), x2_grid.flatten()))

    func_results = [func(inputs) for func in funcs]

    # Create a 3D surface plot using Plotly
    surfaces = []
    _none_list: list[None] = [None] * len(funcs)
    colour_list: list[str] | list[None] = colors or _none_list
    for func_result, color in zip(func_results, colour_list, strict=True):
        surface = plotly.graph_objects.Surface(
            x=x1_values,
            y=x2_values,
            z=func_result.reshape(x1_grid.shape),
            opacity=0.7,
            colorscale=color,
        )
        surfaces.append(surface)

    return plotly.graph_objects.Figure(data=surfaces)


def scatter_plot_training(
    model_bridge: TorchModelBridge,
    metric_name: str,
    axis: tuple[int, int] = (0, 1),
    figure: Figure | None = None,
    *,
    error_bars: bool = True,
    error_bar_confidence_interval: float = 0.95,
) -> Figure:
    """Make a scattter plot of a metric for the training data of the model.

    Args:
        model_bridge: The model the training data scatter plot is to be made for.
        metric_name: The name of the metric to plot. Must match the name of a metric in the model.
        axis: The axis of the input space to plot the scatter plot in
        figure: The figure to add the scatter plot to. If None, a new figure is created.
        error_bars: Whether to add error bars to the plot.
        error_bar_confidence_interval: The confidence interval the error bars in the scatter plot represents.

    Returns:
        A Scatter3d plot of the training data for the given metric.
    """
    xs = np.array([list(obs.features.parameters.values()) for obs in model_bridge.get_training_data()])
    ys = []
    y_noise = []
    for obs in model_bridge.get_training_data():
        metric_index = obs.data.metric_names.index(metric_name)
        ys.append(obs.data.means[metric_index])
        y_noise.append(np.sqrt(obs.data.covariance[metric_index][metric_index]))

    figure = figure or plotly.graph_objects.Figure()
    scatter = Scatter3d(
        x=xs[:, axis[0]],
        y=xs[:, axis[1]],
        z=ys,
        mode="markers+text",
        marker={"size": 5, "color": "red"},
    )

    _ = figure.add_trace(scatter)
    if error_bars:
        if error_bar_confidence_interval >= 1.0:
            error_bar_confidence_interval = 1.0 - 1e-6
        elif error_bar_confidence_interval <= 0.0:
            error_bar_confidence_interval = 0.0

        standard_interval = norm.interval(error_bar_confidence_interval)
        # Add error bars
        for i in range(xs.shape[0]):
            _ = figure.add_trace(
                plotly.graph_objects.Scatter3d(
                    x=[
                        xs[i, axis[0]],
                        xs[i, axis[0]],
                    ],
                    y=[
                        xs[i, axis[1]],
                        xs[i, axis[1]],
                    ],
                    z=[
                        ys[i] + y_noise[i] * standard_interval[0],
                        ys[i] + y_noise[i] * standard_interval[1],
                    ],
                    mode="lines",
                    line={"color": "red"},
                )
            )
    return figure


def plot_gp_fits_2d_surface(  # noqa: C901
    model_bridge: TorchModelBridge,
    search_space: SearchSpace,
    metrics: dict[
        str,
        Callable[[Numpy2dArray], Numpy1dArray],
    ]
    | None = None,
    num_points: int = 101,
) -> Figure:
    """Plot the GP fit for the given metrics over the 2D search space.

    Args:
        model_bridge: The model bridge used to make predictions.
        search_space: The search space over which the functions are to be evaluated and plotted.
        metrics: A dictionary of metrics to plot. The keys are the names of the metrics in the model bridge model
            and the values are callables that return the metric value for a given input.
        num_points: The number of points in each dimension to evaluate the functions at.
    """
    # Extract the parameter names and ranges from the search space

    figs = []
    observations_names = search_space.parameters.keys()

    # Get metric names from the model
    metrics_names = list(model_bridge.metric_names)

    def pred_helper_closure(
        metric_name: str,
    ) -> Callable[[Numpy2dArray], Numpy1dArray]:
        def pred_helper(
            x: Numpy2dArray,
        ) -> Numpy1dArray:
            if len(x.shape) == 1:
                x = x.reshape(1, -1)
            pred_val_list = [
                model_bridge.predict(
                    [
                        ObservationFeatures(
                            parameters={
                                obs_name: x[i, obs_index] for obs_index, obs_name in enumerate(observations_names)
                            }
                        )
                    ]
                )[0][metric_name]
                for i in range(x.shape[0])
            ]
            return np.array(pred_val_list)

        return pred_helper

    for metric_name in metrics_names:
        fig = None
        funcs = [pred_helper_closure(metric_name)]
        colors = ["Reds"]

        # If we have a ground truth function for the metric add it to the plot
        if metrics is not None and metric_name in metrics:
            funcs.insert(0, metrics[metric_name])
            colors.insert(0, "Viridis")

        fig = plot_surface_over_2d_search_space(
            search_space=search_space,
            funcs=funcs,
            colors=colors,
            num_points=num_points,
        )

        fig = scatter_plot_training(
            model_bridge=model_bridge,
            metric_name=metric_name,
            figure=fig,
        )
        _ = fig.update_scenes(
            {
                "xaxis": {"title": "x1"},
                "yaxis": {"title": "x2"},
                "zaxis": {"title": "response"},
            }
        )
        figs.append(fig)

    ### Plot them side by side
    fig_subplots = plotly.subplots.make_subplots(
        rows=1,
        cols=len(metrics_names),
        specs=[[{"type": "surface"}, {"type": "surface"}]],
        subplot_titles=metrics_names,
    )

    for idx, fig in enumerate(figs):
        for data in fig.data:
            _ = fig_subplots.add_trace(data, row=1, col=idx + 1)

    _ = fig_subplots.update_scenes({"xaxis": {"title": "x1"}, "yaxis": {"title": "x2"}, "zaxis": {"title": "response"}})

    # Remove the colorbar and legend from the subplots
    for trace in fig_subplots.data:
        if isinstance(trace, Surface):
            _ = trace.update(showscale=False)
        elif isinstance(trace, Scatter3d):
            _ = trace.update(showlegend=False)
    return fig_subplots


def plot_1d_model(model: SingleTaskGP, X: torch.Tensor | None = None, ax: None | Axes = None) -> Axes:  # noqa: N803
    """Plots a model with 1d in put, and any number of outputs..

    Args:
        model: Only SingleTaskGp is supported an training data is extracted from the model.
        X: (n,1): Linspace of [0,1] is used by default. Only 1d is currently supported.
        ax: will plot to this axis if provied
    """
    X = X or torch.linspace(0, 1, 100).reshape(-1, 1)  # noqa: N806

    if ax is None:
        _, ax = plt.subplots()

    # Quick and dirty way to ensure consistent colours
    colours = ["b", "c", "m", "y", "k", "r"]

    train_x_all = model.train_inputs[0].detach()  # type: ignore  # noqa: PGH003
    train_y_all = model.train_targets.detach()
    train_var_all = model.likelihood.noise.detach()

    # t = 1 then:
    # shape model.train_targets: (n)
    # shape model.train_inputs: ((n,d),)
    if len(model.train_targets.shape) == 1:
        n_targets = 1
        # need to add a t dimension to all of these so they can be treated the same way as the multicase
        train_x_all = train_x_all.unsqueeze(0)
        train_y_all = train_y_all.unsqueeze(0)
        train_var_all = train_var_all.unsqueeze(0)

    # t > 1 then:
    # shape model.train_targets: (t,n)
    # shape model.train_inputs: ((t,n,d),)
    else:
        n_targets = model.train_targets.shape[-2]

    for target_idx in range(n_targets):
        c = colours[target_idx % len(colours)]

        train_x = train_x_all[target_idx]
        train_y = train_y_all[target_idx]
        train_var = train_var_all[target_idx]

        with torch.no_grad():
            posterior: GPyTorchPosterior = model.posterior(X)  # type: ignore  # noqa: PGH003

        mean = posterior.mean[:, target_idx]
        var = posterior.variance[:, target_idx]
        _ = ax.fill_between(X.flatten(), mean - 1.95 * var**0.5, mean + 1.95 * var**0.5, alpha=0.3, color=c)
        _ = ax.plot(X, mean, color=c, label=f"gp target {target_idx}")
        _ = ax.scatter(train_x.flatten(), train_y, color=c)
        _ = ax.errorbar(train_x.flatten(), train_y, 1.95 * train_var**0.5, fmt="o", color=c)

    _ = ax.set_title("Gp prediction")
    return ax
