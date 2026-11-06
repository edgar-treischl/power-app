# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.25.2",
#     "matplotlib==3.11.2",
#     "numpy==2.5.4",
#     "pandas==3.1.1",
#     "seaborn==0.13.2",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="medium",
    app_title="Palmer Regression Analysis",
    css_file="public/custom.css",
)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Regression in a Nutshell
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Learn how ordinary least squares (OLS) linear regression helps you understand
    the relationship between two variables.

    In this interactive notebook, you will work with the Palmer Penguins dataset.
    """)
    return


@app.cell
def _():
    from src.plots import (
            make_cor_plot,
        )

    return (make_cor_plot,)


@app.cell
def _(mo, make_cor_plot):
    corr = mo.ui.slider(
        start=-1.0,
        stop=1.0,
        step=0.05,
        value=0.7,
        label="Correlation"
    )

    corr
    return (corr,)


@app.cell
def _(corr, make_cor_plot):
    make_cor_plot(corr.value)
    return


if __name__ == "__main__":
    app.run()
