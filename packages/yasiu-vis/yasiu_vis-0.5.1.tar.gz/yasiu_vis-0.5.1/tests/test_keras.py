import pytest

import keras
import os

from yasiu_vis.ykeras import plotLayersWeights
from matplotlib import pyplot as plt


def new_model():
    inputSize = 4
    model = keras.models.Sequential()
    model.add(keras.Input(shape=(inputSize,)))
    model.add(keras.layers.Dense(20, activation="leaky_relu"))
    model.add(keras.layers.Dense(10, activation="leaky_relu"))
    model.add(keras.layers.Dense(10, activation="leaky_relu"))
    model.add(keras.layers.Dense(10, activation="leaky_relu"))
    model.add(keras.layers.Dense(10, activation="leaky_relu"))
    model.add(keras.layers.Dense(10, activation="leaky_relu"))
    model.add(keras.layers.Dense(10, activation="leaky_relu"))
    model.add(keras.layers.Dense(2, activation="linear"))

    optim = keras.optimizers.Adam(learning_rate=0.001)
    model.compile(loss="mse", optimizer=optim)

    return model


def test_plotSequential1():
    model = new_model()
    plotLayersWeights(model.layers)
    plt.close()


def test_plotSequential2():
    model = new_model()
    plotLayersWeights(model.layers)
    plt.close()


def test_plotSequential3():
    model = new_model()
    plotLayersWeights([model.layers[0]])
    plt.close()


def test_plotSequential4():
    model = new_model()
    plotLayersWeights(model)
    plt.close()


@pytest.mark.parametrize("innerCanvas", [1, 3, 5])
@pytest.mark.parametrize("midScale", [0.5, 0.8])
@pytest.mark.parametrize("drawVertical", [True, False])
@pytest.mark.parametrize("separateFirstLast", [True, False])
@pytest.mark.parametrize("normalizeColors", [True, False])
@pytest.mark.parametrize("scaleWeights", [None, 10, 100])
def test_arguments(
    innerCanvas, midScale,
    drawVertical, separateFirstLast, normalizeColors,
    scaleWeights
):
    model = new_model()
    plotLayersWeights(
        model,
        innerCanvas=innerCanvas,
        midScale=midScale,
        drawVertical=drawVertical,
        # figsize=(3, 4), dpi=40,
        separateFirstLast=separateFirstLast,
        normalizeColors=normalizeColors,
        scaleWeights=scaleWeights,
    )
    plt.close()
