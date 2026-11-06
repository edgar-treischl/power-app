
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def make_cor_plot(corr):
    np.random.seed(6687)

    x = 1 + np.random.normal(100, 500, 1000)
    random1 = np.random.uniform(x.min(), x.max(), 1000)
    y = x * corr + random1 * (1 - corr)

    df = pd.DataFrame({"x": x, "y": y})

    r = round(df["x"].corr(df["y"]), 2)

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.set_theme(style="white", font_scale=1.2)

    sns.regplot(
        data=df,
        x="x",
        y="y",
        ci=None,
        scatter_kws={"alpha": 0.6},
        line_kws={"color": "blue"},
        ax=ax
    )

    ax.text(0, -1700, f"R = {r}", fontsize=15)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    fig.tight_layout()

    return fig
