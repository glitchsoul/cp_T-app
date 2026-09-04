import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# CONFIG
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
    "cp298", "molar", "density", "source", "notes"
]

NUMERIC = [
    "tmin", "tmax", "a0", "a1", "a2", "a3",
    "cp298", "molar", "density"
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

CP_LO = 0.0
CP_HI = 20000.0


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------------- PAGE ---------------- */

    .stApp {
        background: #f3f4f6;
    }

    [data-testid="stAppViewContainer"] {
        background: #f3f4f6;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    header[data-testid="stHeader"] {
        background: rgba(243,244,246,0.95);
    }

    /* ---------------- TEXT ---------------- */

    h1 {
        font-weight: 650 !important;
        letter-spacing: -0.045em !important;
        color: #202124 !important;
    }

    h2, h3 {
        font-weight: 600 !important;
        color: #202124 !important;
    }

    p {
        color: #69717d;
    }

    /* ---------------- SIDEBAR ---------------- */

    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #d9dce1;
    }

    section[data-testid="stSidebar"] > div {
        background: #ffffff !important;
    }

    /* ---------------- INPUTS ---------------- */

    div[data-testid="stTextInput"] input {
        background: #f8f9fb !important;
        border: 1px solid #c9cdd3 !important;
        border-radius: 10px !important;
        color: #202124 !important;
    }

    div[data-baseweb="select"] > div {
        background: #f8f9fb !important;
        border: 1px solid #c9cdd3 !important;
        border-radius: 10px !important;
    }

    /* Make selected items blue instead of red */

    div[data-baseweb="tag"] {
        background: #eaf3ff !important;
        border: 1px solid #c9e0fa !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="tag"] span {
        color: #075ca8 !important;
    }

    div[data-baseweb="tag"] svg {
        color: #075ca8 !important;
    }

    /* ---------------- BUTTONS ---------------- */

    .stDownloadButton button {
        background: #0071e3 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 550 !important;
    }

    .stDownloadButton button:hover {
        background: #0067cf !important;
    }

    /* ---------------- SLIDER ---------------- */

    [data-testid="stSlider"] [role="slider"] {
        background: #0071e3 !important;
        border-color: #0071e3 !important;
    }

    /* ---------------- TABS ---------------- */

    button[data-baseweb="tab"] {
        color: #69717d !important;
        font-weight: 500 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #202124 !important;
        font-weight: 600 !important;
    }

    /* ---------------- TABLE ---------------- */

    [data-testid="stDataFrame"] {
        border: 1px solid #cbd0d6 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* ---------------- ALERTS ---------------- */

    div[data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    /* ---------------- DIVIDERS ---------------- */

    hr {
        border-color: #d9dce1 !important;
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
                "segments": []
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

    for column in NUMERIC:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return build_materials(df)


# ============================================================
# CP CALCULATIONS
# ============================================================

def cp_poly(segment, temperature):

    temperature = np.asarray(
        temperature,
        dtype=float
    )

    return (
        segment["a0"]
        + segment["a1"] * temperature
        + segment["a2"] * temperature**2
        + segment["a3"] * temperature**3
    )


def cp_value(material, temperature):

    for segment in material["segments"]:

        if (
            segment["tmin"]
            <= temperature
            <= segment["tmax"]
        ):

            value = float(
                cp_poly(
                    segment,
                    temperature
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


# ============================================================
# RANKING
# ============================================================

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
                    round(value, 1)
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
    "Interactive **Cp–T** database for engineering materials."
)

# Small statistics row

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
        "Unit",
        "J kg⁻¹ K⁻¹"
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Materials")

    st.caption("SEARCH")

    search = st.text_input(
        "Search materials",
        placeholder="Material or formula...",
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

        filtered_names.append(name)

    st.caption("MATERIAL CLASS")

    selected_categories = st.multiselect(
        "Material class",
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

    default_materials = [

        name

        for name in [
            "Aluminium",
            "Copper",
            "Alumina (Al₂O₃)",
            "Polyethylene HDPE — solid"
        ]

        if name in filtered_names
    ]

    st.caption("SELECTED MATERIALS")

    selected_materials = st.multiselect(

        "Materials",

        filtered_names,

        default=(
            default_materials
            if default_materials
            else filtered_names[:3]
        ),

        label_visibility="collapsed"
    )

    st.divider()

    st.caption("TEMPERATURE RANGE")

    t_lo, t_hi = st.slider(

        "Temperature",

        min_value=int(global_min),

        max_value=int(global_max),

        value=(

            int(global_min),

            1500
            if global_max > 1500
            else int(global_max)
        ),

        step=10,

        label_visibility="collapsed"
    )


# ============================================================
# EMPTY
# ============================================================

if not selected_materials:

    st.info(
        "Select at least one material from the sidebar."
    )

    st.stop()


# ============================================================
# WARNING
# ============================================================

flagged = []

for name in selected_materials:

    material = materials[name]

    if coverage_gap(
        material,
        t_lo,
        t_hi
    ):

        flagged.append(
            f"{name} — "
            f"validated range "
            f"{material['tmin']:.0f}–"
            f"{material['tmax']:.0f} K"
        )


if flagged:

    st.warning(
        "Some selected materials extend outside "
        "their validated temperature range:\n\n"
        + "\n".join(
            f"• {item}"
            for item in flagged
        )
    )


# ============================================================
# MAIN CHART CARD
# ============================================================

st.subheader(
    "Cp vs Temperature"
)

st.caption(
    "Specific heat capacity at constant pressure"
)

st.caption(
    f"{len(selected_materials)} materials  ·  "
    f"{t_lo:.0f}–{t_hi:.0f} K  ·  "
    f"J kg⁻¹ K⁻¹"
)


# ============================================================
# GRAPH
# ============================================================

fig = go.Figure()

for i, name in enumerate(selected_materials):

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
                width=2.8
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

    height=560,

    paper_bgcolor="#ffffff",

    plot_bgcolor="#ffffff",

    margin=dict(
        l=80,
        r=40,
        t=25,
        b=75
    ),

    font=dict(
        family="Arial, sans-serif",
        color="#5f6368",
        size=12
    ),

    legend=dict(
        bgcolor="rgba(255,255,255,0.96)",
        bordercolor="#bfc4cb",
        borderwidth=1,
        font=dict(
            size=11,
            color="#4b5058"
        )
    ),

    hoverlabel=dict(
        bgcolor="#202124",
        font=dict(
            color="white"
        )
    ),

    xaxis=dict(

        title=dict(
            text="Temperature, T (K)",
            font=dict(
                size=13,
                color="#454a52"
            )
        ),

        showline=True,

        mirror=True,

        linecolor="#8f959e",

        linewidth=1.3,

        gridcolor="#e9ebee",

        gridwidth=1,

        zeroline=False,

        ticks="outside",

        tickcolor="#8f959e",

        tickfont=dict(
            size=11,
            color="#727983"
        )
    ),

    yaxis=dict(

        title=dict(
            text="Specific heat, Cp (J kg⁻¹ K⁻¹)",
            font=dict(
                size=13,
                color="#454a52"
            )
        ),

        showline=True,

        mirror=True,

        linecolor="#8f959e",

        linewidth=1.3,

        gridcolor="#e9ebee",

        gridwidth=1,

        zeroline=False,

        ticks="outside",

        tickcolor="#8f959e",

        tickfont=dict(
            size=11,
            color="#727983"
        )
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
        "Specific heat at a selected temperature."
    )

    comparison_temperature = st.slider(

        "Comparison temperature (K)",

        int(t_lo),

        int(t_hi),

        value=min(
            max(298, int(t_lo)),
            int(t_hi)
        ),

        step=5,

        key="comparison_temperature"
    )

    comparison_rows = []

    for name in selected_materials:

        value = cp_value(
            materials[name],
            comparison_temperature
        )

        if np.isfinite(value):

            comparison_rows.append(
                (
                    name,
                    value
                )
            )

    if comparison_rows:

        comparison_rows.sort(
            key=lambda x: x[1],
            reverse=True
        )

        labels = [
            x[0]
            for x in comparison_rows
        ]

        values = [
            x[1]
            for x in comparison_rows
        ]

        comparison_fig = go.Figure(

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

        comparison_fig.update_layout(

            height=max(
                300,
                65 * len(labels)
            ),

            paper_bgcolor="#ffffff",

            plot_bgcolor="#ffffff",

            margin=dict(
                l=30,
                r=80,
                t=20,
                b=65
            ),

            xaxis=dict(
                title=(
                    f"Cp at "
                    f"{comparison_temperature:.0f} K "
                    "(J kg⁻¹ K⁻¹)"
                ),
                showline=True,
                mirror=True,
                linecolor="#8f959e",
                gridcolor="#e9ebee"
            ),

            yaxis=dict(
                autorange="reversed",
                showline=True,
                mirror=True,
                linecolor="#8f959e"
            )
        )

        st.plotly_chart(
            comparison_fig,
            use_container_width=True,
            config={
                "displaylogo": False
            }
        )


# ============================================================
# MATERIALS
# ============================================================

with tab_materials:

    st.subheader(
        "Material information"
    )

    records = []

    for name in selected_materials:

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
        "Rank materials by specific heat."
    )

    ranking_temperature = st.slider(

        "Ranking temperature (K)",

        int(global_min),

        int(global_max),

        value=min(
            max(298, int(global_min)),
            int(global_max)
        ),

        step=5,

        key="ranking_temperature"
    )

    ranking = rank_materials(
        materials,
        ranking_temperature
    )

    if not ranking.empty:

        st.dataframe(
            ranking,
            use_container_width=True
        )


# ============================================================
# DATA
# ============================================================

with tab_data:

    st.subheader(
        "Computed data"
    )

    frames = []

    for name in selected_materials:

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

    else:

        st.info(
            "Nothing to export."
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
