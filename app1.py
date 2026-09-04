import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Specific Heat Explorer",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path(__file__).parent / "materials.csv"

COLS = [
    "idx", "name", "formula", "category", "cas", "tmin", "tmax",
    "A", "B", "C", "D", "E", "a0", "a1", "a2", "a3", "r2",
    "cp298", "molar", "density", "source", "notes",
]

NUMERIC = [
    "tmin", "tmax",
    "a0", "a1", "a2", "a3",
    "cp298", "molar", "density",
]

PALETTE = [
    "#4F86C6",
    "#55A868",
    "#E5A23C",
    "#8C6BB1",
    "#5FA8C9",
    "#C96A72",
    "#6FAF9B",
    "#A67C52",
]

CP_LO = 0.0
CP_HI = 20000.0
ACCENT = "#5D7892"


# ============================================================
# COMPLETE UI STYLE
# ============================================================

CUSTOM_CSS = """
<style>

/* ==========================================================
   GLOBAL PAGE
   ========================================================== */

html,
body {
    background: #e5e7ea !important;
}

.stApp {
    background: #e5e7ea !important;
    color: #555b63 !important;
}

[data-testid="stAppViewContainer"] {
    background: #e5e7ea !important;
}

[data-testid="stMain"] {
    background: #e5e7ea !important;
}

.block-container {
    max-width: 1320px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
}

header[data-testid="stHeader"] {
    background: rgba(229,231,234,0.88) !important;
    backdrop-filter: blur(20px) saturate(130%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(130%) !important;
    border-bottom: 1px solid rgba(160,165,172,0.25) !important;
}

#MainMenu,
footer {
    visibility: hidden;
}


/* ==========================================================
   FONT
   ========================================================== */

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
        "SF Pro Text",
        "SF Pro Display",
        "Segoe UI",
        sans-serif !important;
}


/* ==========================================================
   HEADINGS
   ========================================================== */

h1 {
    color: #4c5259 !important;
    font-size: 2.15rem !important;
    line-height: 1.12 !important;
    font-weight: 560 !important;
    letter-spacing: -0.045em !important;
    margin-bottom: 0.25rem !important;
}

h2 {
    color: #555b63 !important;
    font-size: 1.38rem !important;
    line-height: 1.25 !important;
    font-weight: 520 !important;
    letter-spacing: -0.025em !important;
}

h3 {
    color: #5d636b !important;
    font-size: 1.08rem !important;
    font-weight: 520 !important;
    letter-spacing: -0.015em !important;
}

p {
    color: #737a83 !important;
    font-size: 0.86rem !important;
    font-weight: 400 !important;
}

[data-testid="stCaptionContainer"] {
    color: #858c94 !important;
    font-size: 0.74rem !important;
    font-weight: 400 !important;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            145deg,
            rgba(239,241,243,0.96),
            rgba(222,225,229,0.94)
        ) !important;

    border-right: 1px solid #c1c6cc !important;

    box-shadow:
        8px 0 25px rgba(0,0,0,0.035) !important;
}

section[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

section[data-testid="stSidebar"] h2 {
    color: #565c64 !important;
    font-size: 1.04rem !important;
    font-weight: 560 !important;
}

section[data-testid="stSidebar"] h3 {
    color: #626971 !important;
    font-size: 0.96rem !important;
    font-weight: 520 !important;
}


/* Sidebar labels */

section[data-testid="stSidebar"]
[data-testid="stMarkdownContainer"] p {

    color: #808790 !important;

    font-size: 0.65rem !important;

    font-weight: 550 !important;

    letter-spacing: 0.075em !important;

    text-transform: uppercase !important;
}


/* ==========================================================
   SEARCH BAR
   ========================================================== */

section[data-testid="stSidebar"]
div[data-testid="stTextInput"] > div > div {

    background:
        rgba(247,248,249,0.58) !important;

    backdrop-filter:
        blur(20px) saturate(130%) !important;

    -webkit-backdrop-filter:
        blur(20px) saturate(130%) !important;

    border:
        1px solid rgba(255,255,255,0.82) !important;

    border-radius:
        12px !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.85),
        0 4px 14px rgba(0,0,0,0.045) !important;
}

section[data-testid="stSidebar"]
div[data-testid="stTextInput"] input {

    background:
        transparent !important;

    border:
        none !important;

    color:
        #5d646c !important;

    font-size:
        0.82rem !important;

    font-weight:
        400 !important;

    min-height:
        40px !important;
}

section[data-testid="stSidebar"]
div[data-testid="stTextInput"] input::placeholder {
    color: #9aa1a9 !important;
}


/* ==========================================================
   MULTISELECT BOX
   ========================================================== */

section[data-testid="stSidebar"]
div[data-testid="stMultiSelect"]
div[data-baseweb="select"] > div {

    background:
        rgba(238,240,242,0.72) !important;

    background-color:
        rgba(238,240,242,0.72) !important;

    border:
        1px solid #bcc2c9 !important;

    border-radius:
        11px !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.85),
        0 3px 12px rgba(0,0,0,0.035) !important;

    min-height:
        42px !important;
}


/* ==========================================================
   MATERIAL CHIPS
   NO RED
   ========================================================== */

section[data-testid="stSidebar"]
div[data-testid="stMultiSelect"]
[data-baseweb="tag"] {

    background:
        rgba(214,218,222,0.82) !important;

    background-color:
        rgba(214,218,222,0.82) !important;

    border:
        1px solid #bec4ca !important;

    border-radius:
        8px !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.65),
        0 1px 4px rgba(0,0,0,0.04) !important;

    color:
        #5c636b !important;

    margin:
        3px 3px 3px 0 !important;
}

section[data-testid="stSidebar"]
div[data-testid="stMultiSelect"]
[data-baseweb="tag"] span {

    color:
        #5c636b !important;

    font-size:
        0.76rem !important;

    font-weight:
        450 !important;
}

section[data-testid="stSidebar"]
div[data-testid="stMultiSelect"]
[data-baseweb="tag"] svg {

    color:
        #7c848d !important;

    width:
        12px !important;

    height:
        12px !important;
}

section[data-testid="stSidebar"]
div[data-testid="stMultiSelect"]
[data-baseweb="tag"]:hover {

    background:
        rgba(245,246,247,0.92) !important;

    border-color:
        #aeb5bd !important;
}


/* ==========================================================
   DROPDOWN
   LIGHT GRAY — FIXES BLACK MENU
   ========================================================== */

div[data-baseweb="popover"] {

    background:
        rgba(232,234,237,0.98) !important;

    background-color:
        #e8eaed !important;

    color:
        #5b626a !important;

    border:
        1px solid #bfc4ca !important;

    border-radius:
        12px !important;

    box-shadow:
        0 18px 42px rgba(0,0,0,0.14) !important;

    backdrop-filter:
        blur(22px) saturate(130%) !important;

    -webkit-backdrop-filter:
        blur(22px) saturate(130%) !important;
}

div[data-baseweb="popover"] * {
    color: #626971 !important;
}

div[data-baseweb="popover"]
div[data-baseweb="menu"] {

    background:
        #e8eaed !important;

    background-color:
        #e8eaed !important;
}

div[data-baseweb="popover"]
[role="option"] {

    background:
        transparent !important;

    color:
        #626971 !important;

    font-size:
        0.80rem !important;

    font-weight:
        400 !important;

    border-radius:
        8px !important;

    margin:
        2px 5px !important;
}

div[data-baseweb="popover"]
[role="option"]:hover {

    background:
        #d9dde2 !important;

    color:
        #4f555c !important;
}

div[data-baseweb="popover"]
[role="option"][aria-selected="true"] {

    background:
        #d4d9de !important;

    color:
        #50575f !important;
}


/* Dropdown search */

div[data-baseweb="popover"] input {

    background:
        #f0f1f3 !important;

    color:
        #555c64 !important;

    border:
        1px solid #c5cad0 !important;

    border-radius:
        8px !important;
}


/* ==========================================================
   SLIDER
   ========================================================== */

section[data-testid="stSidebar"]
[data-testid="stSlider"] [role="slider"] {

    background:
        #6f8295 !important;

    border-color:
        #6f8295 !important;

    box-shadow:
        0 1px 4px rgba(70,90,110,0.20) !important;
}


/* ==========================================================
   METRIC CARDS
   ========================================================== */

div[data-testid="stMetric"] {

    background:
        rgba(239,241,243,0.72) !important;

    border:
        1px solid #d0d4d9 !important;

    border-radius:
        13px !important;

    padding:
        10px 14px !important;

    box-shadow:
        0 2px 8px rgba(0,0,0,0.025) !important;
}

div[data-testid="stMetricLabel"] {

    color:
        #858b93 !important;

    font-size:
        0.70rem !important;

    font-weight:
        450 !important;
}

div[data-testid="stMetricValue"] {

    color:
        #626971 !important;

    font-size:
        1.35rem !important;

    font-weight:
        500 !important;
}


/* ==========================================================
   RANGE WARNING
   ========================================================== */

.range-note {

    background:
        #ecebe4 !important;

    border:
        1px solid #d1cdbd !important;

    color:
        #716d60 !important;

    border-radius:
        11px !important;

    padding:
        10px 13px !important;

    font-size:
        0.78rem !important;

    line-height:
        1.55 !important;

    margin:
        0.55rem 0 1rem !important;

    box-shadow:
        0 2px 8px rgba(0,0,0,0.025) !important;
}

.range-note strong {
    color: #625e52 !important;
    font-weight: 550 !important;
}


/* ==========================================================
   CHART CARD
   ========================================================== */

.chart-shell {

    background:
        rgba(232,234,237,0.72) !important;

    border:
        1px solid #adb3ba !important;

    border-radius:
        15px !important;

    padding:
        1rem 1.1rem 0.75rem !important;

    box-shadow:
        0 4px 16px rgba(0,0,0,0.035) !important;
}

.chart-title {

    color:
        #555b63 !important;

    font-size:
        1.18rem !important;

    font-weight:
        550 !important;

    letter-spacing:
        -0.02em !important;
}

.chart-subtitle {

    color:
        #858b93 !important;

    font-size:
        0.78rem !important;

    font-weight:
        400 !important;

    margin-top:
        0.15rem !important;
}


/* ==========================================================
   CONTEXT PILLS
   ========================================================== */

.context-row {

    display:
        flex !important;

    gap:
        7px !important;

    flex-wrap:
        wrap !important;

    margin-top:
        0.65rem !important;
}

.context-pill {

    color:
        #707881 !important;

    background:
        rgba(243,244,246,0.78) !important;

    border:
        1px solid #c9cdd2 !important;

    padding:
        4px 9px !important;

    border-radius:
        999px !important;

    font-size:
        0.72rem !important;

    font-weight:
        400 !important;
}


/* ==========================================================
   PLOTLY FRAME
   ========================================================== */

div[data-testid="stPlotlyChart"] {

    background:
        #e2e4e7 !important;

    border:
        1px solid #aeb4bb !important;

    border-radius:
        0 0 15px 15px !important;

    padding:
        5px !important;

    box-shadow:
        0 4px 15px rgba(0,0,0,0.04) !important;
}


/* ==========================================================
   TABS
   ========================================================== */

.stTabs [data-baseweb="tab-list"] {

    gap:
        3px !important;

    border-bottom:
        1px solid #c8cdd2 !important;

    background:
        transparent !important;
}

.stTabs [data-baseweb="tab"] {

    color:
        #7a8189 !important;

    font-size:
        0.82rem !important;

    font-weight:
        450 !important;

    padding:
        0.6rem 0.95rem !important;

    border-radius:
        8px 8px 0 0 !important;
}

.stTabs [aria-selected="true"] {

    color:
        #555c64 !important;

    font-weight:
        550 !important;
}

.stTabs [data-baseweb="tab-highlight"] {

    background:
        #71869a !important;
}


/* ==========================================================
   DATAFRAME
   ========================================================== */

div[data-testid="stDataFrame"] {

    background:
        #e2e4e7 !important;

    border:
        1px solid #b6bcc3 !important;

    border-radius:
        11px !important;

    overflow:
        hidden !important;
}


/* ==========================================================
   BUTTONS
   ========================================================== */

button[kind="primary"],
.stDownloadButton button {

    background:
        #697b8b !important;

    color:
        #ffffff !important;

    border:
        none !important;

    border-radius:
        9px !important;

    font-size:
        0.80rem !important;

    font-weight:
        500 !important;
}

button[kind="primary"]:hover,
.stDownloadButton button:hover {

    background:
        #5d6e7d !important;
}


/* ==========================================================
   DIVIDERS
   ========================================================== */

hr {

    border:
        0 !important;

    border-top:
        1px solid #c9cdd2 !important;

    margin:
        1.25rem 0 !important;
}


/* ==========================================================
   MOBILE
   ========================================================== */

@media (max-width: 800px) {

    .block-container {
        padding-top: 1rem !important;
    }

    h1 {
        font-size: 1.8rem !important;
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

        name = str(
            r["name"]
        ).strip()

        seg = {
            "tmin": r["tmin"],
            "tmax": r["tmax"],
            "a0": r["a0"],
            "a1": r["a1"],
            "a2": r["a2"],
            "a3": r["a3"],
            "notes": str(
                r["notes"]
            ).strip(),
        }

        if not (
            np.isfinite(seg["tmin"])
            and
            np.isfinite(seg["tmax"])
        ):
            continue

        if name not in materials:

            materials[name] = {

                "name":
                    name,

                "formula":
                    str(
                        r["formula"]
                    ).strip(),

                "category":
                    str(
                        r["category"]
                    ).strip(),

                "cas":
                    str(
                        r["cas"]
                    ).strip(),

                "cp298":
                    r["cp298"],

                "molar":
                    r["molar"],

                "density":
                    r["density"],

                "source":
                    str(
                        r["source"]
                    ).strip(),

                "segments":
                    [],
            }

        materials[name]["segments"].append(
            seg
        )

    for m in materials.values():

        m["segments"].sort(
            key=lambda s: s["tmin"]
        )

        m["tmin"] = min(
            s["tmin"]
            for s in m["segments"]
        )

        m["tmax"] = max(
            s["tmax"]
            for s in m["segments"]
        )

    return materials


@st.cache_data
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


def cp_poly(
    seg: dict,
    T
):

    T = np.asarray(
        T,
        dtype=float
    )

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

        if (
            seg["tmin"]
            <= T
            <= seg["tmax"]
        ):

            v = float(
                cp_poly(
                    seg,
                    T
                )
            )

            if (
                np.isfinite(v)
                and CP_LO < v < CP_HI
            ):

                return v

            return np.nan

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
                    n
                    * (hi - lo)
                    / span
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

        xs.append(
            np.array([np.nan])
        )

        ys.append(
            np.array([np.nan])
        )

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
        t_lo
        <
        material["tmin"] - 1e-9
        or
        t_hi
        >
        material["tmax"] + 1e-9
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
                    round(
                        v,
                        1
                    ),
            })

    out = pd.DataFrame(
        rows
    )

    if not out.empty:

        out = (
            out
            .sort_values(
                "Cp (J/kg·K)",
                ascending=False
            )
            .reset_index(
                drop=True
            )
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
            l=72,
            r=35,
            t=28,
            b=65
        ),

        font=dict(

            family=(
                "-apple-system, "
                "BlinkMacSystemFont, "
                "Segoe UI, sans-serif"
            ),

            size=11,

            color="#707780"
        ),

        hovermode="closest",

        plot_bgcolor="#f0f1f3",

        paper_bgcolor="#e2e4e7",

        legend=dict(

            orientation="v",

            yanchor="top",

            y=1,

            xanchor="left",

            x=1.02,

            bgcolor="rgba(238,240,242,0.96)",

            bordercolor="#aeb4bb",

            borderwidth=1,

            font=dict(
                size=10,
                color="#5d646c"
            ),
        ),
    )

    fig.update_xaxes(

        showgrid=True,

        gridcolor="#d9dde1",

        gridwidth=1,

        zeroline=False,

        showline=True,

        mirror=True,

        linecolor="#8e969f",

        linewidth=1.2,

        ticks="outside",

        tickcolor="#8e969f",

        tickfont=dict(
            color="#747c85",
            size=10
        ),

        title_font=dict(
            color="#555d66",
            size=12
        ),
    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor="#d9dde1",

        gridwidth=1,

        zeroline=False,

        showline=True,

        mirror=True,

        linecolor="#8e969f",

        linewidth=1.2,

        ticks="outside",

        tickcolor="#8e969f",

        tickfont=dict(
            color="#747c85",
            size=10
        ),

        title_font=dict(
            color="#555d66",
            size=12
        ),
    )

    return fig


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # APPLY STYLE
    # --------------------------------------------------------

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


    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        """
        <div style="
            color:#7c848d;
            font-size:0.66rem;
            font-weight:550;
            letter-spacing:0.09em;
            text-transform:uppercase;
            margin-bottom:0.35rem;
        ">
            ENGINEERING MATERIALS
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title(
        "Specific Heat Explorer"
    )

    st.markdown(
        """
        <div style="
            color:#737a83;
            font-size:0.90rem;
            font-weight:400;
            margin-bottom:1.2rem;
        ">
            Interactive C<sub>p</sub>–T database for engineering materials
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    c1, c2, c3 = st.columns(
        3
    )

    with c1:

        st.metric(
            "Materials",
            len(materials)
        )

    with c2:

        st.metric(
            "Material classes",
            len(cats_all)
        )

    with c3:

        st.metric(
            "Specific heat unit",
            "J kg⁻¹ K⁻¹"
        )


    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        st.subheader(
            "Materials"
        )

        st.caption(
            "SEARCH"
        )

        query = st.text_input(

            "Search",

            placeholder=(
                "Search material or formula..."
            )
        ).strip().lower()


        st.caption(
            "MATERIAL CLASS"
        )

        cats = st.multiselect(

            "Material classes",

            cats_all,

            default=cats_all,

            label_visibility="collapsed"
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

            n

            for n in [

                "Aluminium",

                "Copper",

                "Alumina (Al₂O₃)",

                "Polyethylene HDPE — solid"

            ]

            if n in options
        ]


        st.caption(
            "SELECTED MATERIALS"
        )


        chosen = st.multiselect(

            "Selected materials",

            options,

            default=(
                defaults
                if defaults
                else options[:3]
            ),

            help=(
                "Select one or more materials "
                "to compare."
            ),

            label_visibility="collapsed"
        )


        st.divider()


        st.subheader(
            "Temperature"
        )


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

            step=10,

            label_visibility="collapsed"
        )


        if t_hi <= t_lo:

            t_hi = min(
                t_lo + 10,
                int(
                    np.ceil(g_hi)
                )
            )

            t_lo = t_hi - 10


        st.caption(
            "Curves are shown only within "
            "their validated ranges."
        )


    # ========================================================
    # EMPTY STATE
    # ========================================================

    if not chosen:

        st.markdown(

            """
            <div class="chart-shell"
                 style="
                 text-align:center;
                 padding:4rem 1.5rem;
                 ">

                <div class="chart-title">
                    Select a material
                </div>

                <div class="chart-subtitle">
                    Choose one or more materials to explore
                    how specific heat changes with temperature.
                </div>

            </div>
            """,

            unsafe_allow_html=True
        )

        st.stop()


    # ========================================================
    # VALIDATION WARNING
    # ========================================================

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
            f"validated range "
            f"{lo:.0f}–{hi:.0f} K"

            for nm, lo, hi in flagged
        )


        st.markdown(

            '<div class="range-note">'

            '<strong>Outside validated range</strong>'
            '<br>'

            f'{msg}'

            '</div>',

            unsafe_allow_html=True
        )


    # ========================================================
    # CHART HEADER
    # ========================================================

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


    # ========================================================
    # MAIN GRAPH
    # ========================================================

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

                    width=2.6
                ),

                connectgaps=False,

                hovertemplate=(

                    f"<b>{n}</b><br>"

                    "Temperature = %{x:.0f} K<br>"

                    "Cp = %{y:.1f} J kg⁻¹ K⁻¹"

                    "<extra></extra>"
                )
            )
        )


    fig.update_layout(

        xaxis_title=(
            "Temperature, T (K)"
        ),

        yaxis_title=(
            "Specific heat, Cp "
            "(J kg⁻¹ K⁻¹)"
        )
    )


    st.plotly_chart(

        styled_figure(
            fig,
            height=530
        ),

        use_container_width=True,

        config={

            "displaylogo":
                False,

            "toImageButtonOptions": {

                "filename":
                    "Cp_vs_T",

                "scale":
                    2
            }
        }
    )


    st.caption(

        "Drag to zoom · double-click to reset · "
        "use the camera icon to export the graph."
    )


    # ========================================================
    # TABS
    # ========================================================

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
                max(
                    298,
                    t_lo
                ),
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

                    marker_color="#71869A",

                    text=[

                        f"{v:.0f}"

                        for v in vals
                    ],

                    textposition="outside",

                    hovertemplate=(

                        "<b>%{y}</b><br>"

                        "Cp = %{x:.1f} J kg⁻¹ K⁻¹"

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
                    "displaylogo":
                        False
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
    # MATERIAL INFORMATION
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
                    (
                        f"{m['tmin']:.0f} – "
                        f"{m['tmax']:.0f}"
                    ),

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
            "Rank the full database by specific heat "
            "at a selected temperature."
        )


        c1, c2 = st.columns(
            [1, 1]
        )


        with c1:

            Tr = st.slider(

                "Temperature (K)",

                int(g_lo),

                int(g_hi),

                value=min(
                    298,
                    int(g_hi)
                ),

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

                    marker_color="#71869A",

                    hovertemplate=(

                        "<b>%{y}</b><br>"

                        "Cp = %{x:.1f} J kg⁻¹ K⁻¹"

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
                    "displaylogo":
                        False
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

                        "Material":
                            n,

                        "T (K)":
                            T,

                        "Cp (J/kg·K)":
                            C

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

                mime=
                    "text/csv"
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


    # ========================================================
    # FOOTER
    # ========================================================

    st.divider()


    st.markdown(

        """
        <div style="
            text-align:center;
            color:#858b93;
            font-size:0.70rem;
            font-weight:400;
            padding-top:0.4rem;
        ">
            Specific Heat Explorer ·
            Thermodynamic data shown within
            validated temperature ranges
        </div>
        """,

        unsafe_allow_html=True
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
