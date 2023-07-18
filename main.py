import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import List
plt.style.use("ggplot")

months: List[str] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]    


def make_gif(xvalues: List[float],
             yvalues: List[float],
             oname: str = "tokyo.gif",
             interval: int = 3) -> None:
    M: int = len(xvalues)
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6), dpi=150)

    # 見た目の調整
    # 1. gridをつける
    # 2. N方向 (上) を 0°にする
    # 3. 回転を時計回りにする (-1)
    # 4. 値域の設定
    # 5. 軸を月の名前にする
    ax.grid(True)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_ylim([-5.0, 5.0])
    ax.set_xticks(np.linspace(0, 2 * np.pi, num=12, endpoint=False))
    ax.set_xticklabels(months)

    # 更新関数 (i番目の線分を作る)
    def plot(i):
        plt.cla()
        # 設定
        ax.grid(True)
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_ylim([-5.0, 5.0])
        ax.set_xticks(np.linspace(0, 2 * np.pi, num=12, endpoint=False))
        ax.set_xticklabels(months)

        # タイトル (年)
        off = i // 12
        year = 1876 + off
        ax.set_title(f"Year {year}")

        # これまでのプロット (薄く) / 新しいプロット (赤色)
        prevs_xx = [xvalues[k] for k in range(i + 1)]
        prevs_yy = [yvalues[k] for k in range(i + 1)]
        if prevs_xx:
            ax.plot(prevs_xx, prevs_yy, color="k", alpha=0.2)

        if i < len(xvalues) - 1:
            xx = [xvalues[i], xvalues[i + 1]]
            yy = [yvalues[i], yvalues[i + 1]]
            ax.plot(xx, yy, color="r", alpha=0.5)

    # 保存する
    ani = animation.FuncAnimation(fig, plot, save_count=M, interval=interval, repeat=False)
    ani.save(oname)


def main(fn: str = "./data/tokyo.csv") -> None:
    df = pd.read_csv(fn)

    # 1. 年データを落とす
    # 2. 全データの平均からの差分を求める
    df.drop("Annual", inplace=True, axis=1)
    data = df[months] - df[months].mean()
    
    # 円周上にplotする準備 (2\pi/12)
    # dataを[rbase, rbase, ...], [values[1876], values[1877], ...] と並べる
    rbase: np.ndarray = np.linspace(0, 2 * np.pi, num=12, endpoint=False)
    xvalues: List[float] = []
    yvalues: List[float] = []
    for (i, row) in data.iterrows():
        for j in rbase:
            xvalues.append(j)
        for j in row.values:
            yvalues.append(j)

    # gifファイルを作成する
    make_gif(
        xvalues,
        yvalues,
        "tokyo.gif"
    )


if __name__ == '__main__':
    main()