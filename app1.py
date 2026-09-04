import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Specific Heat Explorer",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SETTINGS
# ============================================================

DATA_FILE = Path(__file__).parent / "materials.csv"

COLS = [
    "idx",
    "name",
    "formula",
    "category",
    "cas",
    "tmin",
    "tmax",
    "A",
    "B",
    "C",
    "D",
    "E",
    "a0",
    "a1",
    "a2",
    "a3",
    "r2",
    "cp298",
    "molar",
    "density",
    "source",
    "notes",
]

NUMERIC = [
    "tmin",
    "tmax",
    "A",
    "B",
    "C",
    "D",
    "E",
    "a0",
    "a1",
    "a2",
    "a3",
    "r2",
    "cp298",
    "molar",
    "density",
]

PALETTE = [
    "#0071E3",
    "#34C759",
    "#FF9F0A",
    "#AF52DE",
    "#5AC8FA",
    "#FF375F",
    "#64D2FF",
    "#FF6B35",
]

CP_LO = 0
CP_HI = 20000


# ============================================================
# PYTHON EMBEDDED STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GENERAL
    ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 0%,
                rgba(255,255,255,0.95),
                transparent 32%
            ),
            #f3f4f6 !important;
        color: #2b2d31 !important;
    }

    [data-testid="stAppViewContainer"] {
        background: #f3f4f6 !important;
    }

    [data-testid="stMain"] {
        background: #f3f4f6 !important;
    }

    .block-container {
        max-width: 1320px !important;
        padding-top: 1.4rem !important;
        padding-bottom: 3rem !important;
    }

    header[data-testid="stHeader"] {
        background: rgba(243,244,246,0.78) !important;
        backdrop-filter: blur(20px) saturate(140%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(140%) !important;
    }


    /* ======================================================
       TYPOGRAPHY
       ====================================================== */

    h1 {
        color: #24262a !important;
        font-size: 2.15rem !important;
        line-height: 1.15 !important;
        font-weight: 600 !important;
        letter-spacing: -0.045em !important;
        margin-bottom: 0.3rem !important;
    }

    h2 {
        color: #2b2d31 !important;
        font-size: 1.38rem !important;
        font-weight: 550 !important;
        letter-spacing: -0.025em !important;
    }

    h3 {
        color: #34373c !important;
        font-size: 1.08rem !important;
        font-weight: 550 !important;
    }

    p {
        color: #727983 !important;
        font-size: 0.86rem !important;
        font-weight: 400 !important;
    }

    [data-testid="stCaptionContainer"] {
        color: #858b95 !important;
        font-size: 0.74rem !important;
        font-weight: 400 !important;
    }


    /* ======================================================
       SIDEBAR
       macOS glass appearance
       ====================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.90),
                rgba(246,247,249,0.78)
            ) !important;

        border-right: 1px solid rgba(190,195,202,0.65) !important;

        box-shadow:
            8px 0 30px rgba(0,0,0,0.035) !important;
    }

    section[data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] h2 {
        font-size: 1.02rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.015em !important;
    }


    /* ======================================================
       SIDEBAR LABELS
       ====================================================== */

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"]
    p {
        color: #8a9099 !important;
        font-size: 0.66rem !important;
        font-weight: 550 !important;
        letter-spacing: 0.085em !important;
        text-transform: uppercase !important;
    }


    /* ======================================================
       SEARCH BOX
       ====================================================== */

    section[data-testid="stSidebar"]
    div[data-testid="stTextInput"] > div > div {

        background:
            rgba(255,255,255,0.48) !important;

        backdrop-filter:
            blur(20px) saturate(155%) !important;

        -webkit-backdrop-filter:
            blur(20px) saturate(155%) !important;

        border:
            1px solid rgba(255,255,255,0.90) !important;

        border-radius:
            12px !important;

        box-shadow:
            0 5px 18px rgba(0,0,0,0.045),
            inset 0 1px 0 rgba(255,255,255,0.9) !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stTextInput"] input {

        background: transparent !important;

        border: none !important;

        color: #4e555e !important;

        font-size: 0.82rem !important;

        font-weight: 400 !important;

        min-height: 40px !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stTextInput"] input::placeholder {

        color: #a0a6ae !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stTextInput"] > div > div:focus-within {

        border-color:
            rgba(0,113,227,0.28) !important;

        box-shadow:
            0 5px 18px rgba(0,0,0,0.05),
            0 0 0 3px rgba(0,113,227,0.07) !important;
    }


    /* ======================================================
       ALL MULTISELECT BOXES
       ====================================================== */

    section[data-testid="stSidebar"]
    div[data-testid="stMultiSelect"]
    div[data-baseweb="select"] > div {

        background:
            rgba(255,255,255,0.46) !important;

        backdrop-filter:
            blur(20px) saturate(155%) !important;

        -webkit-backdrop-filter:
            blur(20px) saturate(155%) !important;

        border:
            1px solid rgba(255,255,255,0.88) !important;

        border-radius:
            12px !important;

        box-shadow:
            0 6px 20px rgba(0,0,0,0.045),
            inset 0 1px 0 rgba(255,255,255,0.9) !important;

        min-height:
            42px !important;
    }


    /* ======================================================
       REMOVE RED STREAMLIT TAGS
       ====================================================== */

    section[data-testid="stSidebar"]
    div[data-testid="stMultiSelect"]
    [data-baseweb="tag"] {

        background:
            rgba(255,255,255,0.72) !important;

        background-color:
            rgba(255,255,255,0.72) !important;

        border:
            1px solid rgba(185,192,201,0.58) !important;

        border-radius:
            8px !important;

        box-shadow:
            0 2px 8px rgba(0,0,0,0.045) !important;

        color:
            #59616b !important;

        margin:
            3px 3px 3px 0 !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stMultiSelect"]
    [data-baseweb="tag"] span {

        color:
            #59616b !important;

        font-size:
            0.76rem !important;

        font-weight:
            450 !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stMultiSelect"]
    [data-baseweb="tag"] svg {

        color:
            #7d8791 !important;

        width:
            12px !important;

        height:
            12px !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stMultiSelect"]
    [data-baseweb="tag"]:hover {

        background:
            rgba(255,255,255,0.92) !important;

        border-color:
            rgba(155,163,173,0.62) !important;
    }


    /* ======================================================
       DROPDOWN
       ====================================================== */

    div[data-baseweb="popover"] {

        background:
            rgba(255,255,255,0.82) !important;

        backdrop-filter:
            blur(25px) saturate(160%) !important;

        -webkit-backdrop-filter:
            blur(25px) saturate(160%) !important;

        border:
            1px solid rgba(210,214,220,0.8) !important;

        border-radius:
            13px !important;

        box-shadow:
            0 18px 45px rgba(0,0,0,0.13) !important;
    }

    div[data-baseweb="menu"] {
        background: transparent !important;
    }

    div[role="option"] {

        color:
            #4b525b !important;

        font-size:
            0.80rem !important;

        border-radius:
            8px !important;

        margin:
            2px 5px !important;
    }

    div[role="option"]:hover {

        background:
            rgba(0,113,227,0.07) !important;
    }

    div[role="option"][aria-selected="true"] {

        background:
            rgba(0,113,227,0.09) !important;

        color:
            #075ca8 !important;
    }


    /* ======================================================
       SLIDER
       ====================================================== */

    section[data-testid="stSidebar"]
    [data-testid="stSlider"] [role="slider"] {

        background:
            #0071e3 !important;

        border-color:
            #0071e3 !important;

        box-shadow:
            0 1px 4px rgba(0,113,227,0.25) !important;
    }


    /* ======================================================
       STATISTICS
       ====================================================== */

    div[data-testid="stMetric"] {

        background:
            rgba(255,255,255,0.38) !important;

        border:
            1px solid rgba(220,223,228,0.75) !important;

        border-radius:
            12px !important;

        padding:
            10px 14px !important;
    }

    div[data-testid="stMetricLabel"] {

        color:
            #858b94 !important;

        font-size:
            0.70rem !important;

        font-weight:
            450 !important;
    }

    div[data-testid="stMetricValue"] {

        color:
            #4e555e !important;

        font-size:
            1.35rem !important;

        font-weight:
            500 !important;
    }


    /* ======================================================
       WARNING
       ====================================================== */

    div[data-testid="stAlert"] {

        background:
            rgba(255,249,232,0.80) !important;

        border:
            1px solid rgba(224,204,153,0.72) !important;

        border-radius:
            11px !important;

        color:
            #786842 !important;

        padding:
            0.65rem 0.85rem !important;

        box-shadow:
            0 3px 12px rgba(0,0,0,0.025) !important;
    }

    div[data-testid="stAlert"] p {

        color:
            #786842 !important;

        font-size:
            0.76rem !important;

        font-weight:
            400 !important;
    }


    /* ======================================================
       CHART CONTAINER
       ====================================================== */

    div[data-testid="stPlotlyChart"] {

        background:
            #ffffff !important;

        border:
            1px solid #c8ccd2 !important;

        border-radius:
            0 0 15px 15px !important;

        padding:
            4px !important;

        box-shadow:
            0 4px 16px rgba(0,0,0,0.035) !important;
    }


    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {

        color:
            #7a8089 !important;

        font-size:
            0.82rem !important;

        font-weight:
            450 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {

        color:
            #33363b !important;

        font-weight:
            550 !important;
    }

    div[data-baseweb="tab-highlight"] {

        background:
            #0071e3 !important;
    }


    /* ======================================================
       TABLE
       ====================================================== */

    [data-testid="stDataFrame"] {

        border:
            1px solid #cbd0d6 !important;

        border-radius:
            11px !important;

        overflow:
            hidden !important;
    }


    /* ======================================================
       DOWNLOAD BUTTON
       ====================================================== */

    .stDownloadButton button {

        background:
            #0071e3 !important;

        color:
            white !important;

        border:
            none !important;

        border-radius:
            9px !important;

        font-size:
            0.80rem !important;

        font-weight:
            500 !important;
    }

    .stDownloadButton button:hover {

        background:
            #0067cf !important;
    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {

        border-top:
            1px solid #dfe1e5 !important;
    }


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 800px) {

        h1 {
            font-size: 1.85rem !important;
        }

        .block-container {
            padding-top: 1rem !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA
# ============================================================

def build_materials(df):

    materials = {}

    for _, r in df.iterrows():

        name = str(r["name"]).strip()

        segment = {
            "tmin": r["tmin"],
            "tmax": r["tmax"],
            "a0": r["a0"],
            "a1": r["a1"],
            "a2": r["a2"],
            "a3": r["a3"],
            "notes": str(r["notes"]).strip(),
        }

        if not (
            np.isfinite(segment["tmin"])
            and np.isfinite(segment["tmax"])
        ):
            continue

        if name not in materials:

            materials[name] = {
                "name": name,
                "formula": str(r["formula"]).strip(),
                "category": str(r["category"]).strip(),
                "cas": str(r["cas"]).strip(),
                "cp298": r["cp298"],
                "molar": r["molar"],
                "density": r["density"],
                "source": str(r["source"]).strip(),
                "segments": [],
            }

        materials[name]["segments"].append(
            segment
        )

    for material in materials.values():

        material["segments"].sort(
            key=lambda x: x["tmin"]
        )

        material["tmin"] = min(
            x["tmin"]
            for x in material["segments"]
        )

        material["tmax"] = max(
            x["tmax"]
            for x in material["segments"]
        )

    return materials


@st.cache_data
def load_materials():

    df = pd.read_csv(DATA_FILE)

    if len(df.columns) != len(COLS):

        raise ValueError(
            f"Expected {len(COLS)} columns in materials.csv, "
            f"found {len(df.columns)}."
        )

    df.columns = COLS

    for column in NUMERIC:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return build_materials(df)


# ============================================================
# CALCULATIONS
# ============================================================

def cp_poly(segment, T):

    T = np.asarray(
        T,
        dtype=float
    )

    return (
        segment["a0"]
        + segment["a1"] * T
        + segment["a2"] * T**2
        + segment["a3"] * T**3
    )


def cp_value(material, T):

    for segment in material["segments"]:

        if (
            segment["tmin"]
            <= T
            <= segment["tmax"]
        ):

            value = float(
                cp_poly(
                    segment,
                    T
                )
            )

            if (
                np.isfinite(value)
                and CP_LO < value < CP_HI
            ):

                return value

    return np.nan


def material_curve(
    material,
    t_lo,
    t_hi,
    n=400
):

    span = max(
        t_hi - t_lo,
        1e-9
    )

    xs = []
    ys = []

    for segment in material["segments"]:

        lo = max(
            segment["tmin"],
            t_lo
        )

        hi = min(
            segment["tmax"],
            t_hi
        )

        if hi <= lo:
            continue

        points = max(
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
            points
        )

        C = cp_poly(
            segment,
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
    material,
    t_lo,
    t_hi
):

    return (
        t_lo < material["tmin"]
        or
        t_hi > material["tmax"]
    )


def rank_materials(
    materials,
    temperature
):

    rows = []

    for material in materials.values():

        value = cp_value(
            material,
            temperature
        )

        if np.isfinite(value):

            rows.append({

                "Material":
                    material["name"],

                "Formula":
                    material["formula"],

                "Category":
                    material["category"],

                "Cp (J/kg·K)":
                    round(
                        value,
                        1
                    )
            })

    result = pd.DataFrame(rows)

    if not result.empty:

        result = (
            result
            .sort_values(
                "Cp (J/kg·K)",
                ascending=False
            )
            .reset_index(drop=True)
        )

        result.index += 1

    return result


# ============================================================
# LOAD
# ============================================================

try:

    materials = load_materials()

except Exception as error:

    st.error(
        f"Could not load materials.csv — {error}"
    )

    st.stop()


names_all = sorted(
    materials.keys()
)

categories_all = sorted(
    {
        m["category"]
        for m in materials.values()
    }
)

global_min = min(
    m["tmin"]
    for m in materials.values()
)

global_max = max(
    m["tmax"]
    for m in materials.values()
)


# ============================================================
# HEADER
# ============================================================

st.caption(
    "ENGINEERING MATERIALS"
)

st.title(
    "Specific Heat Explorer"
)

st.markdown(
    "Interactive Cp–T database for engineering materials."
)


# ============================================================
# STATS
# ============================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Materials",
        len(materials)
    )

with c2:

    st.metric(
        "Material classes",
        len(categories_all)
    )

with c3:

    st.metric(
        "Specific heat unit",
        "J kg⁻¹ K⁻¹"
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "Materials"
    )

    st.caption(
        "SEARCH"
    )

    search = st.text_input(
        "Search materials",
        placeholder="Search material or formula...",
        label_visibility="collapsed"
    ).strip().lower()

    filtered_names = []

    for name in names_all:

        material = materials[name]

        if search:

            if (
                search not in name.lower()
                and
                search not in material["formula"].lower()
            ):
                continue

        filtered_names.append(
            name
        )

    st.caption(
        "MATERIAL CLASS"
    )

    selected_categories = st.multiselect(

        "Material classes",

        categories_all,

        default=categories_all,

        label_visibility="collapsed"
    )

    filtered_names = [

        name

        for name in filtered_names

        if materials[name]["category"]
        in selected_categories
    ]

    st.caption(
        f"{len(filtered_names)} of "
        f"{len(names_all)} materials"
    )

    st.caption(
        "SELECTED MATERIALS"
    )

    defaults = [

        name

        for name in [
            "Aluminium",
            "Copper",
            "Alumina (Al₂O₃)",
            "Polyethylene HDPE — solid"
        ]

        if name in filtered_names
    ]

    chosen = st.multiselect(

        "Selected materials",

        filtered_names,

        default=(
            defaults
            if defaults
            else filtered_names[:3]
        ),

        label_visibility="collapsed"
    )

    st.divider()

    st.caption(
        "TEMPERATURE RANGE"
    )

    t_lo, t_hi = st.slider(

        "Temperature",

        min_value=int(
            np.floor(global_min)
        ),

        max_value=int(
            np.ceil(global_max)
        ),

        value=(

            int(
                np.floor(global_min)
            ),

            1500
            if global_max > 1500
            else int(
                np.ceil(global_max)
            )
        ),

        step=10,

        label_visibility="collapsed"
    )

    st.caption(
        "Curves are shown only within "
        "their validated temperature ranges."
    )


# ============================================================
# EMPTY STATE
# ============================================================

if not chosen:

    st.info(
        "Select one or more materials from the sidebar."
    )

    st.stop()


# ============================================================
# VALIDATION WARNING
# ============================================================

flagged = []

for name in chosen:

    material = materials[name]

    if coverage_gap(
        material,
        t_lo,
        t_hi
    ):

        flagged.append(

            f"{name} — validated range "
            f"{material['tmin']:.0f}–"
            f"{material['tmax']:.0f} K"
        )


if flagged:

    st.warning(

        "Some selected materials extend outside "
        "their validated temperature range:\n\n"
        + "\n".join(
            f"• {x}"
            for x in flagged
        )
    )


# ============================================================
# CHART TITLE
# ============================================================

st.subheader(
    "Cp vs Temperature"
)

st.caption(
    "Specific heat capacity at constant pressure"
)

st.caption(
    f"{len(chosen)} materials  ·  "
    f"{t_lo:.0f}–{t_hi:.0f} K  ·  "
    f"J kg⁻¹ K⁻¹"
)


# ============================================================
# MAIN GRAPH
# ============================================================

fig = go.Figure()

for i, name in enumerate(chosen):

    material = materials[name]

    T, C = material_curve(
        material,
        t_lo,
        t_hi
    )

    if T.size == 0:
        continue

    fig.add_trace(

        go.Scatter(

            x=T,

            y=C,

            mode="lines",

            name=name,

            line=dict(

                color=PALETTE[
                    i % len(PALETTE)
                ],

                width=2.6
            ),

            connectgaps=False,

            hovertemplate=(

                "<b>%{fullData.name}</b><br>"

                "Temperature: %{x:.0f} K<br>"

                "Cp: %{y:.1f} J kg⁻¹ K⁻¹"

                "<extra></extra>"
            )
        )
    )


# ============================================================
# GRAPH DESIGN
# ============================================================

fig.update_layout(

    height=540,

    paper_bgcolor="#ffffff",

    plot_bgcolor="#ffffff",

    margin=dict(
        l=82,
        r=40,
        t=30,
        b=72
    ),

    font=dict(
        family="Arial, sans-serif",
        size=11,
        color="#707780"
    ),

    hovermode="closest",

    hoverlabel=dict(
        bgcolor="#25272b",
        bordercolor="#25272b",
        font=dict(
            color="#ffffff",
            size=11
        )
    ),

    legend=dict(
        bgcolor="rgba(255,255,255,0.96)",
        bordercolor="#c8ccd2",
        borderwidth=1,
        font=dict(
            color="#555c65",
            size=10
        )
    ),

    xaxis=dict(

        title=dict(

            text="Temperature, T (K)",

            font=dict(
                color="#555b64",
                size=12
            )
        ),

        showline=True,

        mirror=True,

        linecolor="#949aa3",

        linewidth=1.2,

        ticks="outside",

        tickcolor="#949aa3",

        tickfont=dict(
            color="#777e88",
            size=10
        ),

        gridcolor="#eaecf0",

        gridwidth=1,

        zeroline=False
    ),

    yaxis=dict(

        title=dict(

            text="Specific heat, Cp (J kg⁻¹ K⁻¹)",

            font=dict(
                color="#555b64",
                size=12
            )
        ),

        showline=True,

        mirror=True,

        linecolor="#949aa3",

        linewidth=1.2,

        ticks="outside",

        tickcolor="#949aa3",

        tickfont=dict(
            color="#777e88",
            size=10
        ),

        gridcolor="#eaecf0",

        gridwidth=1,

        zeroline=False
    )
)


st.plotly_chart(

    fig,

    use_container_width=True,

    config={
        "displaylogo": False,
        "responsive": True,
        "toImageButtonOptions": {
            "filename": "Cp_vs_T",
            "scale": 2
        }
    }
)

st.caption(
    "Drag to zoom · double-click to reset · "
    "camera icon to export."
)


# ============================================================
# TABS
# ============================================================

tab_compare, tab_materials, tab_rankings, tab_data = st.tabs(
    [
        "Compare",
        "Materials",
        "Rankings",
        "Data"
    ]
)


# ============================================================
# COMPARE
# ============================================================

with tab_compare:

    st.subheader(
        "Compare materials"
    )

    st.caption(
        "Compare specific heat at a selected temperature."
    )

    Tc = st.slider(

        "Comparison temperature (K)",

        int(t_lo),

        int(t_hi),

        value=min(
            max(
                298,
                int(t_lo)
            ),
            int(t_hi)
        ),

        step=5,

        key="comparison_temperature"
    )

    rows = []

    missing = []

    for name in chosen:

        value = cp_value(
            materials[name],
            Tc
        )

        if np.isfinite(value):

            rows.append(
                (
                    name,
                    value
                )
            )

        else:

            missing.append(
                name
            )

    if rows:

        rows.sort(
            key=lambda x: x[1],
            reverse=True
        )

        labels = [
            x[0]
            for x in rows
        ]

        values = [
            x[1]
            for x in rows
        ]

        bar = go.Figure(

            go.Bar(

                x=values,

                y=labels,

                orientation="h",

                marker_color="#0071E3",

                text=[
                    f"{v:.0f}"
                    for v in values
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

            height=max(
                280,
                65 * len(rows)
            ),

            paper_bgcolor="#ffffff",

            plot_bgcolor="#ffffff",

            margin=dict(
                l=30,
                r=80,
                t=25,
                b=65
            ),

            xaxis=dict(

                title=dict(

                    text=(
                        f"Specific heat at "
                        f"{Tc:.0f} K "
                        "(J kg⁻¹ K⁻¹)"
                    ),

                    font=dict(
                        size=12,
                        color="#555b64"
                    )
                ),

                showline=True,

                mirror=True,

                linecolor="#949aa3",

                gridcolor="#eaecf0",

                tickfont=dict(
                    size=10,
                    color="#777e88"
                )
            ),

            yaxis=dict(

                autorange="reversed",

                showline=True,

                mirror=True,

                linecolor="#949aa3",

                tickfont=dict(
                    size=10,
                    color="#555b64"
                )
            )
        )

        st.plotly_chart(

            bar,

            use_container_width=True,

            config={
                "displaylogo": False
            }
        )

    else:

        st.info(
            "None of the selected materials are "
            "valid at this temperature."
        )

    if missing:

        st.caption(
            f"Not valid at {Tc:.0f} K: "
            + ", ".join(missing)
        )


# ============================================================
# MATERIAL INFORMATION
# ============================================================

with tab_materials:

    st.subheader(
        "Material information"
    )

    st.caption(
        "Properties and provenance for the selected materials."
    )

    records = []

    for name in chosen:

        material = materials[name]

        records.append({

            "Material":
                material["name"],

            "Formula":
                material["formula"],

            "Category":
                material["category"],

            "Valid T range (K)":
                f"{material['tmin']:.0f} – "
                f"{material['tmax']:.0f}",

            "Cp @ 298 K":
                (
                    None
                    if not np.isfinite(
                        material["cp298"]
                    )
                    else round(
                        material["cp298"],
                        1
                    )
                ),

            "Molar mass":
                (
                    None
                    if not np.isfinite(
                        material["molar"]
                    )
                    else round(
                        material["molar"],
                        3
                    )
                ),

            "Density":
                (
                    None
                    if not np.isfinite(
                        material["density"]
                    )
                    else round(
                        material["density"],
                        0
                    )
                ),

            "Source":
                material["source"]
        })

    st.dataframe(

        pd.DataFrame(records),

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# RANKINGS
# ============================================================

with tab_rankings:

    st.subheader(
        "Material ranking"
    )

    st.caption(
        "Rank materials by specific heat at a selected temperature."
    )

    c1, c2 = st.columns(2)

    with c1:

        Tr = st.slider(

            "Ranking temperature (K)",

            int(global_min),

            int(global_max),

            value=min(
                max(
                    298,
                    int(global_min)
                ),
                int(global_max)
            ),

            step=5,

            key="ranking_temperature"
        )

    with c2:

        topn = st.number_input(

            "Materials to show",

            min_value=5,

            max_value=50,

            value=15,

            step=5
        )

    ranking = rank_materials(
        materials,
        Tr
    )

    if ranking.empty:

        st.info(
            "No materials are valid at this temperature."
        )

    else:

        order = st.radio(

            "Sort",

            [
                "Highest Cp",
                "Lowest Cp"
            ],

            horizontal=True,

            key="ranking_order"
        )

        if order == "Highest Cp":

            view = ranking.head(
                int(topn)
            )

        else:

            view = ranking.tail(
                int(topn)
            )

        ranking_fig = go.Figure(

            go.Bar(

                x=view["Cp (J/kg·K)"],

                y=view["Material"],

                orientation="h",

                marker_color="#0071E3",

                hovertemplate=(

                    "<b>%{y}</b><br>"

                    "Cp = %{x:.1f} J kg⁻¹ K⁻¹"

                    "<extra></extra>"
                )
            )
        )

        ranking_fig.update_layout(

            height=max(
                340,
                32 * len(view)
            ),

            paper_bgcolor="#ffffff",

            plot_bgcolor="#ffffff",

            margin=dict(
                l=30,
                r=45,
                t=25,
                b=65
            ),

            xaxis=dict(

                title=dict(

                    text=(
                        f"Specific heat at "
                        f"{Tr:.0f} K "
                        "(J kg⁻¹ K⁻¹)"
                    ),

                    font=dict(
                        size=12,
                        color="#555b64"
                    )
                ),

                showline=True,

                mirror=True,

                linecolor="#949aa3",

                gridcolor="#eaecf0",

                tickfont=dict(
                    size=10,
                    color="#777e88"
                )
            ),

            yaxis=dict(

                autorange="reversed",

                showline=True,

                mirror=True,

                linecolor="#949aa3",

                tickfont=dict(
                    size=10,
                    color="#555b64"
                )
            )
        )

        st.plotly_chart(

            ranking_fig,

            use_container_width=True,

            config={
                "displaylogo": False
            }
        )

        st.caption(
            f"{len(ranking)} materials have a valid "
            f"fit at {Tr:.0f} K."
        )


# ============================================================
# DATA EXPORT
# ============================================================

with tab_data:

    st.subheader(
        "Computed data"
    )

    st.caption(
        "Sampled Cp–T values for the current selection."
    )

    frames = []

    for name in chosen:

        T, C = material_curve(

            materials[name],

            t_lo,

            t_hi
        )

        if T.size:

            frames.append(

                pd.DataFrame({

                    "Material": name,

                    "T (K)": T,

                    "Cp (J/kg·K)": C

                }).dropna()
            )

    if frames:

        output = pd.concat(
            frames,
            ignore_index=True
        )

        st.dataframe(

            output.head(500),

            use_container_width=True,

            hide_index=True
        )

        st.download_button(

            "Download curve data (CSV)",

            output.to_csv(
                index=False
            ).encode("utf-8"),

            file_name="cp_vs_T_export.csv",

            mime="text/csv"
        )

        st.caption(
            f"{len(output):,} computed points "
            f"across {len(frames)} materials."
        )

    else:

        st.info(
            "Nothing to export for the current selection."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Specific Heat Explorer · "
    "Thermodynamic data shown within "
    "validated temperature ranges"
)
