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


# ============================================================
# MATERIAL COLORS (for charts – unchanged)
# ============================================================

MATERIAL_COLORS = [
    "#2E6F95",   # deep slate blue
    "#3D9E6D",   # teal green
    "#C77D1E",   # golden amber
    "#8A5D9E",   # soft purple
    "#4A8B9F",   # light teal
    "#BF6F6F",   # muted coral
    "#5E8C7A",   # sage
    "#A67C52",   # warm brown
]

CP_LO = 0.0
CP_HI = 20000.0


# ============================================================
# CSS – with new sidebar box colours
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   GLOBAL
   ========================================================== */

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #e2e4e7 !important;
    color: #1a1c1e !important;
}

.block-container {
    max-width: 1320px !important;
    padding-top: 1.4rem !important;
    padding-bottom: 3rem !important;
}

header[data-testid="stHeader"] {
    background: rgba(226,228,231,0.88) !important;
    border-bottom: 1px solid #c3c7cc !important;
    backdrop-filter: blur(22px) !important;
}


/* ==========================================================
   TEXT – all dark
   ========================================================== */

.stApp p, .stApp span, .stApp label {
    color: #1a1c1e !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #0a0c0e !important;
}

h1 {
    font-size: 2.15rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.045em !important;
    margin-bottom: 0.25rem !important;
}

h2 {
    font-size: 1.35rem !important;
    font-weight: 700 !important;
}

h3 {
    font-size: 1.05rem !important;
    font-weight: 650 !important;
}

[data-testid="stCaptionContainer"] p {
    color: #2c3036 !important;
    font-size: 0.76rem !important;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {
    background: linear-gradient(145deg, #eceef0, #dfe2e5) !important;
    border-right: 1px solid #bfc4ca !important;
    box-shadow: 7px 0 24px rgba(0,0,0,0.045) !important;
}

section[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #0a0c0e !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #1a1c1e !important;
    font-size: 0.67rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.055em !important;
}


/* ==========================================================
   SEARCH BAR
   ========================================================== */

section[data-testid="stSidebar"] div[data-testid="stTextInput"] > div > div {
    background: rgba(250,251,252,0.72) !important;
    border: 1px solid #bfc5cb !important;
    border-radius: 12px !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.9), 0 4px 13px rgba(0,0,0,0.045) !important;
    backdrop-filter: blur(18px) !important;
}

section[data-testid="stSidebar"] div[data-testid="stTextInput"] input {
    background: transparent !important;
    color: #1a1c1e !important;
    border: none !important;
    font-size: 0.83rem !important;
}

section[data-testid="stSidebar"] div[data-testid="stTextInput"] input::placeholder {
    color: #5a6068 !important;
}


/* ==========================================================
   MULTISELECT BOX – new colours
   ========================================================== */

/* The main dropdown area (where chips are) */
section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
    background: #d4e4f7 !important;        /* soft slate blue */
    border: 1px solid #8a9db0 !important;  /* slightly darker border */
    border-radius: 11px !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.85), 0 3px 10px rgba(0,0,0,0.035) !important;
    color: #1a1c1e !important;
    min-height: 42px !important;
}

section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div:focus-within {
    border-color: #657a8c !important;
    box-shadow: 0 0 0 3px rgba(105,125,145,0.13) !important;
}


/* ==========================================================
   SELECTED MATERIAL CHIPS – new colours
   ========================================================== */

section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background: #b8cfe0 !important;        /* slightly darker steel blue */
    border: 1px solid #7a94a8 !important;
    border-radius: 8px !important;
    color: #1a1c1e !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.5) !important;
}

section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] [data-baseweb="tag"] span {
    color: #1a1c1e !important;
    font-size: 0.75rem !important;
    font-weight: 550 !important;
}

/* Close icon – gray, not red */
section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] [data-baseweb="tag"] svg {
    color: #4a5058 !important;
    fill: #4a5058 !important;
    opacity: 0.8 !important;
}

section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] [data-baseweb="tag"] svg:hover {
    color: #1a1c1e !important;
    fill: #1a1c1e !important;
    opacity: 1 !important;
}


/* ==========================================================
   DROPDOWN POPOVER – no red/black highlights
   ========================================================== */

div[data-baseweb="popover"] {
    background: #eef0f2 !important;
    border: 1px solid #b9bfc5 !important;
    border-radius: 12px !important;
    box-shadow: 0 15px 38px rgba(0,0,0,0.16) !important;
    backdrop-filter: blur(22px) !important;
}

div[data-baseweb="popover"] * {
    color: #1a1c1e !important;
}

div[data-baseweb="popover"] div[data-baseweb="menu"] {
    background: #eef0f2 !important;
}

div[data-baseweb="popover"] [role="option"] {
    background: transparent !important;
    color: #1a1c1e !important;
    font-size: 0.82rem !important;
    border-radius: 8px !important;
    margin: 2px 5px !important;
}

div[data-baseweb="popover"] [role="option"]:hover {
    background: #cbd8e6 !important;
    color: #0a0c0e !important;
}

div[data-baseweb="popover"] [role="option"][aria-selected="true"] {
    background: #b3c9df !important;
    color: #0a0c0e !important;
    font-weight: 650 !important;
}

div[data-baseweb="popover"] [role="option"][aria-selected="true"]:hover {
    background: #a3bdd6 !important;
    color: #0a0c0e !important;
}


/* ==========================================================
   SLIDER
   ========================================================== */

section[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: #64798b !important;
    border-color: #64798b !important;
}


/* ==========================================================
   METRIC CARDS
   ========================================================== */

div[data-testid="stMetric"] {
    background: #ebedef !important;
    border: 1px solid #c6cbd0 !important;
    border-radius: 13px !important;
    padding: 10px 14px !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.025) !important;
}

div[data-testid="stMetricLabel"] {
    color: #2c3238 !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
}

div[data-testid="stMetricValue"] {
    color: #0a0c0e !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
}


/* ==========================================================
   WARNING – slate blue
   ========================================================== */

div[data-testid="stAlert"] {
    background: #d9e6f2 !important;
    border: 1px solid #7a9eb3 !important;
    border-radius: 11px !important;
}

div[data-testid="stAlert"] p {
    color: #1a2b3c !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
}


/* ==========================================================
   TABS
   ========================================================== */

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #bfc4ca !important;
}

.stTabs [data-baseweb="tab"] {
    color: #2c3238 !important;
    font-size: 0.82rem !important;
    font-weight: 550 !important;
}

.stTabs [aria-selected="true"] {
    color: #0a0c0e !important;
    font-weight: 700 !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background: #657a8c !important;
}


/* ==========================================================
   PLOTLY
   ========================================================== */

div[data-testid="stPlotlyChart"] {
    background: #dfe2e5 !important;
    border: 1px solid #8f979f !important;
    border-radius: 14px !important;
    padding: 5px !important;
    box-shadow: 0 5px 16px rgba(0,0,0,0.045) !important;
}


/* ==========================================================
   DATAFRAME
   ========================================================== */

div[data-testid="stDataFrame"] {
    border: 1px solid #aeb5bc !important;
    border-radius: 11px !important;
    overflow: hidden !important;
}


/* ==========================================================
   DOWNLOAD BUTTON
   ========================================================== */

.stDownloadButton button {
    background: #657a8c !important;
    color: white !important;
    border: none !important;
    border-radius: 9px !important;
    font-size: 0.80rem !important;
    font-weight: 650 !important;
}

.stDownloadButton button:hover {
    background: #566b7c !important;
}


/* ==========================================================
   DIVIDER
   ========================================================== */

hr {
    border-top: 1px solid #c1c6cb !important;
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
    for _, row in df.iterrows():
        name = str(row["name"]).strip()
        segment = {
            "tmin": row["tmin"],
            "tmax": row["tmax"],
            "a0": row["a0"],
            "a1": row["a1"],
            "a2": row["a2"],
            "a3": row["a3"],
            "notes": str(row["notes"]).strip()
        }
        if not (np.isfinite(segment["tmin"]) and np.isfinite(segment["tmax"])):
            continue
        if name not in materials:
            materials[name] = {
                "name": name,
                "formula": str(row["formula"]).strip(),
                "category": str(row["category"]).strip(),
                "cas": str(row["cas"]).strip(),
                "cp298": row["cp298"],
                "molar": row["molar"],
                "density": row["density"],
                "source": str(row["source"]).strip(),
                "segments": []
            }
        materials[name]["segments"].append(segment)

    for material in materials.values():
        material["segments"].sort(key=lambda x: x["tmin"])
        material["tmin"] = min(x["tmin"] for x in material["segments"])
        material["tmax"] = max(x["tmax"] for x in material["segments"])

    return materials


@st.cache_data
def load_materials():
    df = pd.read_csv(DATA_FILE)
    if len(df.columns) != len(COLS):
        raise ValueError(f"Expected {len(COLS)} columns in materials.csv, found {len(df.columns)}.")
    df.columns = COLS
    for column in NUMERIC:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return build_materials(df)


def cp_poly(segment, temperature):
    temperature = np.asarray(temperature, dtype=float)
    return (segment["a0"] + segment["a1"] * temperature +
            segment["a2"] * temperature**2 + segment["a3"] * temperature**3)


def cp_value(material, temperature):
    for segment in material["segments"]:
        if segment["tmin"] <= temperature <= segment["tmax"]:
            value = float(cp_poly(segment, temperature))
            if np.isfinite(value) and CP_LO < value < CP_HI:
                return value
            return np.nan
    return np.nan


def material_curve(material, t_lo, t_hi, n=400):
    span = max(t_hi - t_lo, 1e-9)
    x_parts = []
    y_parts = []

    for segment in material["segments"]:
        low = max(segment["tmin"], t_lo)
        high = min(segment["tmax"], t_hi)
        if high <= low:
            continue
        points = max(2, int(round(n * (high - low) / span)))
        temperature = np.linspace(low, high, points)
        capacity = cp_poly(segment, temperature)
        capacity = np.where(np.isfinite(capacity) & (capacity > CP_LO) & (capacity < CP_HI), capacity, np.nan)
        x_parts.append(temperature)
        y_parts.append(capacity)
        x_parts.append(np.array([np.nan]))
        y_parts.append(np.array([np.nan]))

    if not x_parts:
        return np.array([]), np.array([])
    return np.concatenate(x_parts), np.concatenate(y_parts)


def coverage_gap(material, t_lo, t_hi):
    return t_lo < material["tmin"] or t_hi > material["tmax"]


def rank_materials(materials, temperature):
    rows = []
    for material in materials.values():
        value = cp_value(material, temperature)
        if np.isfinite(value):
            rows.append({
                "Material": material["name"],
                "Formula": material["formula"],
                "Category": material["category"],
                "Cp (J/kg·K)": round(value, 1)
            })
    result = pd.DataFrame(rows)
    if not result.empty:
        result = result.sort_values("Cp (J/kg·K)", ascending=False).reset_index(drop=True)
        result.index += 1
    return result


# ============================================================
# LOAD DATABASE
# ============================================================

try:
    materials = load_materials()
except Exception as error:
    st.error(f"Could not load materials.csv — {error}")
    st.stop()

all_names = sorted(materials.keys())
all_categories = sorted({material["category"] for material in materials.values()})
global_min = min(material["tmin"] for material in materials.values())
global_max = max(material["tmax"] for material in materials.values())


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("Materials")
    st.caption("SEARCH")
    search_text = st.text_input(
        "Search",
        placeholder="Search material or formula...",
        label_visibility="collapsed"
    ).strip().lower()

    st.caption("MATERIAL CLASS")
    categories = st.multiselect(
        "Material classes",
        all_categories,
        default=all_categories,
        label_visibility="collapsed"
    )
    if not categories:
        categories = all_categories

    available = []
    for name in all_names:
        material = materials[name]
        category_ok = material["category"] in categories
        search_ok = not search_text or search_text in name.lower() or search_text in material["formula"].lower()
        if category_ok and search_ok:
            available.append(name)

    st.caption(f"{len(available)} of {len(all_names)} materials")

    st.caption("SELECTED MATERIALS")
    preferred = ["Aluminium", "Copper", "Alumina (Al₂O₃)", "Polyethylene HDPE — solid"]
    default_selection = [name for name in preferred if name in available]
    chosen = st.multiselect(
        "Selected materials",
        available,
        default=default_selection if default_selection else available[:3],
        label_visibility="collapsed"
    )

    st.divider()

    st.header("Temperature")
    t_lo, t_hi = st.slider(
        "Temperature range",
        min_value=int(np.floor(global_min)),
        max_value=int(np.ceil(global_max)),
        value=(int(np.floor(global_min)), min(1500, int(np.ceil(global_max)))),
        step=10,
        label_visibility="collapsed"
    )

    st.caption("Curves are shown only within their validated temperature ranges.")


# ============================================================
# MAIN HEADER
# ============================================================

st.caption("ENGINEERING MATERIALS")
st.title("Specific Heat Explorer")
st.markdown("Interactive Cₚ–T database for engineering materials.")


# ============================================================
# SUMMARY
# ============================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Materials", len(materials))

with c2:
    st.metric("Material classes", len(all_categories))

with c3:
    st.metric("Specific heat unit", "J kg⁻¹ K⁻¹")


# ============================================================
# EMPTY STATE
# ============================================================

if not chosen:
    st.info("Select one or more materials from the sidebar to explore Cp versus temperature.")
    st.stop()


# ============================================================
# WARNING
# ============================================================

flagged = []
for name in chosen:
    material = materials[name]
    if coverage_gap(material, t_lo, t_hi):
        flagged.append(f"{name} — validated range {material['tmin']:.0f}–{material['tmax']:.0f} K")

if flagged:
    st.warning(
        "Some selected materials extend outside their validated temperature range:\n\n"
        + "\n".join(f"• {item}" for item in flagged)
    )


# ============================================================
# CHART TITLE
# ============================================================

st.subheader("Cp vs Temperature")
st.caption("Specific heat capacity at constant pressure")
st.caption(f"{len(chosen)} materials  ·  {t_lo:.0f}–{t_hi:.0f} K  ·  J kg⁻¹ K⁻¹")


# ============================================================
# MAIN GRAPH
# ============================================================

fig = go.Figure()

chosen_colors = {}

for index, name in enumerate(chosen):
    color = MATERIAL_COLORS[index % len(MATERIAL_COLORS)]
    chosen_colors[name] = color
    temperature, capacity = material_curve(materials[name], t_lo, t_hi)
    if temperature.size == 0:
        continue
    fig.add_trace(
        go.Scatter(
            x=temperature,
            y=capacity,
            mode="lines",
            name=name,
            line=dict(color=color, width=2.8),
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
    margin=dict(l=80, r=35, t=25, b=70),
    font=dict(family="Arial, sans-serif", size=11, color="#2c3238"),
    hovermode="closest",
    legend=dict(
        bgcolor="rgba(246,247,248,0.96)",
        bordercolor="#9ca4ac",
        borderwidth=1,
        font=dict(size=10, color="#1a1c1e")
    ),
    xaxis=dict(
        title=dict(text="Temperature, T (K)", font=dict(size=12, color="#0a0c0e")),
        showline=True,
        mirror=True,
        linecolor="#7c858e",
        linewidth=1.3,
        ticks="outside",
        tickcolor="#7c858e",
        tickfont=dict(size=10, color="#2c3238"),
        gridcolor="#d9dde1",
        zeroline=False
    ),
    yaxis=dict(
        title=dict(text="Specific heat, Cp (J kg⁻¹ K⁻¹)", font=dict(size=12, color="#0a0c0e")),
        showline=True,
        mirror=True,
        linecolor="#7c858e",
        linewidth=1.3,
        ticks="outside",
        tickcolor="#7c858e",
        tickfont=dict(size=10, color="#2c3238"),
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
        "toImageButtonOptions": {"filename": "Cp_vs_T", "scale": 2}
    }
)

st.caption("Drag to zoom · double-click to reset · camera icon to export.")


# ============================================================
# TABS
# ============================================================

tab_compare, tab_materials, tab_rankings, tab_data = st.tabs(
    ["Compare", "Materials", "Rankings", "Data"]
)


# ============================================================
# COMPARE
# ============================================================

with tab_compare:
    st.subheader("Compare materials")
    st.caption("Compare specific heat at a selected temperature.")

    comparison_temperature = st.slider(
        "Comparison temperature (K)",
        int(t_lo),
        int(t_hi),
        value=min(max(298, int(t_lo)), int(t_hi)),
        step=5,
        key="comparison_temperature"
    )

    comparison_rows = []
    for name in chosen:
        value = cp_value(materials[name], comparison_temperature)
        if np.isfinite(value):
            comparison_rows.append({
                "name": name,
                "value": value,
                "color": chosen_colors.get(name, MATERIAL_COLORS[len(comparison_rows) % len(MATERIAL_COLORS)])
            })

    comparison_rows.sort(key=lambda row: row["value"], reverse=True)

    if comparison_rows:
        bar = go.Figure()

        for row in comparison_rows:
            bar.add_trace(
                go.Bar(
                    x=[row["value"]],
                    y=[row["name"]],
                    orientation="h",
                    marker=dict(color=row["color"], line=dict(color=row["color"], width=1)),
                    text=[f"{row['value']:.0f}"],
                    textposition="outside",
                    hovertemplate=(
                        "<b>" + row["name"] + "</b><br>"
                        "Cp = %{x:.1f} J kg⁻¹ K⁻¹"
                        "<extra></extra>"
                    ),
                    showlegend=False
                )
            )

        bar.update_layout(
            height=max(280, 70 * len(comparison_rows)),
            paper_bgcolor="#dfe2e5",
            plot_bgcolor="#f3f4f5",
            margin=dict(l=25, r=70, t=25, b=65),
            bargap=0.32,
            xaxis=dict(
                title=dict(
                    text=f"Specific heat at {comparison_temperature:.0f} K (J kg⁻¹ K⁻¹)",
                    font=dict(size=12, color="#0a0c0e")
                ),
                showline=True,
                mirror=True,
                linecolor="#7c858e",
                linewidth=1.3,
                gridcolor="#d9dde1",
                zeroline=False,
                tickfont=dict(size=10, color="#2c3238")
            ),
            yaxis=dict(
                autorange="reversed",
                showline=True,
                mirror=True,
                linecolor="#7c858e",
                linewidth=1.3,
                tickfont=dict(size=10, color="#0a0c0e")
            )
        )

        st.plotly_chart(bar, use_container_width=True, config={"displaylogo": False})


# ============================================================
# MATERIAL INFORMATION
# ============================================================

with tab_materials:
    st.subheader("Material information")
    st.caption("Properties and provenance for the selected materials.")

    information = []
    for name in chosen:
        material = materials[name]
        information.append({
            "Material": material["name"],
            "Formula": material["formula"],
            "Category": material["category"],
            "Valid T range (K)": f"{material['tmin']:.0f} – {material['tmax']:.0f}",
            "Cp @ 298 K": None if not np.isfinite(material["cp298"]) else round(material["cp298"], 1),
            "Molar mass": None if not np.isfinite(material["molar"]) else round(material["molar"], 3),
            "Density": None if not np.isfinite(material["density"]) else round(material["density"], 0),
            "Source": material["source"]
        })

    st.dataframe(pd.DataFrame(information), use_container_width=True, hide_index=True)


# ============================================================
# RANKINGS
# ============================================================

with tab_rankings:
    st.subheader("Material ranking")
    st.caption("Rank materials by specific heat at a selected temperature.")

    col1, col2 = st.columns(2)

    with col1:
        ranking_temperature = st.slider(
            "Ranking temperature (K)",
            int(global_min),
            int(global_max),
            value=min(max(298, int(global_min)), int(global_max)),
            step=5,
            key="ranking_temperature"
        )

    with col2:
        top_n = st.number_input(
            "Materials to show",
            min_value=5,
            max_value=50,
            value=15,
            step=5
        )

    ranking = rank_materials(materials, ranking_temperature)

    if ranking.empty:
        st.info("No materials are valid at this temperature.")
    else:
        ranking_order = st.radio(
            "Sort",
            ["Highest Cp", "Lowest Cp"],
            horizontal=True
        )

        if ranking_order == "Highest Cp":
            ranking_view = ranking.head(int(top_n))
        else:
            ranking_view = ranking.tail(int(top_n))

        ranking_fig = go.Figure()

        for _, row in ranking_view.iterrows():
            material_name = row["Material"]
            material_color = MATERIAL_COLORS[all_names.index(material_name) % len(MATERIAL_COLORS)]
            ranking_fig.add_trace(
                go.Bar(
                    x=[row["Cp (J/kg·K)"]],
                    y=[material_name],
                    orientation="h",
                    marker_color=material_color,
                    showlegend=False,
                    text=[f"{row['Cp (J/kg·K)']:.0f}"],
                    textposition="outside"
                )
            )

        ranking_fig.update_layout(
            height=max(350, 34 * len(ranking_view)),
            paper_bgcolor="#dfe2e5",
            plot_bgcolor="#f3f4f5",
            margin=dict(l=30, r=65, t=25, b=65),
            bargap=0.28,
            xaxis=dict(
                title=dict(
                    text=f"Specific heat at {ranking_temperature:.0f} K (J kg⁻¹ K⁻¹)",
                    font=dict(size=12, color="#0a0c0e")
                ),
                showline=True,
                mirror=True,
                linecolor="#7c858e",
                gridcolor="#d9dde1",
                zeroline=False,
                tickfont=dict(size=10, color="#2c3238")
            ),
            yaxis=dict(
                autorange="reversed",
                showline=True,
                mirror=True,
                linecolor="#7c858e",
                tickfont=dict(size=10, color="#0a0c0e")
            )
        )

        st.plotly_chart(ranking_fig, use_container_width=True, config={"displaylogo": False})


# ============================================================
# DATA EXPORT
# ============================================================

with tab_data:
    st.subheader("Computed data")
    st.caption("Sampled Cp–T values for the current selection.")

    frames = []
    for name in chosen:
        temperature, capacity = material_curve(materials[name], t_lo, t_hi)
        if temperature.size:
            frames.append(
                pd.DataFrame({
                    "Material": name,
                    "T (K)": temperature,
                    "Cp (J/kg·K)": capacity
                }).dropna()
            )

    if frames:
        output = pd.concat(frames, ignore_index=True)
        st.dataframe(output.head(500), use_container_width=True, hide_index=True)

        st.download_button(
            "Download curve data (CSV)",
            output.to_csv(index=False).encode("utf-8"),
            file_name="cp_vs_T_export.csv",
            mime="text/csv"
        )

        st.caption(f"{len(output):,} computed points.")
    else:
        st.info("Nothing to export for the current selection.")


# ============================================================
# FOOTER
# ============================================================

st.divider()
st.caption("Specific Heat Explorer · Thermodynamic data shown within validated temperature ranges.")
