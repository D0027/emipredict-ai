import streamlit as st

CUSTOM_CSS = """
<style>
    /* ---- Global ---- */
    html, body, [class*="css"] { font-family: 'Segoe UI', 'Inter', sans-serif; }

    /* Hide default Streamlit chrome for a cleaner app feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* ---- Header banner ---- */
    .epai-header {
        background: linear-gradient(120deg, #123B36 0%, #0E1117 70%);
        border: 1px solid #21332F;
        border-radius: 14px;
        padding: 1.6rem 2rem;
        margin-bottom: 1.4rem;
    }
    .epai-header h1 {
        margin: 0;
        font-size: 1.9rem;
        color: #F1F5F3;
        font-weight: 700;
    }
    .epai-header p {
        margin: 0.35rem 0 0 0;
        color: #9FB3AD;
        font-size: 0.95rem;
    }

    /* ---- KPI Cards ---- */
    .kpi-card {
        background: #161B22;
        border: 1px solid #262E36;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        text-align: left;
        transition: border-color 0.2s ease;
    }
    .kpi-card:hover { border-color: #3EC6A8; }
    .kpi-label {
        color: #8B96A5;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.35rem;
    }
    .kpi-value {
        color: #F1F5F3;
        font-size: 1.7rem;
        font-weight: 700;
        line-height: 1.1;
    }
    .kpi-sub {
        color: #6E7A87;
        font-size: 0.78rem;
        margin-top: 0.25rem;
    }

    /* ---- Verdict badges ---- */
    .badge {
        display: inline-block;
        padding: 0.28rem 0.75rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-eligible { background: rgba(62,198,168,0.15); color: #3EC6A8; border: 1px solid #3EC6A8; }
    .badge-highrisk { background: rgba(246,174,45,0.15); color: #F6AE2D; border: 1px solid #F6AE2D; }
    .badge-noteligible { background: rgba(230,57,70,0.15); color: #E63946; border: 1px solid #E63946; }
    .badge-pass { background: rgba(62,198,168,0.15); color: #3EC6A8; border: 1px solid #3EC6A8; }
    .badge-fail { background: rgba(230,57,70,0.15); color: #E63946; border: 1px solid #E63946; }

    /* ---- Section titles ---- */
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F1F5F3;
        margin: 1.2rem 0 0.4rem 0;
        border-left: 4px solid #3EC6A8;
        padding-left: 0.6rem;
    }

    /* ---- Result panel ---- */
    .result-panel {
        background: #161B22;
        border: 1px solid #262E36;
        border-radius: 14px;
        padding: 1.5rem;
    }

    div[data-testid="stMetricValue"] { color: #3EC6A8; }
        /* ---- Sidebar Navigation (Advanced) ---- */
    section[data-testid="stSidebar"] {
        background: #0E1117;
        border-right: 1px solid #21332F;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    /* Nav links container */
    div[data-testid="stSidebarNav"] ul {
        padding: 0 0.5rem;
    }

    /* Individual nav item */
    div[data-testid="stSidebarNav"] li {
        margin-bottom: 0.25rem;
    }

    div[data-testid="stSidebarNav"] a {
        display: flex;
        align-items: center;
        border-radius: 10px;
        padding: 0.55rem 0.9rem;
        color: #9FB3AD;
        font-size: 0.92rem;
        font-weight: 500;
        transition: all 0.18s ease;
        border: 1px solid transparent;
    }

    div[data-testid="stSidebarNav"] a:hover {
        background: rgba(62,198,168,0.08);
        color: #F1F5F3;
        border-color: #21332F;
        transform: translateX(2px);
    }

    /* Active/selected page */
    div[data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(90deg, rgba(62,198,168,0.16) 0%, rgba(62,198,168,0.04) 100%);
        color: #3EC6A8;
        font-weight: 700;
        border: 1px solid rgba(62,198,168,0.35);
        box-shadow: inset 3px 0 0 #3EC6A8;
    }

    div[data-testid="stSidebarNav"] span {
        color: inherit;
    }



        /* ---- ULTRA PRO MAX Background — EMI Predict AI ---- */
    .stApp {
        background: #0B0F14;
    }

    /* Layer 1: neural dot grid */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        background-image:
            radial-gradient(circle, rgba(62,198,168,0.55) 1.3px, transparent 1.3px),
            radial-gradient(circle, rgba(62,198,168,0.35) 1.3px, transparent 1.3px),
            radial-gradient(circle, rgba(246,174,45,0.25) 1px, transparent 1px);
        background-size: 140px 140px, 190px 190px, 95px 95px;
        background-position: 0 0, 70px 100px, 40px 20px;
        animation: nodesFloat 22s ease-in-out infinite;
        mask-image: radial-gradient(ellipse 85% 60% at 50% 0%, transparent 25%, #000 100%);
        -webkit-mask-image: radial-gradient(ellipse 85% 60% at 50% 0%, transparent 25%, #000 100%);
    }

    /* Layer 2: corner glows */
    .stApp::after {
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        background:
            radial-gradient(ellipse 36% 26% at 4% 96%, rgba(62,198,168,0.12) 0%, transparent 70%),
            radial-gradient(ellipse 30% 24% at 97% 4%, rgba(18,59,54,0.45) 0%, transparent 70%);
        animation: glowPulse 12s ease-in-out infinite;
    }

    @keyframes nodesFloat {
        0%, 100% { background-position: 0 0, 70px 100px, 40px 20px; }
        50%      { background-position: 25px 35px, 40px 70px, 65px 50px; }
    }

    @keyframes glowPulse {
        0%, 100% { opacity: 0.55; transform: scale(1); }
        50%      { opacity: 1; transform: scale(1.08); }
    }

    /* Layer 3: floating rupee marks — small, scattered, drifting */
    .epai-rupee {
        position: fixed;
        z-index: 0;
        pointer-events: none;
        user-select: none;
        color: rgba(62,198,168,0.07);
        font-weight: 800;
        line-height: 1;
    }
    .epai-rupee.r1 { top: 12%;  left: 8%;  font-size: 3.2rem; animation: rupeeFloat1 14s ease-in-out infinite; }
    .epai-rupee.r2 { top: 65%;  left: 88%; font-size: 4rem;   color: rgba(246,174,45,0.06); animation: rupeeFloat2 18s ease-in-out infinite; }
    .epai-rupee.r3 { top: 80%;  left: 15%; font-size: 2.4rem; animation: rupeeFloat3 16s ease-in-out infinite; }
    .epai-rupee.r4 { top: 25%;  left: 92%; font-size: 2.8rem; animation: rupeeFloat1 20s ease-in-out infinite reverse; }
    .epai-rupee.r5 { top: 48%;  left: 3%;  font-size: 2rem;   color: rgba(246,174,45,0.05); animation: rupeeFloat2 15s ease-in-out infinite; }

    @keyframes rupeeFloat1 {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50%      { transform: translateY(-25px) rotate(8deg); }
    }
    @keyframes rupeeFloat2 {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50%      { transform: translateY(20px) rotate(-6deg); }
    }
    @keyframes rupeeFloat3 {
        0%, 100% { transform: translate(0,0) rotate(0deg); }
        50%      { transform: translate(15px,-15px) rotate(5deg); }
    }

    /* Layer 4: subtle horizontal AI-scan line */
    .epai-scanline {
        position: fixed;
        left: 0; right: 0;
        height: 2px;
        z-index: 0;
        pointer-events: none;
        background: linear-gradient(90deg, transparent 0%, rgba(62,198,168,0.35) 50%, transparent 100%);
        animation: scanMove 7s linear infinite;
    }

    @keyframes scanMove {
        0%   { top: -5%; opacity: 0; }
        10%  { opacity: 1; }
        90%  { opacity: 1; }
        100% { top: 105%; opacity: 0; }
    }

    /* ---- Layer: Rain Drops with Road Splash ---- */
    .epai-rain {
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
    }

    .epai-rain .drop {
        position: absolute;
        top: -10%;
        width: 2px;
        height: 70px;
        background: linear-gradient(180deg, transparent 0%, rgba(62,198,168,0.65) 60%, rgba(62,198,168,0.9) 100%);
        animation: rainFall linear infinite;
    }

    .epai-rain .road {
        position: absolute;
        left: 0; right: 0; bottom: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent 0%, rgba(62,198,168,0.35) 50%, transparent 100%);
        box-shadow: 0 0 12px rgba(62,198,168,0.25);
    }

    .epai-rain .splash {
        position: absolute;
        bottom: 1px;
        width: 10px;
        height: 10px;
        border: 1.5px solid rgba(62,198,168,0.6);
        border-radius: 50%;
        transform: translateX(-50%) scale(0);
        animation: splashRipple linear infinite;
    }

    .epai-rain .drop:nth-child(2)  { left: 4%;  height: 55px; animation-duration: 2.6s; animation-delay: 0s; }
    .epai-rain .drop:nth-child(3)  { left: 11%; height: 80px; animation-duration: 3.3s; animation-delay: 0.5s; }
    .epai-rain .drop:nth-child(4)  { left: 18%; height: 45px; animation-duration: 2.2s; animation-delay: 1s; }
    .epai-rain .drop:nth-child(5)  { left: 25%; height: 70px; animation-duration: 2.9s; animation-delay: 0.2s; }
    .epai-rain .drop:nth-child(6)  { left: 33%; height: 58px; animation-duration: 3.1s; animation-delay: 1.4s; }
    .epai-rain .drop:nth-child(7)  { left: 41%; height: 50px; animation-duration: 2.5s; animation-delay: 0.7s; }
    .epai-rain .drop:nth-child(8)  { left: 49%; height: 85px; animation-duration: 3.5s; animation-delay: 0.1s; }
    .epai-rain .drop:nth-child(9)  { left: 57%; height: 55px; animation-duration: 2.7s; animation-delay: 1.2s; }
    .epai-rain .drop:nth-child(10) { left: 65%; height: 65px; animation-duration: 3.0s; animation-delay: 0.6s; }
    .epai-rain .drop:nth-child(11) { left: 73%; height: 75px; animation-duration: 3.4s; animation-delay: 1.7s; }
    .epai-rain .drop:nth-child(12) { left: 81%; height: 48px; animation-duration: 2.3s; animation-delay: 0.3s; }
    .epai-rain .drop:nth-child(13) { left: 89%; height: 62px; animation-duration: 2.8s; animation-delay: 0.9s; }
    .epai-rain .drop:nth-child(14) { left: 96%; height: 58px; animation-duration: 3.1s; animation-delay: 1.3s; }
    .epai-rain .drop:nth-child(15) { left: 8%;  height: 46px; animation-duration: 2.4s; animation-delay: 1.9s; }
    .epai-rain .drop:nth-child(16) { left: 60%; height: 52px; animation-duration: 2.6s; animation-delay: 2.1s; }

    .epai-rain .splash:nth-child(17) { left: 4%;  animation-duration: 2.6s; animation-delay: 0s; }
    .epai-rain .splash:nth-child(18) { left: 11%; animation-duration: 3.3s; animation-delay: 0.5s; }
    .epai-rain .splash:nth-child(19) { left: 18%; animation-duration: 2.2s; animation-delay: 1s; }
    .epai-rain .splash:nth-child(20) { left: 25%; animation-duration: 2.9s; animation-delay: 0.2s; }
    .epai-rain .splash:nth-child(21) { left: 33%; animation-duration: 3.1s; animation-delay: 1.4s; }
    .epai-rain .splash:nth-child(22) { left: 41%; animation-duration: 2.5s; animation-delay: 0.7s; }
    .epai-rain .splash:nth-child(23) { left: 49%; animation-duration: 3.5s; animation-delay: 0.1s; }
    .epai-rain .splash:nth-child(24) { left: 57%; animation-duration: 2.7s; animation-delay: 1.2s; }
    .epai-rain .splash:nth-child(25) { left: 65%; animation-duration: 3.0s; animation-delay: 0.6s; }
    .epai-rain .splash:nth-child(26) { left: 73%; animation-duration: 3.4s; animation-delay: 1.7s; }
    .epai-rain .splash:nth-child(27) { left: 81%; animation-duration: 2.3s; animation-delay: 0.3s; }
    .epai-rain .splash:nth-child(28) { left: 89%; animation-duration: 2.8s; animation-delay: 0.9s; }
    .epai-rain .splash:nth-child(29) { left: 96%; animation-duration: 3.1s; animation-delay: 1.3s; }
    .epai-rain .splash:nth-child(30) { left: 8%;  animation-duration: 2.4s; animation-delay: 1.9s; }
    .epai-rain .splash:nth-child(31) { left: 60%; animation-duration: 2.6s; animation-delay: 2.1s; }

    @keyframes rainFall {
        0%   { transform: translateY(0); opacity: 0; }
        8%   { opacity: 0.9; }
        88%  { opacity: 0.9; }
        92%  { transform: translateY(100vh); opacity: 0; }
        100% { transform: translateY(100vh); opacity: 0; }
    }

    @keyframes splashRipple {
        0%, 89%  { transform: translateX(-50%) scale(0); opacity: 0; }
        90%      { transform: translateX(-50%) scale(0.3); opacity: 0.8; }
        100%     { transform: translateX(-50%) scale(1.4); opacity: 0; }
    }

        /* ---- Nav Cards (Home page navigation) ---- */
    .nav-card {
        background: linear-gradient(145deg, #161B22 0%, #12161C 100%);
        border: 1px solid #262E36;
        border-radius: 14px;
        padding: 1.3rem 1.4rem;
        height: 100%;
        transition: all 0.25s ease;
        cursor: default;
    }
    .nav-card:hover {
        border-color: #3EC6A8;
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(62,198,168,0.15);
    }
    .nav-card .nav-icon {
        font-size: 1.6rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    .nav-card .nav-title {
        color: #F1F5F3;
        font-size: 1.02rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    .nav-card .nav-desc {
        color: #8B96A5;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    /* ---- Problem/Solution Panels ---- */
    .info-panel {
        background: #161B22;
        border: 1px solid #262E36;
        border-left: 3px solid #3EC6A8;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        height: 100%;
    }
    .info-panel h4 {
        color: #3EC6A8;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin: 0 0 0.6rem 0;
    }
    .info-panel p, .info-panel li {
        color: #C7D0D6;
        font-size: 0.92rem;
        line-height: 1.6;
    }
    .info-panel ul {
        margin: 0.4rem 0 0.8rem 0;
        padding-left: 1.1rem;
    }


        /* ---- Data Exploration: tabs + dataframe theming ---- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #12161C;
        padding: 0.35rem;
        border-radius: 10px;
        border: 1px solid #21332F;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #8B96A5;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(62,198,168,0.15) !important;
        color: #3EC6A8 !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #262E36;
        border-radius: 10px;
        overflow: hidden;
    }

    /* ---- Small info strip (record count) ---- */
    .data-strip {
        display: inline-block;
        background: rgba(62,198,168,0.08);
        border: 1px solid rgba(62,198,168,0.25);
        color: #3EC6A8;
        padding: 0.4rem 0.9rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }


        /* ---- Prediction Engine: form section styling ---- */
    div[data-testid="stForm"] {
        background: #12161C;
        border: 1px solid #21332F;
        border-radius: 16px;
        padding: 1.8rem 1.8rem 1rem 1.8rem;
    }

    /* Bold "section" markdown lines inside the form act like sub-headers */
    div[data-testid="stForm"] p strong {
        color: #3EC6A8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: inline-block;
        margin: 1.1rem 0 0.6rem 0;
        border-bottom: 1px solid #21332F;
        padding-bottom: 0.4rem;
        width: 100%;
    }

    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(120deg, #3EC6A8 0%, #2A9D8F 100%);
        color: #0B0F14;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 0;
        transition: all 0.2s ease;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(62,198,168,0.35);
    }

    /* ---- Prediction Result panel ---- */
    .predict-result-card {
        background: #161B22;
        border: 1px solid #262E36;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        height: 100%;
    }
    .predict-result-card .result-label {
        color: #8B96A5;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }

    div[data-testid="stMetric"] {
        background: #161B22;
        border: 1px solid #262E36;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
    }


        /* ---- Model Performance: code block + mlflow panel ---- */
    div[data-testid="stCodeBlock"] {
        border: 1px solid #262E36;
        border-radius: 10px;
    }
    div[data-testid="stCodeBlock"] pre {
        background: #12161C !important;
    }


        /* ---- Data Management: delete confirmation panel ---- */
    .delete-preview {
        background: rgba(230,57,70,0.06);
        border: 1px solid rgba(230,57,70,0.3);
        border-radius: 12px;
        padding: 1rem 1.3rem;
        margin-bottom: 0.8rem;
        color: #C7D0D6;
        font-size: 0.95rem;
    }

    div[data-testid="stDownloadButton"] button {
        border: 1px solid #3EC6A8;
        color: #3EC6A8;
        background: transparent;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background: rgba(62,198,168,0.1);
    }


        /* ---- Experiment Log table ---- */
    .run-id-text {
        font-family: 'Consolas', monospace;
        font-size: 0.78rem;
        color: #6E7A87;
    }

</style>
"""


def inject_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="epai-rupee r1">₹</div>
        <div class="epai-rupee r2">₹</div>
        <div class="epai-rupee r3">₹</div>
        <div class="epai-rupee r4">₹</div>
        <div class="epai-rupee r5">₹</div>
        <div class="epai-scanline"></div>
        <div class="epai-rain">
            <div class="road"></div>
            <span class="drop"></span><span class="drop"></span><span class="drop"></span>
            <span class="drop"></span><span class="drop"></span><span class="drop"></span>
            <span class="drop"></span><span class="drop"></span><span class="drop"></span>
            <span class="drop"></span><span class="drop"></span><span class="drop"></span>
            <span class="drop"></span><span class="drop"></span><span class="drop"></span>
            <span class="splash"></span><span class="splash"></span><span class="splash"></span>
            <span class="splash"></span><span class="splash"></span><span class="splash"></span>
            <span class="splash"></span><span class="splash"></span><span class="splash"></span>
            <span class="splash"></span><span class="splash"></span><span class="splash"></span>
            <span class="splash"></span><span class="splash"></span><span class="splash"></span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def header(title: str, subtitle: str):
    st.markdown(
        f"""<div class="epai-header"><h1>{title}</h1><p>{subtitle}</p></div>""",
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, sub: str = ""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def eligibility_badge(label: str) -> str:
    cls = {
        "Eligible": "badge-eligible",
        "High_Risk": "badge-highrisk",
        "Not_Eligible": "badge-noteligible",
    }.get(label, "badge-highrisk")
    return f'<span class="badge {cls}">{label.replace("_", " ")}</span>'


def pass_fail_badge(passed: bool, text: str) -> str:
    cls = "badge-pass" if passed else "badge-fail"
    return f'<span class="badge {cls}">{text}</span>'
