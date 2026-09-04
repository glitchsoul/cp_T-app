import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = Path(__file__).parent / "materials.csv"

COLS = [
    "idx", "name", "formula", "category", "cas", "tmin", "tmax",
    "A", "B", "C", "D", "E", "a0", "a1", "a2", "a3", "r2",
    "cp298", "molar", "density", "source", "notes",
]

NUMERIC = [
    "tmin", "tmax", "a0", "a1", "a2", "a3",
    "cp298", "molar", "density"
]

PALETTE = [
    "#0071E3",
    "#FF453A",
    "#34C759",
    "#FF9F0A",
    "#AF52DE",
    "#5AC8FA",
    "#FF375F",
    "#64D2FF",
]

CP_LO = 0.0
CP_HI = 20000.0
ACCENT = "#0071E3"


# ============================================================
# APPLE-LIKE MINIMAL UI
# ============================================================

CUSTOM_CSS = """
<style>

:root {
    --bg: #f5f5f7;
    --surface: #ffffff;
    --surface-soft: #fbfbfd;
    --text: #1d1d1f;
    --muted: #6e6e73;
    --line: #d2d2d7;
    --accent: #0071e3;
    --accent-soft: #e8f2ff;
}

/* ---------------------------------------------------------
   GLOBAL
--------------------------------------------------------- */

.stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
}

.block-container {
    max-width: 1320px;
    padding-top: 2.3rem;
    padding-bottom: 4rem;
}

#MainMenu,
footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: rgba(245, 245, 247, 0.88) !important;
}


/* ---------------------------------------------------------
   TYPOGRAPHY
--------------------------------------------------------- */

html,
body,
.stApp,
.stMarkdown,
p,
span,
label,
div,
button,
input,
textarea,
select {
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "SF Pro Display",
        "SF Pro Text",
        "Inter",
        "Segoe UI",
        sans-serif !important;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: var(--text) !important;
    letter-spacing: -0.025em !important;
}

p,
.stCaption,
small {
    color: var(--muted) !important;
}


/* ---------------------------------------------------------
   HEADER
--------------------------------------------------------- */

.app-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 30px;
    margin-bottom: 2rem;
}

.app-title {
    font-size: clamp(2.2rem, 4vw, 3.25rem);
    line-height: 1.02;
    font-weight: 700;
    letter-spacing: -0.05em;
    color: var(--text);
}

.app-sub {
    margin-top: 0.55rem;
    font-size: 1rem;
    color: var(--muted);
}

.header-meta {
    text-align: right;
    color: var(--muted);
    font-size: 0.82rem;
    line-height: 1.55;
}

.header-meta strong {
    color: var(--text);
    font-weight: 600;
}


/* ---------------------------------------------------------
   SECTION TITLES
--------------------------------------------------------- */

.eyebrow {
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 650;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.section-title {
    color: var(--text);
    font-size: 1.15rem;
    font-weight: 650;
    letter-spacing: -0.02em;
}


/* ---------------------------------------------------------
   INPUTS
--------------------------------------------------------- */

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {

    background: var(--surface) !important;
    color: var(--text) !important;

    border: 1px solid var(--line) !important;
    border-radius: 10px !important;

    min-height: 42px !important;

    box-shadow: none !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {

    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,113,227,0.12) !important;
}


/* ---------------------------------------------------------
   SELECT / MULTISELECT
--------------------------------------------------------- */

div[data-baseweb="select"] > div {

    background: var(--surface) !important;
    color: var(--text) !important;

    border-color: var(--line) !important;
    border-radius: 10px !important;

    box-shadow: none !important;
}

div[data-baseweb="tag"] {

    background: var(--accent-soft) !important;
    border: 0 !important;
    border-radius: 999px !important;

    padding-left: 8px !important;
    padding-right: 8px !important;
}

div[data-baseweb="tag"] span {
    color: #005bb5 !important;
}


/* ---------------------------------------------------------
   BUTTONS
--------------------------------------------------------- */

button[kind="primary"],
.stDownloadButton button {

    background: var(--accent) !important;
    color: white !important;

    border: 0 !important;
    border-radius: 10px !important;

    font-weight: 600 !important;

    transition: 0.15s ease !important;
}

button[kind="primary"]:hover,
.stDownloadButton button:hover {

    background: #0067cf !important;
    transform: translateY(-1px);
}

button[kind="secondary"] {

    background: var(--surface) !important;
    color: var(--text) !important;

    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
}


/* ---------------------------------------------------------
   SLIDER
--------------------------------------------------------- */

.stSlider [data-baseweb="slider"] {
    padding-top: 0.3rem;
}

.stSlider [role="slider"] {

    background: var(--accent) !important;
    border-color: var(--accent) !important;

    box-shadow: none !important;
}


/* ---------------------------------------------------------
   DIVIDERS
--------------------------------------------------------- */

hr {

    border: 0 !important;
    border-top: 1px solid var(--line) !important;

    margin: 1.3rem 0 !important;
}


/* ---------------------------------------------------------
   CHART CONTAINER
--------------------------------------------------------- */

.chart-shell {

    background: var(--surface);

    border: 1px solid rgba(210,210,215,0.85);

    border-radius: 18px;

    padding: 1.2rem 1.2rem 0.7rem;

    box-shadow:
        0 8px 30px rgba(0,0,0,0.035);
}

.chart-title {

    font-size: 1.22rem;

    font-weight: 650;

    letter-spacing: -0.025em;

    color: var(--text);
}

.chart-subtitle {

    font-size: 0.86rem;

    color: var(--muted);

    margin-top: 0.18rem;
}


/* ---------------------------------------------------------
   CONTEXT PILLS
--------------------------------------------------------- */

.context-row {

    display: flex;

    gap: 8px;

    flex-wrap: wrap;

    margin-top: 0.7rem;

    margin-bottom: 0.1rem;
}

.context-pill {

    font-size: 0.76rem;

    color: var(--muted);

    background: var(--surface-soft);

    border: 1px solid #e5e5ea;

    padding: 5px 9px;

    border-radius: 999px;
}


/* ---------------------------------------------------------
   RANGE WARNING
--------------------------------------------------------- */

.range-note {

    background: #fff8e6;

    border: 1px solid #ead8a4;

    color: #6b5200;

    border-radius: 10px;

    padding: 10px 13px;

    font-size: 0.82rem;

    margin: 0.5rem 0 0.9rem;
}

.range-note strong {
    color: #4f3d00;
}


/* ---------------------------------------------------------
   TABS
--------------------------------------------------------- */

.stTabs [data-baseweb="tab-list"] {

    gap: 4px;

    border-bottom: 1px solid var(--line);

    background: transparent;
}

.stTabs [data-baseweb="tab"] {

    color: var(--muted) !important;

    border-radius: 8px 8px 0 0 !important;

    padding: 0.65rem 1rem !important;

    font-weight: 550 !important;
}

.stTabs [aria-selected="true"] {

    color: var(--text) !important;

    border-bottom-color: var(--accent) !important;
}


/* ---------------------------------------------------------
   DATAFRAME
--------------------------------------------------------- */

div[data-testid="stDataFrame"] {

    border: 1px solid var(--line);

    border-radius: 12px;

    overflow: hidden;

    background: white;
}


/* ---------------------------------------------------------
   SIDEBAR
--------------------------------------------------------- */

section[data-testid="stSidebar"] {

    background: var(--surface) !important;

    border-right: 1px solid var(--line) !important;
}

section[data-testid="stSidebar"] * {
    color: var(--text) !important;
}


/* ---------------------------------------------------------
   RESPONSIVE
--------------------------------------------------------- */

@media (max-width: 800px) {

    .app-header {

        align-items: flex-start;

        flex-direction: column;
    }

    .header-meta {

        text-align: left;
    }

    .block-container {

        padding-top: 1.2rem;
    }
}

</style>
"""


# ============================================================
# DATA FUNCTIONS
# ============================================================

def build_materials(df: pd.DataFrame) -> dict:

    materials = {}

    for _, r in df.iterrows():

        name = str(r["name"]).strip()

        seg = {
            "tmin": r["tmin"],
            "tmax": r["tmax"],
            "a0": r["a0"],
            "a1": r["a1"],
            "a2": r["a2"],
            "a3": r["a3"],
            "notes": str(r["notes"]).strip(),
        }

        if not (
            np.isfinite(seg["tmin"])
            and np.isfinite(seg["tmax"])
        ):
            continue

        if name not in materials:

            materials[name] = {

                "name": name,

                "formula":
                    str(r["formula"]).strip(),

                "category":
                    str(r["category"]).strip(),

                "cas":
                    str(r["cas"]).strip(),

                "cp298":
                    r["cp298"],

                "molar":
                    r["molar"],

                "density":
                    r["density"],

                "source":
                    str(r["source"]).strip(),

                "segments": [],
            }

        materials[name]["segments"].append(seg)

    for m in materials.values():

        m["segments"].sort(
            key=lambda s: s["tmin"]
        )

        m["tmin"] = min(
            s["tmin"] for s in m["segments"]
        )

        m["tmax"] = max(
            s["tmax"] for s in m["segments"]
        )

    return materials


def load_materials(
    path: Path = DATA_FILE
) -> dict:

    df = pd.read_csv(path)

    if len(df.columns) != len(COLS):

        raise ValueError(
            f"Expected {len(COLS)} columns in materials.csv, "
            f"found {len(df.columns)}."
        )

    df.columns = COLS

    for c in NUMERIC:

        df[c] = pd.to_numeric(
            df[c],
            errors="coerce"
        )

    return build_materials(df)


def cp_poly(seg: dict, T):

    T = np.asarray(T, dtype=float)

    return (
        seg["a0"]
        + seg["a1"] * T
        + seg["a2"] * T**2
        + seg["a3"] * T**3
    )


def cp_value(
    material: dict,
    T: float
) -> float:

    for seg in material["segments"]:

        if seg["tmin"] <= T <= seg["tmax"]:

            v = float(
                cp_poly(seg, T)
            )

            return (
                v
                if (
                    np.isfinite(v)
                    and CP_LO < v < CP_HI
                )
                else np.nan
            )

    return np.nan


def material_curve(
    material: dict,
    t_lo: float,
    t_hi: float,
    n: int = 400
):

    span = max(
        t_hi - t_lo,
        1e-9
    )

    xs = []
    ys = []

    for seg in material["segments"]:

        lo = max(
            seg["tmin"],
            t_lo
        )

        hi = min(
            seg["tmax"],
            t_hi
        )

        if hi <= lo:
            continue

        pts = max(
            2,
            int(
                round(
                    n * (hi - lo) / span
                )
            )
        )

        T = np.linspace(
            lo,
            hi,
            pts
        )

        C = cp_poly(
            seg,
            T
        )

        C = np.where(
            np.isfinite(C)
            & (C > CP_LO)
            & (C < CP_HI),
            C,
            np.nan
        )

        xs.append(T)
        ys.append(C)

        # Break between phase segments
        xs.append(np.array([np.nan]))
        ys.append(np.array([np.nan]))

    if not xs:

        return (
            np.array([]),
            np.array([])
        )

    return (
        np.concatenate(xs),
        np.concatenate(ys)
    )


def coverage_gap(
    material: dict,
    t_lo: float,
    t_hi: float
) -> bool:

    return (
        t_lo < material["tmin"] - 1e-9
        or
        t_hi > material["tmax"] + 1e-9
    )


def rank_materials(
    materials: dict,
    T: float
) -> pd.DataFrame:

    rows = []

    for m in materials.values():

        v = cp_value(
            m,
            T
        )

        if np.isfinite(v):

            rows.append({

                "Material":
                    m["name"],

                "Formula":
                    m["formula"],

                "Category":
                    m["category"],

                "Cp (J/kg·K)":
                    round(v, 1),
            })

    out = pd.DataFrame(rows)

    if not out.empty:

        out = (
            out
            .sort_values(
                "Cp (J/kg·K)",
                ascending=False
            )
            .reset_index(drop=True)
        )

        out.index += 1

    return out


# ============================================================
# PLOTLY STYLE
# ============================================================

def styled_figure(
    fig: go.Figure,
    height: int = 520
) -> go.Figure:

    fig.update_layout(

        template="plotly_white",

        height=height,

        margin=dict(
            l=70,
            r=35,
            t=30,
            b=65
        ),

        font=dict(
            family="-apple-system, BlinkMacSystemFont, Inter, Segoe UI, sans-serif",
            size=13,
            color="#1d1d1f"
        ),

        hovermode="closest",

        legend=dict(

            orientation="v",

            yanchor="top",
            y=1,

            xanchor="left",
            x=1.02,

            bgcolor="rgba(255,255,255,0.95)",

            bordercolor="#d2d2d7",

            borderwidth=1,

            font=dict(
                size=12,
                color="#1d1d1f"
            ),
        ),

        plot_bgcolor="#ffffff",

        paper_bgcolor="#ffffff",
    )

    fig.update_xaxes(

        showgrid=True,

        gridcolor="#eeeeef",

        zeroline=False,

        linecolor="#d2d2d7",

        ticks="outside",

        tickcolor="#a1a1a6",

        tickfont=dict(
            color="#6e6e73",
            size=12
        ),

        title_font=dict(
            color="#1d1d1f",
            size=13
        ),
    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor="#eeeeef",

        zeroline=False,

        linecolor="#d2d2d7",

        ticks="outside",

        tickcolor="#a1a1a6",

        tickfont=dict(
            color="#6e6e73",
            size=12
        ),

        title_font=dict(
            color="#1d1d1f",
            size=13
        ),
    )

    return fig


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    st.set_page_config(

        page_title="Specific Heat Explorer",

        page_icon="◦",

        layout="wide",

        initial_sidebar_state="expanded",
    )

    st.markdown(
        CUSTOM_CSS,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    try:

        materials = load_materials()

    except Exception as exc:

        st.error(
            f"Could not load materials.csv — {exc}"
        )

        st.stop()

    names_all = sorted(
        materials.keys()
    )

    cats_all = sorted(
        {
            m["category"]
            for m in materials.values()
        }
    )

    g_lo = min(
        m["tmin"]
        for m in materials.values()
    )

    g_hi = max(
        m["tmax"]
        for m in materials.values()
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(

        '<div class="app-header">'

        '<div>'

        '<div class="app-title">'
        'Specific Heat Explorer'
        '</div>'

        '<div class="app-sub">'
        'Interactive C<sub>p</sub>–T database for engineering materials'
        '</div>'

        '</div>'

        '<div class="header-meta">'

        f'<strong>{len(materials)} materials</strong><br>'

        f'{len(cats_all)} material classes · '
        'J kg⁻¹ K⁻¹'

        '</div>'

        '</div>',

        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    with st.sidebar:

        st.subheader("Materials")

        query = st.text_input(

            "Search",

            placeholder="Search material or formula..."
        ).strip().lower()

        cats = st.multiselect(

            "Material classes",

            cats_all,

            default=cats_all
        )

        def visible(name):

            m = materials[name]

            if m["category"] not in cats:

                return False

            if query:

                if (
                    query not in name.lower()
                    and
                    query not in
                    m["formula"].lower()
                ):

                    return False

            return True

        options = [
            n
            for n in names_all
            if visible(n)
        ]

        st.caption(
            f"{len(options)} of "
            f"{len(names_all)} materials"
        )

        defaults = [

            n for n in [

                "Aluminium",

                "Copper",

                "Alumina (Al₂O₃)",

                "Polyethylene HDPE — solid"

            ]

            if n in options
        ]

        chosen = st.multiselect(

            "Selected materials",

            options,

            default=defaults or options[:3],

            help="Select one or more materials to compare."
        )

        st.divider()

        st.subheader("Temperature")

        t_lo, t_hi = st.slider(

            "Range (K)",

            min_value=int(
                np.floor(g_lo)
            ),

            max_value=int(
                np.ceil(g_hi)
            ),

            value=(

                int(
                    np.floor(g_lo)
                ),

                1500
                if g_hi > 1500
                else int(
                    np.ceil(g_hi)
                )
            ),

            step=10
        )

        if t_hi <= t_lo:

            t_hi = min(
                t_lo + 10,
                int(np.ceil(g_hi))
            )

            t_lo = t_hi - 10

        st.caption(
            "Curves are shown only within "
            "their validated ranges."
        )

    # --------------------------------------------------------
    # EMPTY STATE
    # --------------------------------------------------------

    if not chosen:

        st.markdown(

            '<div class="chart-shell" '
            'style="text-align:center;'
            'padding:4.5rem 1.5rem;">'

            '<div class="chart-title">'
            'Select a material'
            '</div>'

            '<div class="chart-subtitle">'
            'Choose one or more materials to explore '
            'how specific heat changes with temperature.'
            '</div>'

            '</div>',

            unsafe_allow_html=True
        )

        st.stop()

    # --------------------------------------------------------
    # VALIDATION WARNING
    # --------------------------------------------------------

    flagged = [

        (
            materials[n]["name"],
            materials[n]["tmin"],
            materials[n]["tmax"]
        )

        for n in chosen

        if coverage_gap(
            materials[n],
            t_lo,
            t_hi
        )
    ]

    if flagged:

        msg = "<br>".join(

            f"• <strong>{nm}</strong> — "
            f"validated range {lo:.0f}–{hi:.0f} K"

            for nm, lo, hi in flagged
        )

        st.markdown(

            '<div class="range-note">'

            '<strong>Outside validated range</strong><br>'

            f'{msg}'

            '</div>',

            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # MAIN CHART
    # --------------------------------------------------------

    fig = go.Figure()

    for i, n in enumerate(chosen):

        m = materials[n]

        T, C = material_curve(
            m,
            t_lo,
            t_hi
        )

        if T.size == 0:
            continue

        color = PALETTE[
            i % len(PALETTE)
        ]

        fig.add_trace(

            go.Scatter(

                x=T,

                y=C,

                mode="lines",

                name=n,

                line=dict(

                    color=color,

                    width=2.7
                ),

                connectgaps=False,

                hovertemplate=(

                    f"<b>{n}</b><br>"

                    "T = %{x:.0f} K<br>"

                    "Cp = %{y:.1f} J/kg·K"

                    "<extra></extra>"
                )
            )
        )

    fig.update_layout(

        xaxis_title=
        "Temperature, T (K)",

        yaxis_title=
        "Specific heat, Cp (J kg⁻¹ K⁻¹)"
    )

    # Chart header
    st.markdown(

        '<div class="chart-shell">'

        '<div class="chart-title">'
        'Cp vs Temperature'
        '</div>'

        '<div class="chart-subtitle">'
        'Specific heat capacity at constant pressure'
        '</div>'

        '<div class="context-row">'

        f'<span class="context-pill">'
        f'{len(chosen)} materials'
        '</span>'

        f'<span class="context-pill">'
        f'{t_lo:.0f}–{t_hi:.0f} K'
        '</span>'

        '<span class="context-pill">'
        'J kg⁻¹ K⁻¹'
        '</span>'

        '</div>'

        '</div>',

        unsafe_allow_html=True
    )

    st.plotly_chart(

        styled_figure(fig),

        use_container_width=True,

        config={

            "displaylogo": False,

            "toImageButtonOptions": {

                "filename": "Cp_vs_T",

                "scale": 2
            }
        }
    )

    st.caption(
        "Drag to zoom · double-click to reset · "
        "use the camera icon to export the graph."
    )

    # --------------------------------------------------------
    # ANALYSIS NAVIGATION
    # --------------------------------------------------------

    tab_cmp, tab_info, tab_rank, tab_data = st.tabs(

        [
            "Compare",
            "Materials",
            "Rankings",
            "Data"
        ]
    )

    # ========================================================
    # COMPARE
    # ========================================================

    with tab_cmp:

        st.markdown(
            "### Compare materials"
        )

        st.caption(
            "Specific heat at a selected temperature."
        )

        Tc = st.slider(

            "Comparison temperature (K)",

            t_lo,

            t_hi,

            value=min(
                max(298, t_lo),
                t_hi
            ),

            step=5,

            key="cmpT"
        )

        rows = []

        missing = []

        for n in chosen:

            v = cp_value(
                materials[n],
                Tc
            )

            if np.isfinite(v):

                rows.append(
                    (n, v)
                )

            else:

                missing.append(n)

        if rows:

            rows.sort(
                key=lambda x: x[1],
                reverse=True
            )

            labels = [
                r[0]
                for r in rows
            ]

            vals = [
                r[1]
                for r in rows
            ]

            bar = go.Figure(

                go.Bar(

                    x=vals,

                    y=labels,

                    orientation="h",

                    marker_color=ACCENT,

                    text=[
                        f"{v:.0f}"
                        for v in vals
                    ],

                    textposition="outside",

                    hovertemplate=(

                        "<b>%{y}</b><br>"

                        "Cp = %{x:.1f} J/kg·K"

                        "<extra></extra>"
                    )
                )
            )

            bar.update_layout(

                xaxis_title=(
                    f"Specific heat at "
                    f"{Tc:.0f} K "
                    f"(J kg⁻¹ K⁻¹)"
                ),

                yaxis=dict(
                    autorange="reversed"
                )
            )

            st.plotly_chart(

                styled_figure(
                    bar,
                    height=max(
                        260,
                        60 * len(rows)
                    )
                ),

                use_container_width=True,

                config={
                    "displaylogo": False
                }
            )

        else:

            st.info(
                "None of the selected materials "
                "are valid at this temperature."
            )

        if missing:

            st.caption(

                f"Not valid at {Tc:.0f} K: "
                + ", ".join(missing)
            )

    # ========================================================
    # MATERIAL DETAILS
    # ========================================================

    with tab_info:

        st.markdown(
            "### Material information"
        )

        st.caption(
            "Properties and provenance for the selected materials."
        )

        recs = []

        for n in chosen:

            m = materials[n]

            recs.append({

                "Material":
                    m["name"],

                "Formula":
                    m["formula"],

                "Category":
                    m["category"],

                "Valid T range (K)":
                    f"{m['tmin']:.0f} – "
                    f"{m['tmax']:.0f}",

                "Cp @298 K (J/kg·K)":
                    (
                        None
                        if not np.isfinite(
                            m["cp298"]
                        )
                        else round(
                            m["cp298"],
                            1
                        )
                    ),

                "Molar mass (g/mol)":
                    (
                        None
                        if not np.isfinite(
                            m["molar"]
                        )
                        else round(
                            m["molar"],
                            3
                        )
                    ),

                "Density (kg/m³)":
                    (
                        None
                        if not np.isfinite(
                            m["density"]
                        )
                        else round(
                            m["density"],
                            0
                        )
                    ),

                "Phase / notes":
                    m["segments"][0]["notes"],

                "Data source":
                    m["source"],
            })

        st.dataframe(

            pd.DataFrame(recs),

            use_container_width=True,

            hide_index=True
        )

        st.caption(
            "Values are traceable to the thermodynamic "
            "source stored with each material."
        )

    # ========================================================
    # RANKINGS
    # ========================================================

    with tab_rank:

        st.markdown(
            "### Material ranking"
        )

        st.caption(
            "Rank the full database by specific heat at a selected temperature."
        )

        c1, c2 = st.columns(
            [1, 1]
        )

        with c1:

            Tr = st.slider(

                "Temperature (K)",

                int(g_lo),

                int(g_hi),

                value=298,

                step=5,

                key="rankT"
            )

        with c2:

            topn = st.number_input(

                "Materials to show",

                5,

                50,

                15,

                step=5
            )

        rk = rank_materials(
            materials,
            Tr
        )

        if rk.empty:

            st.info(
                "No materials are valid "
                "at this temperature."
            )

        else:

            order = st.radio(

                "Sort",

                [
                    "Highest Cp",
                    "Lowest Cp"
                ],

                horizontal=True,

                key="rankorder"
            )

            if order == "Highest Cp":

                view = rk.head(
                    int(topn)
                )

            else:

                view = rk.tail(
                    int(topn)
                )

            fig_r = go.Figure(

                go.Bar(

                    x=view[
                        "Cp (J/kg·K)"
                    ],

                    y=view[
                        "Material"
                    ],

                    orientation="h",

                    marker_color=ACCENT,

                    hovertemplate=(

                        "<b>%{y}</b><br>"

                        "Cp = %{x:.1f} J/kg·K"

                        "<extra></extra>"
                    )
                )
            )

            fig_r.update_layout(

                xaxis_title=(

                    f"Specific heat at "
                    f"{Tr:.0f} K "
                    f"(J kg⁻¹ K⁻¹)"
                ),

                yaxis=dict(
                    autorange="reversed"
                )
            )

            st.plotly_chart(

                styled_figure(

                    fig_r,

                    height=max(
                        320,
                        30 * len(view)
                    )
                ),

                use_container_width=True,

                config={
                    "displaylogo": False
                }
            )

            st.caption(

                f"{len(rk)} materials have "
                f"a valid fit at {Tr:.0f} K."
            )

    # ========================================================
    # DATA EXPORT
    # ========================================================

    with tab_data:

        st.markdown(
            "### Computed data"
        )

        st.caption(
            "Sampled Cp–T values for the current selection."
        )

        frames = []

        for n in chosen:

            T, C = material_curve(

                materials[n],

                t_lo,

                t_hi
            )

            if T.size:

                frames.append(

                    pd.DataFrame({

                        "Material": n,

                        "T (K)": T,

                        "Cp (J/kg·K)": C

                    }).dropna()
                )

        if frames:

            out = pd.concat(
                frames,
                ignore_index=True
            )

            st.dataframe(

                out.head(500),

                use_container_width=True,

                hide_index=True
            )

            st.download_button(

                "Download curve data (CSV)",

                out.to_csv(
                    index=False
                ).encode("utf-8"),

                file_name=
                "cp_vs_T_export.csv",

                mime="text/csv"
            )

            st.caption(

                f"{len(out):,} computed points "
                f"across {len(frames)} materials."
            )

        else:

            st.info(
                "Nothing to export for "
                "the current selection."
            )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.divider()

    st.markdown(

        '<div style="text-align:center;'
        'color:#6e6e73;font-size:0.78rem;'
        'padding-top:0.5rem;">'
        'Specific Heat Explorer · '
        'Thermodynamic data shown within '
        'validated temperature ranges'
        '</div>',

        unsafe_allow_html=True
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
