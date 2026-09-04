# Specific Heat Explorer — Interactive C<sub>p</sub> vs. T Database

A minimalist Streamlit dashboard for plotting and comparing the **specific heat
capacity at constant pressure (C<sub>p</sub>)** of engineering materials as a
function of **temperature (T)**. Built for the group project brief
*"Interactive (C<sub>p</sub> vs. T) Database for Engineering Materials."*

![overview](preview.png)

## How to run

You need Python 3.9+ installed.

```bash
# 1. (optional) create a clean environment
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

# 2. install the dependencies
pip install -r requirements.txt

# 3. launch the app  (keep app.py and materials.csv in the same folder)
streamlit run app.py
```

Your browser opens at `http://localhost:8501`. To submit it as a *link*, you
can deploy the same folder for free on **share.streamlit.io** (Streamlit
Community Cloud) — no code changes needed.

## What it does (mapped to the brief)

| Requirement in the brief | Where it lives in the app |
|---|---|
| Searchable material list / drop-down | Sidebar **search box** + multi-select |
| Selection of material categories | Sidebar **Categories** filter |
| Plot one or several materials at once | Main **C<sub>p</sub>–T chart** (overlaid curves) |
| Comparison of C<sub>p</sub> values | **Compare at a temperature** tab (bar chart) |
| User-defined temperature range | Sidebar **temperature slider** |
| Name, formula, category, data source | **Material details** tab |
| Zoom, pan, cursor values / data tips | Interactive Plotly chart (drag-zoom, hover) |
| Clear axis titles, units, legend | Labelled axes, `J kg⁻¹ K⁻¹`, legend |
| Warning when T is outside the valid range | Amber **⚠️ warning banner** |
| Extra: ranking, export | **Rankings** tab + **CSV / PNG export** |

## Method & data notes

- **Equation.** Each curve is evaluated from the temperature polynomial fitted
  to the source data:

  `Cp(T) = a0 + a1·T + a2·T² + a3·T³`  in **J/(kg·K)**.

  These `a0…a3` coefficients are provided for every material in `materials.csv`,
  which makes the units consistent across metals, ceramics, polymers, glasses,
  etc. (Specific heat = per unit **mass**, matching the project's "specific
  heat" focus.)

- **Valid ranges.** Every fit is only used inside its listed `[T_min, T_max]`.
  Ask for a wider window and the app clips the curve and warns you — exactly as
  the brief requires.

- **Multi-phase materials.** Materials with several phases (e.g. Iron: α, the
  Curie region, γ+δ) are stored as several rows in the CSV. The app stitches
  them into a **single selectable material** and switches to the correct
  segment at each temperature.

- **Physical safeguard.** A few source fits (notably the narrow Curie-transition
  segment of iron) go non-physical if pushed. Any point that would return a
  negative or absurdly large C<sub>p</sub> is hidden so one bad fit can't
  distort the chart; you see a clean break in the line instead.

- **Sources.** All data comes from the cited references in `materials.csv`
  (NIST-JANAF / NIST Chemistry WebBook, Touloukian TPMD, ASM Handbook, ATHAS /
  SpringerMaterials, Bansal & Doremus, manufacturer datasheets, and journal
  articles). The source string is shown per material in the **Details** tab.

## ⚠️ One thing to check before submitting

## ✅ Project Requirement Met (200+ Materials)

The project brief asks for **at least 200 materials**. The `materials.csv` database currently holds **218 rows (205 unique materials)** across 8 classes, fully satisfying the thermodynamic data requirement. All materials include proper citations to reliable thermodynamic sources.

## Files

| File | Purpose |
|---|---|
| `app.py` | The Streamlit application |
| `materials.csv` | The materials database (edit/extend this) |
| `requirements.txt` | Python dependencies |
| `.streamlit/config.toml` | Light, minimalist theme |
| `test_logic.py` | Physics/data unit tests (`python test_logic.py`) |
| `test_ui_smoke.py` | End-to-end UI flow smoke test |

*Note: the assignment says not to submit source code as the primary
deliverable — submit the running dashboard (a Streamlit Cloud link or a
screen-recorded demo). Keep this project folder as your working source.*
