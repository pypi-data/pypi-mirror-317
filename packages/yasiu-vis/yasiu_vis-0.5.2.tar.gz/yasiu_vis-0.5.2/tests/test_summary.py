import pytest
import pandas as pd
import matplotlib.pyplot as plt
import os

from yasiu_vis.ypandas import summary_plot, random_data_frame


@pytest.fixture()
def short_data_frame():
    df = pd.DataFrame(columns=['colA', 'colB', 'colC'], dtype=float)
    for i in range(15):
        # df.loc[i, :] = [f'{i}A', f'{i}B', f'{i}C']
        df.loc[i, :] = [i, i, i]
    # df.loc[1, :] = ['A', 'B', 'C']
    # df.loc[2, :] = ['A', 'B', 'C']
    # print()
    # print(df)
    # print(df.dtypes)

    return df


def test_first(short_data_frame):
    summary_plot(short_data_frame, show=False)
    # import matplotlib
    # pass
    plt.close()


testPicDir = os.path.join(os.path.dirname(__file__), "pics")
os.makedirs(testPicDir, exist_ok=True)

data_1 = [
    (cols, cls_n, loc)
    for cols in [1, 2, 16, 25]
    for cls_n in range(5, 15, 5)
    for loc in ['same', 'subplot']
]


@pytest.mark.parametrize("cols_n,cls_n,leg_loc", data_1)
def test_2_varying_data(cols_n, cls_n, leg_loc):
    data = random_data_frame(100, cols_n, cls_n)
    summary_plot(
        data, group_key='class', show=False,
        legend_place=leg_loc,
    )
    plt.close("all")


# @pytest.mark.parametrize("class_N", list(range(6, 25)))
# def test_3_varying_class_n(class_N):
#     data = random_data_frame(300, 10, classes_N=class_N)
#     summary_plot(data, group_key='class', show=False)
#     plt.savefig(f"test_pics{os.path.sep}test_3_out_{class_N}.png")
#     plt.close("all")


@pytest.mark.parametrize("class_N", list(range(5, 12)))
def test_4_grouping_values(class_N):
    data = random_data_frame(200, 10, classes_N=class_N)
    summary_plot(data, group_key='col-A', show=False)
    # plt.savefig(f"{testPicDir}{os.path.sep}test_4_out_{class_N}.png")
    plt.close("all")
