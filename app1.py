import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Specific Heat Explorer",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DATA CONFIG
# ============================================================

DATA_FILE = Path(__file__).parent / "materials.csv"

COLS = [
    "idx", "name", "formula", "category", "cas",
    "tmin", "tmax", "A", "B", "C", "D", "E",
    "a0", "a1", "a2", "a3", "r2",
    "cp298", "molar", "density", "source", "notes"
]

NUMERIC = [
    "tmin", "tmax",
    "A", "B", "C", "D", "E",
    "a0", "a1", "a2", "a3",
    "r2", "cp298", "molar", "density"
]

COLORS = [
    "#4E86C4",
    "#58A96B",
    "#D99838",
    "#8A68AE",
    "#5B9FBD",
    "#C86C75",
    "#719D8A",
    "#9A7957"
]

CP_LO = 0.0
CP_HI = 20000.0


# ============================================================
# UI
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   MAIN BACKGROUND
   ========================================================== */

html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #e3e5e8 !important;
    color: #202124 !important;
}

.block-container {
    max-width: 1320px !important;
    padding-top: 1.35rem !important;
    padding-bottom: 3rem !important;
}

header[data-testid="stHeader"] {
    background: rgba(227,229,232,0.90) !important;
    border-bottom: 1px solid #c5c9ce !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
}


/* ==========================================================
   GLOBAL TEXT
   ========================================================== */

.stApp p,
.stApp span,
.stApp label,
.stApp div {
    color: #30343a;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: #111111 !important;
}

h1 {
    font-size: 2.15rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.045em !important;
}

h2 {
    font-size: 1.38rem !important;
    font-weight: 650 !important;
}

h3 {
    font-size: 1.08rem !important;
    font-weight: 650 !important;
}

p {
    color: #454b52 !important;
    font-weight: 400 !important;
}

[data-testid="stCaptionContainer"] {
    color: #5c636b !important;
    font-size: 0.76rem !important;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            145deg,
            #eceef0 0%,
            #dfe2e6 100%
        ) !important;

    border-right: 1px solid #bfc4ca !important;

    box-shadow:
        6px 0 24px rgba(0,0,0,0.04) !important;
}

section[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #111111 !important;
    font-weight: 700 !important;
}


/* Sidebar labels */

section[data-testid="stSidebar"]
[data-testid="stMarkdownContainer"] p {
    color: #3e444b !important;
    font-size: 0.66rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
}


/* ==========================================================
   SEARCH
   ========================================================== */

section[data-testid="stSidebar"]
div[data-testid="stTextInput"] > div > div {

    background: rgba(255,255,255,0.68) !important;

    border: 1px solid #c1c6cc !important;

    border-radius: 12px !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.9),
        0 4px 12px rgba(0,0,0,0.04) !important;

    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
}

section[data-testid="stSidebar"]
div[data-testid="stTextInput"] input {

    background: transparent !important;

    color: #111111 !important;

    border: none !important;

    font-size: 0.83rem !important;

    font-weight: 450 !important;
}

section[data-testid="stSidebar"]
div[data-testid="stTextInput"] input::placeholder {
    color: #7d858e !important;
}


/* ==========================================================
   MULTISELECT
   ========================================================== */

section[data-testid="stSidebar"]
div[data-testid="stMultiSelect"]
div[data-baseweb="select"] > div {

    background: rgba(247,248,249,0.75) !important;

    background-color: rgba(247,248,249,0.75) !important;

    border: 1px solid #bfc4ca !important;

    border-radius: 11px !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.9),
        0 3px 10px rgba(0,0,0,0.04) !important;

    color: #111111 !important;

    min-height: 42px !important;
}


/* No red focus */

section[data-testid="stSidebar"]
div[data-testid="stMultiSelect"]
div[data-baseweb="select"] > div:focus-within {

    border-color: #7f8d9a !important;

    box-shadow:
        0 0 0 3px rgba(100,120,140,0.13) !important;
}


/* ==========================================================
   SELECTED CHIPS
   ========================================================== */

section[data-testid="stSidebar"]
div[data-testid="stMultiSelect"]
[data-baseweb="tag"] {

    background: #d8dce0 !important;

    background-color: #d8dce0 !important;

    border: 1px solid #bdc3c9 !important;

    border-radius: 8px !important;

    color: #202124 !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.7) !important;
}

section[data-testid="stSidebar"]
div[data-testid="stMultiSelect"]
[data-baseweb="tag"] span {

    color: #202124 !important;

    font-size: 0.75rem !important;

    font-weight: 550 !important;
}

section[data-testid="stSidebar"]
div[data-testid="stMultiSelect"]
[data-baseweb="tag"] svg {

    color: #555c64 !important;
}


/* ==========================================================
   DROPDOWN
   ========================================================== */

div[data-baseweb="popover"] {

    background: #eef0f2 !important;

    background-color: #eef0f2 !important;

    border: 1px solid #b9bfc5 !important;

    border-radius: 12px !important;

    box-shadow:
        0 16px 38px rgba(0,0,0,0.17) !important;

    color: #202124 !important;

    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
}

div[data-baseweb="popover"] * {
    color: #202124 !important;
}

div[data-baseweb="popover"]
div[data-baseweb="menu"] {

    background: #eef0f2 !important;
}

div[data-baseweb="popover"]
[role="option"] {

    background: transparent !important;

    color: #202124 !important;

    font-size: 0.82rem !important;

    font-weight: 450 !important;

    border-radius: 8px !important;

    margin: 2px 5px !important;
}

div[data-baseweb="popover"]
[role="option"]:hover {

    background: #d9dde1 !important;

    color: #111111 !important;
}

div[data-baseweb="popover"]
[role="option"][aria-selected="true"] {

    background: #d0d5da !important;

    color: #111111 !important;

    font-weight: 650 !important;
}


/* Dropdown search */

div[data-baseweb="popover"] input {

    background: #ffffff !important;

    color: #111111 !important;

    border: 1px solid #c1c6cc !important;

    border-radius: 8px !important;
}


/* ==========================================================
   SLIDER
   ========================================================== */

section[data-testid="stSidebar"]
[data-testid="stSlider"] [role="slider"] {

    background: #63798b !important;

    border-color: #63798b !important;
}


/* ==========================================================
   METRIC CARDS
   ========================================================== */

div[data-testid="stMetric"] {

    background: #eceef0 !important;

    border: 1px solid #c8cdd2 !important;

    border-radius: 13px !important;

    padding: 10px 14px !important;

    box-shadow:
        0 3px 10px rgba(0,0,0,0.025) !important;
}

div[data-testid="stMetricLabel"] {

    color: #3f454c !important;

    font-size: 0.72rem !important;

    font-weight: 600 !important;
}

div[data-testid="stMetricValue"] {

    color: #111111 !important;

    font-size: 1.4rem !important;

    font-weight: 700 !important;
}


/* ==========================================================
   WARNING
   ========================================================== */

div[data-testid="stAlert"] {

    background: #ece9dd !important;

    border: 1px solid #cbc5b2 !important;

    border-radius: 11px !important;

    color: #35332d !important;
}

div[data-testid="stAlert"] p {

    color: #35332d !important;

    font-size: 0.78rem !important;

    font-weight: 450 !important;
}


/* ==========================================================
   CHART CONTAINER
   ========================================================== */

div[data-testid="stPlotlyChart"] {

    background: #dfe2e5 !important;

    border: 1px solid #969da5 !important;

    border-radius: 14px !important;

    padding: 5px !important;

    box-shadow:
        0 5px 16px rgba(0,0,0,0.045) !important;
}


/* ==========================================================
   TABS
   ========================================================== */

.stTabs [data-baseweb="tab-list"] {

    background: transparent !important;

    border-bottom: 1px solid #bfc4ca !important;
}

.stTabs [data-baseweb="tab"] {

    color: #41474e !important;

    font-size: 0.83rem !important;

    font-weight: 550 !important;
}

.stTabs [aria-selected="true"] {

    color: #111111 !important;

    font-weight: 700 !important;
}

.stTabs [data-baseweb="tab-highlight"] {

    background: #63798b !important;
}


/* ==========================================================
   DATAFRAME
   ========================================================== */

[data-testid="stDataFrame"] {

    border: 1px solid #aeb4bb !important;

    border-radius: 11px !important;

    overflow: hidden !important;
}


/* ==========================================================
   BUTTON
   ========================================================== */

.stDownloadButton button {

    background: #657989 !important;

    color: #ffffff !important;

    border: none !important;

    border-radius: 9px !important;

    font-size: 0.80rem !important;

    font-weight: 650 !important;
}

.stDownloadButton button:hover {

    background: #566a7a !important;
}


/* ==========================================================
   DIVIDER
   ========================================================== */

hr {
    border-top: 1px solid #c4c9ce !important;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# DATA FUNCTIONS
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

        materials[name]["segments"].append(segment)

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

    for c in NUMERIC:

        df[c] = pd.to_numeric(
            df[c],
            errors="coerce"
        )

    return build_materials(df)


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
# LOAD MATERIAL DATABASE
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
        "Search",
        placeholder="Search material or formula...",
        label_visibility="collapsed"
    ).strip().lower()


    st.caption(
        "MATERIAL CLASS"
    )

    selected_categories = st.multiselect(

        "Material classes",

        categories_all,

        default=categories_all,

        label_visibility="collapsed"
    )

    if not selected_categories:

        selected_categories = categories_all


    filtered_names = [

        name

        for name in names_all

        if (
            materials[name]["category"]
            in selected_categories
        )

        and (

            not search

            or search in name.lower()

            or search in
            materials[name]["formula"].lower()
        )
    ]


    st.caption(
        f"{len(filtered_names)} of "
        f"{len(names_all)} materials"
    )


    st.caption(
        "SELECTED MATERIALS"
    )


    preferred = [

        "Aluminium",
        "Copper",
        "Alumina (Al₂O₃)",
        "Polyethylene HDPE — solid"
    ]

    defaults = [

        x

        for x in preferred

        if x in filtered_names
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


    st.header(
        "Temperature"
    )


    t_lo, t_hi = st.slider(

        "Temperature range",

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

            min(
                1500,
                int(
                    np.ceil(global_max)
                )
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
# HEADER
# ============================================================

st.markdown(
    """
    <div style="
        color:#343a40;
        font-size:0.68rem;
        font-weight:700;
        letter-spacing:0.08em;
        margin-bottom:5px;
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
        color:#3f464d;
        font-size:0.88rem;
        font-weight:450;
        margin-bottom:20px;
    ">
        Interactive C<sub>p</sub>–T database for engineering materials
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SUMMARY CARDS
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
# EMPTY STATE
# ============================================================

if not chosen:

    st.markdown(
        """
        <div style="
            background:#e9ebed;
            border:1px solid #aeb5bc;
            border-radius:15px;
            padding:55px 25px;
            text-align:center;
            margin-top:20px;
        ">

            <div style="
                color:#111111;
                font-size:1.18rem;
                font-weight:700;
                margin-bottom:8px;
            ">
                Select a material
            </div>

            <div style="
                color:#454b52;
                font-size:0.82rem;
                font-weight:400;
            ">
                Choose one or more materials from the sidebar
                to explore specific heat versus temperature.
            </div>

        </div>
        """,
        unsafe_allow_html=True
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
# CHART HEADER
# ============================================================

st.markdown(
    """
    <div style="
        margin-top:20px;
        margin-bottom:8px;
    ">

        <div style="
            color:#111111;
            font-size:1.25rem;
            font-weight:700;
            letter-spacing:-0.02em;
        ">
            Cp vs Temperature
        </div>

        <div style="
            color:#454b52;
            font-size:0.80rem;
            font-weight:400;
            margin-top:4px;
        ">
            Specific heat capacity at constant pressure
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div style="
        display:flex;
        gap:8px;
        flex-wrap:wrap;
        margin-bottom:8px;
    ">

        <span style="
            background:#eceef0;
            border:1px solid #c5cad0;
            color:#30353b;
            border-radius:999px;
            padding:4px 10px;
            font-size:0.72rem;
            font-weight:550;
        ">
            {len(chosen)} materials
        </span>

        <span style="
            background:#eceef0;
            border:1px solid #c5cad0;
            color:#30353b;
            border-radius:999px;
            padding:4px 10px;
            font-size:0.72rem;
            font-weight:550;
        ">
            {t_lo:.0f}–{t_hi:.0f} K
        </span>

        <span style="
            background:#eceef0;
            border:1px solid #c5cad0;
            color:#30353b;
            border-radius:999px;
            padding:4px 10px;
            font-size:0.72rem;
            font-weight:550;
        ">
            J kg⁻¹ K⁻¹
        </span>

    </div>
    """,
    unsafe_allow_html=True
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
                color=COLORS[
                    i % len(COLORS)
                ],
                width=2.7
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


fig.update_layout(

    height=530,

    paper_bgcolor="#dfe2e5",

    plot_bgcolor="#f3f4f5",

    margin=dict(
        l=78,
        r=35,
        t=25,
        b=70
    ),

    font=dict(
        family="Arial, sans-serif",
        size=11,
        color="#555c64"
    ),

    hovermode="closest",

    legend=dict(
        bgcolor="rgba(247,248,249,0.95)",
        bordercolor="#a8afb6",
        borderwidth=1,
        font=dict(
            size=10,
            color="#30353b"
        )
    ),

    xaxis=dict(

        title=dict(
            text="Temperature, T (K)",
            font=dict(
                size=12,
                color="#202124"
            )
        ),

        showline=True,
        mirror=True,
        linecolor="#7e878f",
        linewidth=1.3,

        ticks="outside",
        tickcolor="#7e878f",

        tickfont=dict(
            size=10,
            color="#4e555d"
        ),

        gridcolor="#d9dde1",
        zeroline=False
    ),

    yaxis=dict(

        title=dict(
            text="Specific heat, Cp (J kg⁻¹ K⁻¹)",
            font=dict(
                size=12,
                color="#202124"
            )
        ),

        showline=True,
        mirror=True,
        linecolor="#7e878f",
        linewidth=1.3,

        ticks="outside",
        tickcolor="#7e878f",

        tickfont=dict(
            size=10,
            color="#4e555d"
        ),

        gridcolor="#d9dde1",
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
                (name, value)
            )

        else:

            missing.append(name)


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


        comparison = go.Figure(

            go.Bar(

                x=values,

                y=labels,

                orientation="h",

                marker_color="#71869A",

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


        comparison.update_layout(

            height=max(
                280,
                60 * len(rows)
            ),

            paper_bgcolor="#dfe2e5",

            plot_bgcolor="#f3f4f5",

            margin=dict(
                l=30,
                r=70,
                t=25,
                b=65
            ),

            xaxis=dict(
                title=(
                    f"Specific heat at "
                    f"{Tc:.0f} K "
                    f"(J kg⁻¹ K⁻¹)"
                ),
                showline=True,
                mirror=True,
                linecolor="#7e878f",
                gridcolor="#d9dde1",
                tickfont=dict(
                    size=10,
                    color="#4e555d"
                )
            ),

            yaxis=dict(
                autorange="reversed",
                showline=True,
                mirror=True,
                linecolor="#7e878f",
                tickfont=dict(
                    size=10,
                    color="#30353b"
                )
            )
        )


        st.plotly_chart(
            comparison,
            use_container_width=True,
            config={"displaylogo": False}
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
# MATERIALS
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
                (
                    f"{material['tmin']:.0f} – "
                    f"{material['tmax']:.0f}"
                ),

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

            horizontal=True
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

                marker_color="#71869A",

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

            paper_bgcolor="#dfe2e5",

            plot_bgcolor="#f3f4f5",

            margin=dict(
                l=30,
                r=50,
                t=25,
                b=65
            ),

            xaxis=dict(

                title=(
                    f"Specific heat at "
                    f"{Tr:.0f} K "
                    "(J kg⁻¹ K⁻¹)"
                ),

                showline=True,
                mirror=True,
                linecolor="#7e878f",
                gridcolor="#d9dde1",

                tickfont=dict(
                    size=10,
                    color="#4e555d"
                )
            ),

            yaxis=dict(

                autorange="reversed",

                showline=True,
                mirror=True,
                linecolor="#7e878f",

                tickfont=dict(
                    size=10,
                    color="#30353b"
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


# ============================================================
# DATA
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

                    "Material":
                        name,

                    "T (K)":
                        T,

                    "Cp (J/kg·K)":
                        C

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
            f"{len(output):,} computed points."
        )

    else:

        st.info(
            "Nothing to export for the current selection."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#4c535b;
        font-size:0.70rem;
        font-weight:450;
        padding:5px 0 15px 0;
    ">
        Specific Heat Explorer ·
        Thermodynamic data shown within validated temperature ranges
    </div>
    """,
    unsafe_allow_html=True
)
