st.markdown(
    """
    <style>

    /* =========================================================
       GLOBAL BACKGROUND
    ========================================================= */

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {

        background: #e7e9ec !important;
        color: #555b63 !important;
    }

    .block-container {

        max-width: 1320px !important;

        padding-top: 1.45rem !important;
        padding-bottom: 3rem !important;
    }

    header[data-testid="stHeader"] {

        background: rgba(231,233,236,0.88) !important;

        backdrop-filter: blur(22px) saturate(140%) !important;

        -webkit-backdrop-filter:
            blur(22px) saturate(140%) !important;

        border-bottom:
            1px solid rgba(160,165,172,0.25) !important;
    }


    /* =========================================================
       MAIN TYPOGRAPHY
    ========================================================= */

    h1 {

        color: #4b5057 !important;

        font-size: 2.15rem !important;

        line-height: 1.15 !important;

        font-weight: 560 !important;

        letter-spacing: -0.04em !important;

        margin-bottom: 0.25rem !important;
    }

    h2 {

        color: #555b63 !important;

        font-size: 1.38rem !important;

        font-weight: 520 !important;

        letter-spacing: -0.02em !important;
    }

    h3 {

        color: #5c626a !important;

        font-size: 1.08rem !important;

        font-weight: 520 !important;
    }

    p {

        color: #737a83 !important;

        font-size: 0.86rem !important;

        font-weight: 400 !important;
    }

    [data-testid="stCaptionContainer"] {

        color: #858b93 !important;

        font-size: 0.74rem !important;

        font-weight: 400 !important;
    }


    /* =========================================================
       SIDEBAR — SOFT GRAY GLASS
    ========================================================= */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                145deg,
                rgba(239,241,243,0.94),
                rgba(224,227,231,0.92)
            ) !important;

        border-right:
            1px solid #c5c9ce !important;

        box-shadow:
            7px 0 25px rgba(0,0,0,0.035) !important;
    }

    section[data-testid="stSidebar"] > div:first-child {

        background: transparent !important;
    }

    section[data-testid="stSidebar"] h2 {

        color: #555b63 !important;

        font-size: 1.02rem !important;

        font-weight: 560 !important;
    }


    /* Sidebar small labels */

    section[data-testid="stSidebar"]
    [data-testid="stMarkdownContainer"] p {

        color: #7d848d !important;

        font-size: 0.65rem !important;

        font-weight: 520 !important;

        letter-spacing: 0.08em !important;

        text-transform: uppercase !important;
    }


    /* =========================================================
       SEARCH BAR — FROSTED GRAY GLASS
    ========================================================= */

    section[data-testid="stSidebar"]
    div[data-testid="stTextInput"] > div > div {

        background:
            rgba(245,246,247,0.62) !important;

        backdrop-filter:
            blur(20px) saturate(130%) !important;

        -webkit-backdrop-filter:
            blur(20px) saturate(130%) !important;

        border:
            1px solid rgba(255,255,255,0.78) !important;

        border-radius:
            12px !important;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.8),
            0 4px 14px rgba(0,0,0,0.045) !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stTextInput"] input {

        background: transparent !important;

        color: #626971 !important;

        border: none !important;

        font-size: 0.82rem !important;

        font-weight: 400 !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stTextInput"] input::placeholder {

        color: #9aa0a8 !important;
    }


    /* =========================================================
       MULTISELECT — MAIN BOX
    ========================================================= */

    section[data-testid="stSidebar"]
    div[data-testid="stMultiSelect"]
    div[data-baseweb="select"] > div {

        background:
            rgba(240,242,244,0.72) !important;

        background-color:
            rgba(240,242,244,0.72) !important;

        border:
            1px solid #bfc4ca !important;

        border-radius:
            11px !important;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.85),
            0 3px 12px rgba(0,0,0,0.035) !important;

        min-height:
            42px !important;
    }


    /* =========================================================
       SELECTED CHIPS — GRAY GLASS
    ========================================================= */

    section[data-testid="stSidebar"]
    div[data-testid="stMultiSelect"]
    [data-baseweb="tag"] {

        background:
            rgba(218,222,226,0.82) !important;

        background-color:
            rgba(218,222,226,0.82) !important;

        border:
            1px solid #c1c6cc !important;

        border-radius:
            8px !important;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.65),
            0 1px 4px rgba(0,0,0,0.04) !important;

        color:
            #626971 !important;

        margin:
            3px 3px 3px 0 !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stMultiSelect"]
    [data-baseweb="tag"] span {

        color:
            #5d646c !important;

        font-size:
            0.76rem !important;

        font-weight:
            450 !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stMultiSelect"]
    [data-baseweb="tag"] svg {

        color:
            #7c838b !important;

        width:
            12px !important;

        height:
            12px !important;
    }


    /* =========================================================
       IMPORTANT:
       FORCE DROPDOWN TO LIGHT GRAY
       THIS FIXES THE BLACK BOX IN YOUR SCREENSHOT
    ========================================================= */

    div[data-baseweb="popover"] {

        background:
            rgba(232,234,237,0.97) !important;

        background-color:
            #e8eaed !important;

        color:
            #5d646c !important;

        border:
            1px solid #c0c5cb !important;

        border-radius:
            12px !important;

        box-shadow:
            0 16px 40px rgba(0,0,0,0.16) !important;

        backdrop-filter:
            blur(22px) !important;

        -webkit-backdrop-filter:
            blur(22px) !important;
    }

    div[data-baseweb="popover"] * {

        color:
            #626971 !important;
    }

    div[data-baseweb="popover"] div[data-baseweb="menu"] {

        background:
            #e8eaed !important;

        background-color:
            #e8eaed !important;
    }

    div[data-baseweb="popover"] [role="option"] {

        background:
            transparent !important;

        color:
            #626971 !important;

        font-size:
            0.80rem !important;

        border-radius:
            8px !important;

        margin:
            2px 5px !important;
    }

    div[data-baseweb="popover"] [role="option"]:hover {

        background:
            #d9dde2 !important;

        color:
            #4f555d !important;
    }

    div[data-baseweb="popover"]
    [role="option"][aria-selected="true"] {

        background:
            #d4d9df !important;

        color:
            #4f555d !important;
    }


    /* =========================================================
       DROPDOWN SEARCH / INPUT
    ========================================================= */

    div[data-baseweb="popover"] input {

        background:
            #f0f1f3 !important;

        color:
            #555b63 !important;

        border:
            1px solid #c7cbd0 !important;

        border-radius:
            8px !important;
    }


    /* =========================================================
       SLIDER
    ========================================================= */

    section[data-testid="stSidebar"]
    [data-testid="stSlider"] [role="slider"] {

        background:
            #6f879e !important;

        border-color:
            #6f879e !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stSlider"] [data-baseweb="slider"] {

        color:
            #89939e !important;
    }


    /* =========================================================
       STAT CARDS — GRAY
    ========================================================= */

    div[data-testid="stMetric"] {

        background:
            rgba(239,241,243,0.70) !important;

        border:
            1px solid #d0d4d9 !important;

        border-radius:
            13px !important;

        padding:
            9px 14px !important;

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


    /* =========================================================
       WARNING — GRAY/YELLOW, NOT BRIGHT
    ========================================================= */

    div[data-testid="stAlert"] {

        background:
            #eeece3 !important;

        border:
            1px solid #d3cfbd !important;

        border-radius:
            11px !important;

        color:
            #716d5e !important;

        padding:
            0.65rem 0.85rem !important;

        box-shadow:
            0 2px 8px rgba(0,0,0,0.025) !important;
    }

    div[data-testid="stAlert"] p {

        color:
            #716d5e !important;

        font-size:
            0.76rem !important;

        font-weight:
            400 !important;
    }


    /* =========================================================
       CHART AREA
    ========================================================= */

    div[data-testid="stPlotlyChart"] {

        background:
            #e2e4e7 !important;

        border:
            1px solid #aeb4bb !important;

        border-radius:
            15px !important;

        padding:
            5px !important;

        box-shadow:
            0 4px 15px rgba(0,0,0,0.045) !important;
    }


    /* =========================================================
       TABS
    ========================================================= */

    button[data-baseweb="tab"] {

        color:
            #7a8189 !important;

        font-size:
            0.82rem !important;

        font-weight:
            450 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {

        color:
            #565d65 !important;

        font-weight:
            550 !important;
    }

    div[data-baseweb="tab-highlight"] {

        background:
            #71869a !important;
    }


    /* =========================================================
       TABLE
    ========================================================= */

    [data-testid="stDataFrame"] {

        background:
            #e2e4e7 !important;

        border:
            1px solid #b8bdc4 !important;

        border-radius:
            11px !important;

        overflow:
            hidden !important;
    }


    /* =========================================================
       DOWNLOAD BUTTON
    ========================================================= */

    .stDownloadButton button {

        background:
            #697987 !important;

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

    .stDownloadButton button:hover {

        background:
            #5e6d7a !important;
    }


    /* =========================================================
       DIVIDERS
    ========================================================= */

    hr {

        border-top:
            1px solid #c9cdd2 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)
