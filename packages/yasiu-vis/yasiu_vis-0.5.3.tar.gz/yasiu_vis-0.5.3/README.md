# Readme of `yasiu-vis`

High level functions, to quickly visualise data frames.

# Installation

```shell
pip install yasiu-vis
```
# Modules list
- **ykeras**: Visualisation made for keras.Model
- **ypandas**: Visualisation made for pandas.DataFrame

# Examples

## Pandas - Drawing data frame

```py
from yasiu_vis.ypandas import summary_plot


# df: pandas.DataFrame
summary_plot(df, split_windows='group')
summary_plot(
    df, group_key='petal width (cm)', max_groups=4,
    plot_params=dict(alpha=0.7),
)

```
<!-- ![Summary Plot](./pics/summaryPlot.png) -->
![Dataset Summary Plot](https://raw.githubusercontent.com/GrzegorzKrug/yasiu-vis/refs/heads/main/pics/summaryPlot.png)

## Keras - Ploting Neural Network layers
```py
from yasiu_vis.ykeras import plotLayersWeights
from matpotlib import pyplot as plt
import keras

model : keras.models.Sequential # Keras compiled model

plotLayersWeights(model.layers, innerCanvas=1, figsize=(20, 15), dpi=70, scaleWeights=1000)
plt.suptitle("Sequnetial model with dense layers. Weights are scaled for readability", size=20)
plt.show()
```

<!-- ![Keras Weights](./pics/kerasLayers.png) -->
![Keras Weights](https://github.com/GrzegorzKrug/yasiu-vis/blob/main/pics/kerasLayers.png?raw=true)

# All packages

[1. Native Package](https://pypi.org/project/yasiu-native/)

[2. Math Package](https://pypi.org/project/yasiu-math/)

[3. Image Package](https://pypi.org/project/yasiu-image/)

[4. Visualisation Package](https://pypi.org/project/yasiu-vis/)

