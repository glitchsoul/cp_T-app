"""
Interactive Cp vs. T Database for Engineering Materials
=======================================================
A minimalist Streamlit dashboard for exploring the specific heat capacity at
constant pressure (Cp) of engineering materials as a function of temperature (T).

Cp is evaluated from a temperature polynomial fitted to reliable thermodynamic
data:

        Cp(T) = a0 + a1*T + a2*T^2 + a3*T^3        [J / (kg * K)]

Each fit is valid only within the [T_min, T_max] window listed for that data
row. Materials with several phases (e.g. Iron) are stored as several rows and
are stitched back together here into a single, continuous selection.

Run with:   streamlit run app.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# --------------------------------------------------------------------------- #
#  Configuration
# --------------------------------------------------------------------------- #
DATA_FILE = Path(__file__).parent / "materials.csv"

# Column layout of materials.csv (renamed positionally so the app is robust to
# the unicode characters in the original header, e.g. "Cp @298K (J/kg·K)").
COLS = [
    "idx", "name", "formula", "category", "cas", "tmin", "tmax",
    "A", "B", "C", "D", "E", "a0", "a1", "a2", "a3", "r2",
    "cp298", "molar", "density", "source", "notes",
]
NUMERIC = ["tmin", "tmax", "a0", "a1", "a2", "a3", "cp298", "molar", "density"]

# Clean, distinguishable palette for overlaid curves (light-theme friendly).
PALETTE = [
    "#2563EB", "#DC2626", "#059669", "#D97706", "#7C3AED", "#0891B2",
    "#DB2777", "#65A30D", "#4B5563", "#B45309", "#0EA5E9", "#9333EA",
    "#16A34A", "#E11D48", "#7C2D12", "#1E40AF",
]

# Physically plausible band for specific heat (J/kg*K). Anything outside is a
# sign the polynomial is being pushed past where it is meaningful (this happens
# for the narrow Curie-transition segment of iron), so we hide those points
# rather than let one bad fit distort the whole chart.
CP_LO, CP_HI = 0.0, 20000.0


# --------------------------------------------------------------------------- #
#  Data loading & physics (pure functions — no Streamlit calls in here)
# --------------------------------------------------------------------------- #
def build_materials(df: pd.DataFrame) -> dict:
    """Group data rows into materials keyed by name, each with T-segments."""
    materials: dict = {}
    for _, r in df.iterrows():
        name = str(r["name"]).strip()
        seg = {
            "tmin": r["tmin"], "tmax": r["tmax"],
            "a0": r["a0"], "a1": r["a1"], "a2": r["a2"], "a3": r["a3"],
            "notes": str(r["notes"]).strip(),
        }
        if not (np.isfinite(seg["tmin"]) and np.isfinite(seg["tmax"])):
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
        m["segments"].sort(key=lambda s: s["tmin"])
        m["tmin"] = min(s["tmin"] for s in m["segments"])
        m["tmax"] = max(s["tmax"] for s in m["segments"])
    return materials


def load_materials(path: Path = DATA_FILE) -> dict:
    """Read and clean materials.csv, returning the grouped material dict."""
    df = pd.read_csv(path)
    if len(df.columns) != len(COLS):
        raise ValueError(
            f"Expected {len(COLS)} columns in materials.csv, found {len(df.columns)}."
        )
    df.columns = COLS
    for c in NUMERIC:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return build_materials(df)


def cp_poly(seg: dict, T):
    """Specific heat from the cubic polynomial fit [J/(kg*K)]. Accepts scalars or arrays."""
    T = np.asarray(T, dtype=float)
    return seg["a0"] + seg["a1"] * T + seg["a2"] * T ** 2 + seg["a3"] * T ** 3


def cp_value(material: dict, T: float) -> float:
    """Cp of a material at a single temperature, or NaN if T is out of range/unphysical."""
    for seg in material["segments"]:
        if seg["tmin"] <= T <= seg["tmax"]:
            v = float(cp_poly(seg, T))
            return v if (np.isfinite(v) and CP_LO < v < CP_HI) else np.nan
    return np.nan


def material_curve(material: dict, t_lo: float, t_hi: float, n: int = 400):
    """
    Sample Cp(T) for a material across the requested window.

    Returns (T_array, Cp_array) as one continuous trace. Gaps between phase
    segments (and any unphysical points) are inserted as NaN so the plotted
    line breaks cleanly instead of drawing a false connection.
    """
    span = max(t_hi - t_lo, 1e-9)
    xs, ys = [], []
    for seg in material["segments"]:
        lo = max(seg["tmin"], t_lo)
        hi = min(seg["tmax"], t_hi)
        if hi <= lo:
            continue
        pts = max(2, int(round(n * (hi - lo) / span)))
        T = np.linspace(lo, hi, pts)
        C = cp_poly(seg, T)
        C = np.where(np.isfinite(C) & (C > CP_LO) & (C < CP_HI), C, np.nan)
        xs.append(T)
        ys.append(C)
        xs.append(np.array([np.nan]))   # break the line between segments
        ys.append(np.array([np.nan]))
    if not xs:
        return np.array([]), np.array([])
    return np.concatenate(xs), np.concatenate(ys)


def coverage_gap(material: dict, t_lo: float, t_hi: float) -> bool:
    """True if the requested window extends beyond the material's valid range."""
    return t_lo < material["tmin"] - 1e-9 or t_hi > material["tmax"] + 1e-9


def rank_materials(materials: dict, T: float) -> pd.DataFrame:
    """Cp of every material valid at temperature T, sorted high -> low."""
    rows = []
    for m in materials.values():
        v = cp_value(m, T)
        if np.isfinite(v):
            rows.append({
                "Material": m["name"], "Formula": m["formula"],
                "Category": m["category"], "Cp (J/kg·K)": round(v, 1),
            })
    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.sort_values("Cp (J/kg·K)", ascending=False).reset_index(drop=True)
        out.index += 1
    return out


# --------------------------------------------------------------------------- #
#  Streamlit UI
# --------------------------------------------------------------------------- #
CUSTOM_CSS = """
<style>
    .block-container {padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1250px;}
    h1, h2, h3 {letter-spacing: -0.01em;}
    /* app title */
    .app-title {font-size: 1.9rem; font-weight: 700; color: #0f172a; margin-bottom: 0.1rem;}
    .app-sub  {color: #64748b; font-size: 0.95rem; margin-bottom: 0.4rem;}
    /* metric-style summary cards */
    div[data-testid="stMetric"] {
        background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;
        padding: 0.8rem 1rem;
    }
    section[data-testid="stSidebar"] {background: #F8FAFC !important; border-right: 1px solid #E2E8F0;}
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] div {color: #1e293b !important;}
    .stTabs [data-baseweb="tab-list"] {gap: 6px;}
    .stTabs [data-baseweb="tab"] {border-radius: 8px 8px 0 0;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
"""

ACCENT = "#2563EB"


def styled_figure(fig: go.Figure, height: int = 520) -> go.Figure:
    """Apply the clean, minimalist chart theme with high-contrast text."""
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=70, r=25, t=30, b=60),
        font=dict(family="Inter, Segoe UI, sans-serif", size=13, color="#1e293b"),
        hovermode="closest",
        legend=dict(
            orientation="v", yanchor="top", y=1, xanchor="left", x=1.02,
            bgcolor="rgba(255,255,255,0.9)", font=dict(size=12, color="#1e293b"),
        ),
        plot_bgcolor="white", paper_bgcolor="white",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E2E8F0", zeroline=False,
                     linecolor="#64748b", ticks="outside", tickcolor="#64748b",
                     tickfont=dict(color="#1e293b", size=12), title_font=dict(color="#1e293b", size=13))
    fig.update_yaxes(showgrid=True, gridcolor="#E2E8F0", zeroline=False,
                     linecolor="#64748b", ticks="outside", tickcolor="#64748b",
                     tickfont=dict(color="#1e293b", size=12), title_font=dict(color="#1e293b", size=13))
    return fig


def main() -> None:
    st.set_page_config(
        page_title="Cp–T Materials Database",
        page_icon="🔥",
        layout="wide",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    try:
        materials = load_materials()
    except Exception as exc:  # pragma: no cover - defensive UI guard
        st.error(f"Could not load materials.csv — {exc}")
        st.stop()

    names_all = sorted(materials.keys())
    cats_all = sorted({m["category"] for m in materials.values()})
    g_lo = min(m["tmin"] for m in materials.values())
    g_hi = max(m["tmax"] for m in materials.values())

    # ---- Header -------------------------------------------------------------
    st.markdown('<div class="app-title">Specific Heat Explorer</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="app-sub">Interactive C<sub>p</sub> vs. temperature database '
        f'&nbsp;·&nbsp; {len(materials)} materials across {len(cats_all)} classes '
        '&nbsp;·&nbsp; C<sub>p</sub> in J&nbsp;kg⁻¹&nbsp;K⁻¹</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    # ---- Sidebar controls ---------------------------------------------------
    with st.sidebar:
        st.subheader("🔎 Find materials")
        query = st.text_input("Search by name or formula",
                              placeholder="e.g. copper, Al2O3, nylon…").strip().lower()
        cats = st.multiselect("Categories", cats_all, default=cats_all)

        def visible(name: str) -> bool:
            m = materials[name]
            if m["category"] not in cats:
                return False
            if query and query not in name.lower() and query not in m["formula"].lower():
                return False
            return True

        options = [n for n in names_all if visible(n)]

        st.caption(f"{len(options)} of {len(names_all)} materials match")

        defaults = [n for n in ["Aluminium", "Copper", "Alumina (Al₂O₃)",
                                 "Polyethylene HDPE — solid"] if n in options]
        chosen = st.multiselect(
            "Materials to plot", options,
            default=defaults or options[:3],
            help="Select one or several materials to overlay and compare.",
        )

        st.subheader("🌡️ Temperature window")
        t_lo, t_hi = st.slider(
            "Range (K)",
            min_value=int(np.floor(g_lo)), max_value=int(np.ceil(g_hi)),
            value=(int(np.floor(g_lo)), 1500 if g_hi > 1500 else int(np.ceil(g_hi))),
            step=10,
        )
        if t_hi <= t_lo:                 # guard: both handles dragged together
            t_hi = min(t_lo + 10, int(np.ceil(g_hi)))
            t_lo = t_hi - 10
        st.caption("Curves are drawn only where each material's fit is valid.")

    if not chosen:
        st.info("👈 Use the sidebar to search for and select one or more materials "
                "to plot their specific-heat curves.")
        st.stop()

    # ---- Out-of-range warnings ---------------------------------------------
    flagged = [(materials[n]["name"], materials[n]["tmin"], materials[n]["tmax"])
               for n in chosen if coverage_gap(materials[n], t_lo, t_hi)]
    if flagged:
        msg = "  \n".join(
            f"• **{nm}** is only valid for **{lo:.0f}–{hi:.0f} K** — "
            f"the curve is clipped to that range."
            for nm, lo, hi in flagged
        )
        st.warning("Part of your temperature window is outside the validated data "
                   "range for some materials:  \n" + msg, icon="⚠️")

    # ---- Main Cp–T comparison chart ----------------------------------------
    fig = go.Figure()
    for i, n in enumerate(chosen):
        m = materials[n]
        T, C = material_curve(m, t_lo, t_hi)
        if T.size == 0:
            continue
        color = PALETTE[i % len(PALETTE)]
        fig.add_trace(go.Scatter(
            x=T, y=C, mode="lines", name=n,
            line=dict(color=color, width=2.5), connectgaps=False,
            hovertemplate=(f"<b>{n}</b><br>T = %{{x:.0f}} K"
                           "<br>Cp = %{y:.1f} J/kg·K<extra></extra>"),
        ))
    fig.update_layout(
        xaxis_title="Temperature, T (K)",
        yaxis_title="Specific heat, C<sub>p</sub> (J kg⁻¹ K⁻¹)",
    )
    st.plotly_chart(styled_figure(fig), use_container_width=True,
                    config={"displaylogo": False,
                            "toImageButtonOptions": {"filename": "Cp_vs_T",
                                                     "scale": 2}})
    st.caption("Tip: drag to zoom, double-click to reset, and use the 📷 icon "
               "(top-right of the chart) to download it as a PNG.")

    # ---- Detail tabs --------------------------------------------------------
    tab_cmp, tab_info, tab_rank, tab_data = st.tabs(
        ["⚖️  Compare at a temperature", "📋  Material details",
         "🏆  Rankings", "⬇️  Export data"]
    )

    # Compare at a single temperature -> bar chart
    with tab_cmp:
        Tc = st.slider("Comparison temperature (K)", t_lo, t_hi,
                       value=min(max(298, t_lo), t_hi), step=5, key="cmpT")
        rows, missing = [], []
        for n in chosen:
            v = cp_value(materials[n], Tc)
            if np.isfinite(v):
                rows.append((n, v))
            else:
                missing.append(n)
        if rows:
            rows.sort(key=lambda x: x[1], reverse=True)
            labels = [r[0] for r in rows]
            vals = [r[1] for r in rows]
            bar = go.Figure(go.Bar(
                x=vals, y=labels, orientation="h",
                marker_color=ACCENT,
                text=[f"{v:.0f}" for v in vals], textposition="outside",
                hovertemplate="<b>%{y}</b><br>Cp = %{x:.1f} J/kg·K<extra></extra>",
            ))
            bar.update_layout(
                xaxis_title=f"Specific heat at {Tc:.0f} K  (J kg⁻¹ K⁻¹)",
                yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(styled_figure(bar, height=max(240, 60 * len(rows))),
                            use_container_width=True,
                            config={"displaylogo": False})
        else:
            st.info("None of the selected materials are valid at this temperature.")
        if missing:
            st.caption("⚠️ Not valid at "
                       f"{Tc:.0f} K (excluded): {', '.join(missing)}")

    # Material property summary
    with tab_info:
        recs = []
        for n in chosen:
            m = materials[n]
            recs.append({
                "Material": m["name"],
                "Formula": m["formula"],
                "Category": m["category"],
                "Valid T range (K)": f"{m['tmin']:.0f} – {m['tmax']:.0f}",
                "Cp @298 K (J/kg·K)": (None if not np.isfinite(m["cp298"])
                                       else round(m["cp298"], 1)),
                "Molar mass (g/mol)": (None if not np.isfinite(m["molar"])
                                       else round(m["molar"], 3)),
                "Density (kg/m³)": (None if not np.isfinite(m["density"])
                                    else round(m["density"], 0)),
                "Phase / notes": m["segments"][0]["notes"],
                "Data source": m["source"],
            })
        st.dataframe(pd.DataFrame(recs), use_container_width=True, hide_index=True)
        st.caption("Every value is traceable to the cited thermodynamic source.")

    # Rankings across the whole database
    with tab_rank:
        c1, c2 = st.columns([1, 1])
        with c1:
            Tr = st.slider("Rank all materials at (K)", int(g_lo), int(g_hi),
                           value=298, step=5, key="rankT")
        with c2:
            topn = st.number_input("How many to show", 5, 50, 15, step=5)
        rk = rank_materials(materials, Tr)
        if rk.empty:
            st.info("No materials are valid at this temperature.")
        else:
            order = st.radio("Show", ["Highest Cp", "Lowest Cp"],
                             horizontal=True, key="rankorder")
            view = rk.head(int(topn)) if order == "Highest Cp" else rk.tail(int(topn))
            fig_r = go.Figure(go.Bar(
                x=view["Cp (J/kg·K)"], y=view["Material"], orientation="h",
                marker_color=ACCENT,
                hovertemplate="<b>%{y}</b><br>Cp = %{x:.1f} J/kg·K<extra></extra>",
            ))
            fig_r.update_layout(
                xaxis_title=f"Specific heat at {Tr:.0f} K (J kg⁻¹ K⁻¹)",
                yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(styled_figure(fig_r, height=max(300, 28 * len(view))),
                            use_container_width=True, config={"displaylogo": False})
            st.caption(f"{len(rk)} materials have a valid fit at {Tr:.0f} K.")

    # Export the sampled curves
    with tab_data:
        frames = []
        for n in chosen:
            T, C = material_curve(materials[n], t_lo, t_hi)
            if T.size:
                frames.append(pd.DataFrame({"Material": n, "T (K)": T,
                                            "Cp (J/kg·K)": C}).dropna())
        if frames:
            out = pd.concat(frames, ignore_index=True)
            st.dataframe(out.head(500), use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️  Download curve data (CSV)",
                out.to_csv(index=False).encode("utf-8"),
                file_name="cp_vs_T_export.csv", mime="text/csv",
            )
            st.caption(f"{len(out):,} computed points across {len(frames)} materials. "
                       "The graph itself can be saved as PNG with the 📷 button.")
        else:
            st.info("Nothing to export for the current selection.")


if __name__ == "__main__":
    main()
