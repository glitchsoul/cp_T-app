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
    "cp298", "molar", "density", "source", "notes",
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
ACCENT = "#0071E3"


# ============================================================
# PREMIUM LIGHT UI
# ============================================================

CUSTOM_CSS = """
<style>

:root {
    --bg: #f3f4f6;
    --surface: #ffffff;
    --surface2: #f8f9fb;
    --text: #202124;
    --muted: #6b7280;
    --soft: #8b919b;
    --line: #d8dbe0;
    --line-dark: #b9bec7;
    --blue: #0071e3;
    --blue-soft: #edf5ff;
}

/* PAGE */

html, body {
    background: #f3f4f6 !important;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
.main {
    background: #f3f4f6 !important;
    color: #202124 !important;
}

.block-container {
    max-width: 1380px !important;
    padding-top: 2.2rem !important;
    padding-bottom: 4rem !important;
}

#MainMenu,
footer {
    visibility: hidden !important;
}

header[data-testid="stHeader"] {
    background: rgba(243,244,246,0.94) !important;
}


/* TYPOGRAPHY */

html, body, .stApp, p, span, label, div, button, input,
textarea, select {
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "SF Pro Text",
        "SF Pro Display",
        "Inter",
        "Segoe UI",
        sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #202124 !important;
}

p, .stCaption, small {
    color: #6b7280 !important;
}


/* HEADER */

.app-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 30px;
    margin-bottom: 1.7rem;
}

.eyebrow {
    color: #0071e3;
    font-size: 0.72rem;
    font-weight: 650;
    letter-spacing: 0.12em;
    margin-bottom: 0.45rem;
}

.app-title {
    color: #202124;
    font-size: clamp(2.35rem, 4vw, 3.35rem);
    line-height: 1;
    font-weight: 680;
    letter-spacing: -0.055em;
}

.app-sub {
    margin-top: 0.65rem;
    color: #6b7280;
    font-size: 1rem;
    font-weight: 400;
}

.header-meta {
    text-align: right;
    color: #7a808a;
    font-size: 0.82rem;
    line-height: 1.6;
}

.header-meta strong {
    color: #202124;
    font-weight: 600;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #d8dbe0 !important;
}

section[data-testid="stSidebar"] > div:first-child {
    background: #ffffff !important;
}

section[data-testid="stSidebar"] * {
    color: #202124 !important;
}

.sidebar-heading {
    color: #202124 !important;
    font-size: 1.05rem;
    font-weight: 650;
    margin-bottom: 1rem;
}

.sidebar-label {
    color: #858b95 !important;
    font-size: 0.69rem;
    font-weight: 650;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 1.25rem;
    margin-bottom: 0.5rem;
}


/* INPUTS */

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background: #f8f9fb !important;
    color: #202124 !important;
    border: 1px solid #cdd1d7 !important;
    border-radius: 11px !important;
    min-height: 42px !important;
    box-shadow: none !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: #0071e3 !important;
    box-shadow: 0 0 0 3px rgba(0,113,227,0.11) !important;
}


/* SELECT / MULTISELECT */

div[data-baseweb="select"] > div {
    background: #f8f9fb !important;
    color: #202124 !important;
    border: 1px solid #cdd1d7 !important;
    border-radius: 11px !important;
    min-height: 42px;
    box-shadow: none !important;
}

/* Selected chips */

div[data-baseweb="tag"] {
    background: #edf5ff !important;
    border: 1px solid #cfe3fb !important;
    border-radius: 8px !important;
    padding: 3px 7px !important;
}

div[data-baseweb="tag"] span {
    color: #075ca8 !important;
    font-weight: 500 !important;
}

div[data-baseweb="tag"] svg {
    color: #4f83b5 !important;
}


/* BUTTONS */

button[kind="primary"],
.stDownloadButton button {
    background: #0071e3 !important;
    color: white !important;
    border: 0 !important;
    border-radius: 10px !important;
    font-weight: 550 !important;
}

button[kind="primary"]:hover,
.stDownloadButton button:hover {
    background: #0067cf !important;
}

button[kind="secondary"] {
    background: white !important;
    color: #202124 !important;
    border: 1px solid #d1d4d9 !important;
    border-radius: 10px !important;
}


/* SLIDER */

.stSlider [role="slider"] {
    background: #0071e3 !important;
    border-color: #0071e3 !important;
    box-shadow: none !important;
}


/* DIVIDER */

hr {
    border: 0 !important;
    border-top: 1px solid #dfe1e5 !important;
    margin: 1.3rem 0 !important;
}


/* WARNING */

.range-note {
    background: #fff8e7;
    border: 1px solid #ead8a5;
    border-radius: 12px;
    padding: 11px 15px;
    color: #755900;
    font-size: 0.82rem;
    line-height: 1.6;
    margin: 0.8rem 0 1rem;
}

.range-note strong {
    color: #604900;
    font-weight: 600;
}


/* CHART HEADER */

.chart-shell {
    background: #ffffff;
    border: 1px solid #c8ccd2;
    border-radius: 18px;
    padding: 1.25rem 1.3rem 0.8rem;
    box-shadow:
        0 5px 18px rgba(0,0,0,0.035),
        0 1px 2px rgba(0,0,0,0.025);
}

.chart-title {
    color: #202124;
    font-size: 1.22rem;
    font-weight: 620;
    letter-spacing: -0.025em;
}

.chart-subtitle {
    color: #707782;
    font-size: 0.84rem;
    margin-top: 0.22rem;
}

.context-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 0.85rem;
}

.context-pill {
    color: #626872;
    background: #f5f6f8;
    border: 1px solid #e0e2e6;
    border-radius: 9px;
    padding: 5px 10px;
    font-size: 0.75rem;
    font-weight: 500;
}

.context-pill.unit {
    color: #37658f;
    background: #f0f6fc;
    border-color: #d5e5f5;
}


/* CHART FRAME */

.chart-frame {
    background: #ffffff;
    border: 1px solid #bfc4cb;
    border-radius: 0 0 18px 18px;
    border-top: 0;
    padding: 0.25rem 0.35rem 0.2rem;
    margin-bottom: 1.2rem;
}


/* TABS */

.stTabs [data-baseweb="tab-list"] {
    gap: 3px;
    border-bottom: 1px solid #d5d8dd;
}

.stTabs [data-baseweb="tab"] {
    color: #707782 !important;
    font-weight: 500 !important;
    padding: 0.7rem 1rem !important;
}

.stTabs [aria-selected="true"] {
    color: #202124 !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background: #0071e3 !important;
}


/* TABLE */

div[data-testid="stDataFrame"] {
    border: 1px solid #cfd3d9 !important;
    border-radius: 13px !important;
    overflow: hidden !important;
}


/* INFO CARD */

.info-card {
    background: #ffffff;
    border: 1px solid #d8dbe0;
    border-radius: 15px;
    padding: 17px 19px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.025);
}

.info-title {
    color: #202124;
    font-size: 0.96rem;
    font-weight: 600;
}

.info-text {
    color: #707782;
    font-size: 0.83rem;
    line-height: 1.55;
    margin-top: 4px;
}


/* RESPONSIVE */

@media (max-width: 800px) {
    .app-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .header-meta {
        text-align: left;
    }

    .app-title {
        font-size: 2.25rem;
    }
}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


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
                "formula": str(r["formula"]).strip(),
                "category": str(r["category"]).strip(),
                "cas": str(r["cas"]).strip(),
                "cp298": r["cp298"],
                "molar": r["molar"],
                "density": r["density"],
                "source": str(r["source"]).strip(),
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


@st.cache_data
def load_materials(path=DATA_FILE):

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


def cp_poly(seg, T):

    T = np.asarray(T, dtype=float)

    return (
        seg["a0"]
        + seg["a1"] * T
        + seg["a2"] * T**2
        + seg["a3"] * T**3
    )


def cp_value(material, T):

    for seg in material["segments"]:

        if seg["tmin"] <= T <= seg["tmax"]:

            value = float(
                cp_poly(seg, T)
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

        xs.append(np.array([np.nan]))
        ys.append(np.array([np.nan]))

    if not xs:
        return np.array([]), np.array([])

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
        t_lo < material["tmin"] - 1e-9
        or
        t_hi > material["tmax"] + 1e-9
    )


def rank_materials(
    materials,
    T
):

    rows = []

    for m in materials.values():

        value = cp_value(
            m,
            T
        )

        if np.isfinite(value):

            rows.append({
                "Material": m["name"],
                "Formula": m["formula"],
                "Category": m["category"],
                "Cp (J/kg·K)": round(
                    value,
                    1
                ),
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
# PLOT STYLE
# ============================================================

def styled_figure(
    fig,
    height=520
):

    fig.update_layout(

        template="plotly_white",

        height=height,

        margin=dict(
            l=78,
            r=40,
            t=35,
            b=72
        ),

        font=dict(
            family=(
                "-apple-system, "
                "BlinkMacSystemFont, "
                "Inter, Segoe UI, sans-serif"
            ),
            size=12,
            color="#4f5560"
        ),

        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",

        hovermode="closest",

        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.015,
            bgcolor="rgba(255,255,255,0.96)",
            bordercolor="#c9cdd3",
            borderwidth=1,
            font=dict(
                size=11,
                color="#4f5560"
            ),
        ),

        hoverlabel=dict(
            bgcolor="#202124",
            bordercolor="#202124",
            font=dict(
                color="#ffffff",
                size=12
            )
        )
    )

    fig.update_xaxes(

        showgrid=True,

        gridcolor="#eceef1",

        gridwidth=1,

        zeroline=False,

        showline=True,

        mirror=True,

        linecolor="#aeb3ba",

        linewidth=1.2,

        ticks="outside",

        tickcolor="#9298a1",

        tickwidth=1,

        tickfont=dict(
            color="#727985",
            size=11
        ),

        title_font=dict(
            color="#42464d",
            size=13
        )
    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor="#eceef1",

        gridwidth=1,

        zeroline=False,

        showline=True,

        mirror=True,

        linecolor="#aeb3ba",

        linewidth=1.2,

        ticks="outside",

        tickcolor="#9298a1",

        tickwidth=1,

        tickfont=dict(
            color="#727985",
            size=11
        ),

        title_font=dict(
            color="#42464d",
            size=13
        )
    )

    return fig


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # LOAD DATABASE
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
        """
        <div class="app-header">

            <div>

                <div class="eyebrow">
                    ENGINEERING MATERIALS
                </div>

                <div class="app-title">
                    Specific Heat Explorer
                </div>

                <div class="app-sub">
                    Interactive C<sub>p</sub>–T database
                    for engineering materials
                </div>

            </div>

            <div class="header-meta">
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
                <strong>{len(materials)} materials</strong><br>
                {len(cats_all)} material classes ·
                J kg⁻¹ K⁻¹
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    with st.sidebar:

        st.markdown(
            '<div class="sidebar-heading">'
            'Materials'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sidebar-label">Search</div>',
            unsafe_allow_html=True
        )

        query = st.text_input(
            "Search",
            placeholder="Material or formula...",
            label_visibility="collapsed"
        ).strip().lower()

        st.markdown(
            '<div class="sidebar-label">'
            'Material class'
            '</div>',
            unsafe_allow_html=True
        )

        cats = st.multiselect(
            "Material classes",
            cats_all,
            default=cats_all,
            label_visibility="collapsed"
        )

        def visible(name):

            material = materials[name]

            if material["category"] not in cats:
                return False

            if query:

                if (
                    query not in name.lower()
                    and
                    query not in material["formula"].lower()
                ):
                    return False

            return True

        options = [
            name
            for name in names_all
            if visible(name)
        ]

        st.caption(
            f"{len(options)} of {len(names_all)} materials"
        )

        st.markdown(
            '<div class="sidebar-label">'
            'Selected materials'
            '</div>',
            unsafe_allow_html=True
        )

        defaults = [
            name
            for name in [
                "Aluminium",
                "Copper",
                "Alumina (Al₂O₃)",
                "Polyethylene HDPE — solid"
            ]
            if name in options
        ]

        chosen = st.multiselect(
            "Selected materials",
            options,
            default=defaults or options[:3],
            help="Select materials to compare.",
            label_visibility="collapsed"
        )

        st.markdown(
            '<div class="sidebar-label">'
            'Temperature range'
            '</div>',
            unsafe_allow_html=True
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
                int(np.floor(g_lo)),
                1500 if g_hi > 1500
                else int(np.ceil(g_hi))
            ),

            step=10,

            label_visibility="collapsed"
        )

        st.caption(
            "Curves are shown only within "
            "their validated ranges."
        )

    # --------------------------------------------------------
    # EMPTY STATE
    # --------------------------------------------------------

    if not chosen:

        st.markdown(
            """
            <div class="chart-shell"
                 style="
                 text-align:center;
                 padding:5rem 1.5rem;
                 margin-top:1rem;
                 ">

                <div class="chart-title">
                    Select a material
                </div>

                <div class="chart-subtitle">
                    Choose one or more materials to explore
                    specific heat versus temperature.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.stop()

    # --------------------------------------------------------
    # WARNING
    # --------------------------------------------------------

    flagged = [

        (
            materials[name]["name"],
            materials[name]["tmin"],
            materials[name]["tmax"]
        )

        for name in chosen

        if coverage_gap(
            materials[name],
            t_lo,
            t_hi
        )
    ]

    if flagged:

        msg = "<br>".join(

            f"• <strong>{name}</strong> — "
            f"validated range {lo:.0f}–{hi:.0f} K"

            for name, lo, hi in flagged
        )

        st.markdown(
            f"""
            <div class="range-note">

                <strong>⚠ Validated range notice</strong><br>

                {msg}

            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # MAIN CHART HEADER
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="chart-shell">

            <div class="chart-title">
                Cp vs Temperature
            </div>

            <div class="chart-subtitle">
                Specific heat capacity at constant pressure
            </div>

            <div class="context-row">

                <span class="context-pill">
                    {len(chosen)} materials
                </span>

                <span class="context-pill">
                    {t_lo:.0f}–{t_hi:.0f} K
                </span>

                <span class="context-pill unit">
                    J kg⁻¹ K⁻¹
                </span>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # MAIN GRAPH
    # --------------------------------------------------------

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

        color = PALETTE[
            i % len(PALETTE)
        ]

        fig.add_trace(

            go.Scatter(

                x=T,

                y=C,

                mode="lines",

                name=name,

                line=dict(
                    color=color,
                    width=2.7
                ),

                connectgaps=False,

                hovertemplate=(
                    f"<b>{name}</b><br>"
                    "Temperature = %{x:.0f} K<br>"
                    "Cp = %{y:.1f} J kg⁻¹ K⁻¹"
                    "<extra></extra>"
                )
            )
        )

    fig.update_layout(

        xaxis_title=(
            "Temperature, T "
            "<span style='color:#6f7782'>(K)</span>"
        ),

        yaxis_title=(
            "Specific heat, Cp "
            "<span style='color:#6f7782'>"
            "(J kg⁻¹ K⁻¹)"
            "</span>"
        )
    )

    st.markdown(
        '<div class="chart-frame">',
        unsafe_allow_html=True
    )

    st.plotly_chart(

        styled_figure(
            fig,
            height=550
        ),

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

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Drag to zoom · double-click to reset · "
        "use the camera icon to export the graph."
    )

    # --------------------------------------------------------
    # TABS
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
            "Compare specific heat at a selected temperature."
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
                x[0] for x in rows
            ]

            values = [
                x[1] for x in rows
            ]

            bar = go.Figure(

                go.Bar(

                    x=values,

                    y=labels,

                    orientation="h",

                    marker_color=ACCENT,

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
                xaxis_title=(
                    f"Specific heat at {Tc:.0f} K "
                    "(J kg⁻¹ K⁻¹)"
                ),
                yaxis=dict(
                    autorange="reversed"
                )
            )

            st.plotly_chart(
                styled_figure(
                    bar,
                    height=max(
                        280,
                        65 * len(rows)
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
    # MATERIAL INFORMATION
    # ========================================================

    with tab_info:

        st.markdown(
            "### Material information"
        )

        st.caption(
            "Properties and provenance for selected materials."
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

                "Cp @298 K (J/kg·K)":
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

                "Molar mass (g/mol)":
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

                "Density (kg/m³)":
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

                "Phase / notes":
                    material["segments"][0]["notes"],

                "Data source":
                    material["source"]
            })

        st.dataframe(
            pd.DataFrame(records),
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # RANKINGS
    # ========================================================

    with tab_rank:

        st.markdown(
            "### Material ranking"
        )

        st.caption(
            "Rank the database by specific heat "
            "at a selected temperature."
        )

        c1, c2 = st.columns(2)

        with c1:

            Tr = st.slider(

                "Temperature (K)",

                int(g_lo),
                int(g_hi),

                value=min(
                    max(298, int(g_lo)),
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

        ranking = rank_materials(
            materials,
            Tr
        )

        if ranking.empty:

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

                    marker_color=ACCENT,

                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Cp = %{x:.1f} J kg⁻¹ K⁻¹"
                        "<extra></extra>"
                    )
                )
            )

            ranking_fig.update_layout(

                xaxis_title=(
                    f"Specific heat at {Tr:.0f} K "
                    "(J kg⁻¹ K⁻¹)"
                ),

                yaxis=dict(
                    autorange="reversed"
                )
            )

            st.plotly_chart(

                styled_figure(
                    ranking_fig,
                    height=max(
                        340,
                        32 * len(view)
                    )
                ),

                use_container_width=True,

                config={
                    "displaylogo": False
                }
            )

            st.caption(
                f"{len(ranking)} materials have "
                f"a valid fit at {Tr:.0f} K."
            )

    # ========================================================
    # DATA
    # ========================================================

    with tab_data:

        st.markdown(
            "### Computed data"
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
                "Nothing to export for "
                "the current selection."
            )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#858b95;
            font-size:0.76rem;
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
