
# Copilot Instructions for power-app

## Project Overview

`power-app` is an interactive educational notebook built with [marimo](https://marimo.io) that teaches regression analysis using the Palmer Penguins dataset. It's a Python-based application that compiles to a standalone HTML + WebAssembly app deployable to GitHub Pages.

## Build, Test & Deployment

### Development Commands

Use `uv` (fast Python package manager) with the provided Makefile:

- **`make install`** - Install locked dependencies via `uv sync --locked`
- **`make dev`** - Start dev server with hot-reload at `http://127.0.0.1:2718`
  - Runs: `uv run marimo edit app.py --watch --sandbox --host 127.0.0.1 --port 2718`
- **`make check`** - Validate marimo notebook syntax: `uv run marimo check app.py`
- **`make build`** - Runs `check` then exports to static HTML+WASM in `dist/` directory
  - Command: `uv run marimo export html-wasm app.py -o dist --mode run`
- **`make serve`** - Build + serve locally at `http://localhost:8000`
  - Uses Python's built-in HTTP server
- **`make test`** - Composite target: runs `install`, `check`, and `build` sequentially
- **`make clean`** - Remove the `dist/` build directory

### CI/CD

GitHub Actions workflow (`.github/workflows/deploy.yml`):
- Triggered on push to `main` or manual dispatch
- Installs Python 3.12 via `uv`, builds the app, and deploys to GitHub Pages
- Auto-deploys to the live site when merged to main

## Architecture & Key Conventions

### Project Structure

```
power-app/
├── app.py              # Main marimo notebook (entry point)
├── src/
│   ├── __init__.py
│   └── plots.py        # Plotting utilities (correlation plots, regression plots)
├── public/
│   └── custom.css      # Custom CSS for styling (referenced in app.py)
└── pyproject.toml      # Dependencies & project config
```

### Marimo Notebook Pattern

The `app.py` file is a marimo notebook with:
- **Header** - Python script dependencies declared in a PEP 723 comment block
- **App initialization** - `marimo.App()` with `width="medium"`, custom CSS file, and title
- **Cells** - Each function decorated with `@app.cell()` is a reactive cell
  - Cells with `hide_code=True` hide their source, showing only rendered output
  - Use `mo` (marimo object) for markdown, plots, and widgets

**Key pattern**: Cells are functions with parameters that marimo automatically wires based on return values from other cells. This creates a reactive dependency graph.

### Python & Dependencies

- **Python version**: 3.12+ (specified in `pyproject.toml` and `.python-version`)
- **Package manager**: `uv` (fast, deterministic; lock file in `uv.lock`)
- **Key dependencies**:
  - `marimo` - Notebook framework
  - `matplotlib`, `seaborn`, `numpy`, `pandas` - Data visualization & manipulation
  - `scipy`, `statsmodels` - Statistical modeling (declared in app.py's script block)
  - `altair` - Additional plotting (in app.py dependencies)

**Important**: The app.py file has its own dependency declaration (Python script header) separate from `pyproject.toml`. When adding libraries used in the notebook, update both places:
1. The `# dependencies = [...]` comment block in app.py
2. The `dependencies` list in `pyproject.toml` (for reproducible builds)

### Plots Module

`src/plots.py` contains reusable visualization functions:
- **`make_cor_plot(corr)`** - Generates a scatter plot with regression line showing correlation coefficient
  - Takes a correlation value (0 to 1) and generates synthetic data
  - Uses seaborn for styling, matplotlib for plotting
  - Displays correlation (R) on the plot

Patterns to follow:
- Use `seaborn.set_theme()` for consistent styling
- Set random seeds for reproducibility
- Use `sns.regplot()` for regression visualization
- Include explanatory text annotations on plots

### CSS & Styling

Custom CSS is specified in `app.py`:
```python
app = marimo.App(css_file="public/custom.css", ...)
```

The file `public/custom.css` is referenced but not tracked in git; create it as needed for custom styling of the notebook UI.

## Development Workflow

1. **Edit the notebook** - Modify `app.py` or `src/` modules
2. **Run dev mode** - `make dev` for instant feedback
3. **Test changes** - `make build` validates and builds
4. **Commit & push** - CI/CD automatically deploys to GitHub Pages

## Common Tasks

- **Add a new visualization** - Create a function in `src/plots.py`, import in `app.py`, call in a cell
- **Add a library** - Update dependencies in both `app.py`'s script block and `pyproject.toml`; run `uv sync --locked`
- **Debug locally** - Use `make dev` and open DevTools; marimo provides cell-level error messages
- **Deploy** - Push to `main` and wait for GitHub Actions (no manual build step needed)
