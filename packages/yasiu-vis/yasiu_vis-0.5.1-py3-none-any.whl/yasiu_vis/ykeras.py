import matplotlib.pyplot as _plt
import numpy as _np
# from matplotlib.cm import get_cmap as _get_cmap
from matplotlib.colors import Normalize as _Normalize
from keras.models import Model as _Model


def plotLayersWeights(
    layers, innerCanvas=1, midScale=0.8,
    numFmt=">4.2f",
    figsize=(40, 30), dpi=70,
    drawVertical=False,
    separateFirstLast=True,
    normalizeColors=False,
    scaleWeights=None,
):
    """
    Draws layers weights onto matplotlib figure.

    layers: keras `Model` or `list` of keras `Layers`

    innerCanvas: rows/columns for hidden layers.

    midScale:Scales ratio for hidden layers when using `separateFirstLast` default 0.8

    numFmt: number formatter (omited when using `scaleWeights`)

    figsize: `tuple` of `int`s, passed to `pyplot.figure(figsize=figsize)`

    dpi: integer, default=70, passed to `pyplot.figure(dpi=dpi)`

    drawVertical: boolean, stack layers in vertical or horizontal direction

    separateFirstLast: boolean, draw first and last layer independent from hidden layers

    normalizeColors: boolean, Plot each layer in range of indiviudal values <min ,max>

    scaleWeights: `int` or `float`: multiply weights and draw rounded integers instad.
        Use 100 or 1000. (Less clutter on plot). Default 0.

    """
    if isinstance(layers, (_Model,)):
        layers = layers.layers

    elif not isinstance(layers, (list,)):
        layers = [layers]

    if innerCanvas == 1:
        separateFirstLast = False

    canvasSizes = []
    # if len(layers) > 2:
    if separateFirstLast:
        shapes = [lay.get_weights()[0].shape for lay in layers[1:-1]]
    else:
        shapes = [lay.get_weights()[0].shape for lay in layers]

    htemp = []
    for i in range(len(shapes)):
        if i % innerCanvas and innerCanvas > 1:
            "Skip columnes other ahtn first"
            continue

        if (i+innerCanvas) < len(shapes):
            if innerCanvas <= 1:
                shape_scope = [shapes[i]]
            else:
                shape_scope = shapes[i: i+innerCanvas-1]
            sizes = [min(sh) for sh in shape_scope]
            htemp.append(max(sizes) * midScale)

        else:
            # h1, w1 = shapes[i]
            htemp.append(min(shapes[i]) * midScale)
        canvasSizes = htemp
    del htemp

    if separateFirstLast:
        canvasSizes = [
            1.0,
            *canvasSizes,
            1.0
        ]
    elif False:
        pass

    canvasSizes = [c if c > 2.0 else 2.0 for c in canvasSizes]
    all_axes = []

    # print("All ratios:", canvasSizes)
    plots_num = len(canvasSizes)

    fig = _plt.figure(figsize=figsize, dpi=dpi)
    if drawVertical:
        grid = fig.add_gridspec(len(canvasSizes), 1, height_ratios=canvasSizes)
    else:
        grid = fig.add_gridspec(1, len(canvasSizes),  width_ratios=canvasSizes)

    if separateFirstLast:
        "Create separate input"
        ax_first = fig.add_subplot(grid[0, 0])
        all_axes.append(ax_first)

    if separateFirstLast:
        "Skip first row/col"
        end = plots_num - 2 + 1
        start = 1
    else:
        end = plots_num
        start = 0

    for i in range(start, end):
        for j in range(innerCanvas):
            if drawVertical:
                ax = fig.add_subplot(
                    grid[i, 0].subgridspec(1, innerCanvas)[0, j])
            else:
                ax = fig.add_subplot(
                    grid[0, i].subgridspec(innerCanvas, 1)[j, 0])
            all_axes.append(ax)
            # print(f"axes now: {len(all_axes)}")

    if separateFirstLast:
        if drawVertical:
            ax_last = fig.add_subplot(grid[-1, 0])
        else:
            ax_last = fig.add_subplot(grid[0, -1])
        all_axes.append(ax_last)

    if normalizeColors:
        "Allow matplotlib to normalize values"
        my_norm = None
    else:
        my_norm = _Normalize(vmin=-1, vmax=1)

    for lind, lay in enumerate(layers):
        # print(f"Plotting layer index {lind} ({lay.name})")
        ax = all_axes[lind]

        weights, biases = lay.get_weights()
        weights_visualization = weights.copy()
        biases_visualization = _np.expand_dims(
            biases, axis=0)  # Rozszerzenie wymiaru biasów

        # Połączenie wag i biasów w jedną tablicę dla wizualizacji
        combined_visualization = _np.vstack(
            [weights_visualization, biases_visualization])

        is_bias_onRight = False
        H, W = combined_visualization.shape

        if lind == 0:
            # is_bias_onRight = True
            if (drawVertical and (H > W)) or not drawVertical and W > H:
                combined_visualization = combined_visualization.T
                is_bias_onRight = True

        elif lind == len(layers)-1:
            ax = all_axes[-1]
            if drawVertical:
                combined_visualization = combined_visualization.T
                is_bias_onRight = True

        else:
            if (H > W) and drawVertical or not drawVertical and W > H:
                combined_visualization = combined_visualization.T
                is_bias_onRight = True

        ax.matshow(combined_visualization, cmap="viridis", norm=my_norm)

        if type(scaleWeights) in [int, float]:
            "Vectorized scaling"
            combined_visualization = (
                combined_visualization*scaleWeights).round().astype(int)

        for (i, j), val in _np.ndenumerate(combined_visualization):
            if type(scaleWeights) in [int, float]:
                numText = str(val)
            else:
                numText = f"{val:{numFmt}}"

            ax.text(
                j, i, numText, ha='center',
                va='center', color='white', fontsize=10
            )

        if is_bias_onRight:
            ticks = ax.get_xticks()[1:-1]
            tick_strings = [f"$W_{'{'}{int(val)}{'}'}$" for val in ticks]
            tick_strings[-1] = "Bias"
            ax.set_xticks(ticks, tick_strings, rotation=15)
            ax.set_ylabel("Nodes")

        else:
            ticks = ax.get_yticks()[1:-1]
            tick_strings = [f"$W_{'{'}{int(val)}{'}'}$" for val in ticks]
            tick_strings[-1] = "Bias"
            ax.set_yticks(ticks, tick_strings, rotation=40)
            ax.set_xlabel("Nodes")

        ax.set_title(f" Layer: {lind} ({lay.name})")
        ax.grid(0)

    _plt.tight_layout()
    if drawVertical:
        _plt.subplots_adjust(hspace=0.1, wspace=0.01,)
    else:
        _plt.subplots_adjust(wspace=0.03, hspace=0.07,)


__all__ = [
    "plotLayersWeights"
]

if __name__ == "__main__":
    inputSize = 4

    import keras
    import os

    model = keras.models.Sequential()
    model.add(keras.Input(shape=(inputSize,)))
    model.add(keras.layers.Dense(20, activation="leaky_relu"))
    model.add(keras.layers.Dense(10, activation="leaky_relu"))
    # model.add(keras.layers.Dense(10, activation="leaky_relu"))
    # model.add(keras.layers.Dense(10, activation="leaky_relu"))
    # model.add(keras.layers.Dense(10, activation="leaky_relu"))
    model.add(keras.layers.Dense(10, activation="leaky_relu"))
    model.add(keras.layers.Dense(2, activation="linear"))

    optim = keras.optimizers.Adam(learning_rate=0.001)
    model.compile(loss="mse", optimizer=optim)

    X = _np.random.random((1000, 4))
    Y = X[:, :2] + X[:, 2:]

    model.fit(X, Y, epochs=20)

    plotLayersWeights(
        model, innerCanvas=1,
        figsize=(15, 12), dpi=80, scaleWeights=1000
    )

    _plt.suptitle(
        "Sequnetial model with dense layers. Weights are scaled for readability", size=20)
    _plt.subplots_adjust(wspace=0.12, top=0.93)
    _plt.tight_layout()
    picPath = os.path.join(os.path.dirname(__file__),
                           "..", "pics", "kerasLayers.png")
    _plt.savefig(f"{picPath}")
