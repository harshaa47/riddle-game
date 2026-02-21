import base64
import random
import streamlit as st
from pathlib import Path


def load_css(path: str) -> str:
    return Path(path).read_text()


def get_base64_image(path: str) -> str | None:
    p = Path(path)
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None


def get_background_css(image_path: str) -> str:
    b64 = get_base64_image(image_path)
    if not b64:
        return ""
    return f"""
    .stApp {{
        background-image: url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(15, 10, 5, 0.75);
        z-index: 0;
        pointer-events: none;
    }}
    """


def pick_npc_avatar() -> str | None:
    npc_dir = Path("imgs/npcs")
    if npc_dir.exists():
        avatars = list(npc_dir.glob("*.png")) + list(npc_dir.glob("*.jpg")) + list(npc_dir.glob("*.jpeg"))
        if avatars:
            return str(random.choice(avatars))
    return None


def inject_css():
    css = load_css("static/style.css")
    bg_css = get_background_css("imgs/background.png")
    st.markdown(f"<style>{bg_css}\n{css}</style>", unsafe_allow_html=True)


# --- HTML Components ---

PLAYER_AVATAR = "https://em-content.zobj.net/source/twitter/376/person-fencing_1f93a.png"
DEFAULT_NPC_AVATAR = "https://em-content.zobj.net/source/twitter/376/mage_1f9d9.png"


def render_title():
    st.markdown(
        '<div class="medieval-title">The Riddle Chamber</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="medieval-subtitle">Prove thy wit, or be forever silenced...</div>',
        unsafe_allow_html=True,
    )


def render_stats(difficulty: str, turns: int, max_turns: int):
    st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-badge">
            <div class="stat-label">Difficulty</div>
            <div class="stat-value">{difficulty}</div>
        </div>
        <div class="stat-badge">
            <div class="stat-label">Turn</div>
            <div class="stat-value">{turns} / {max_turns}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_riddle(query: str):
    st.markdown(f"""
    <div class="riddle-scroll">
        <div class="riddle-text">{query}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="medieval-divider">- - -</div>', unsafe_allow_html=True)


def render_victory_banner():
    st.markdown("""
    <div class="result-banner result-won">
        <div class="result-title">Huzzah! Victory!</div>
        <div class="result-text">Thy wisdom has pierced the veil of mystery.</div>
    </div>
    """, unsafe_allow_html=True)


def render_defeat_banner(answer: str):
    st.markdown(f"""
    <div class="result-banner result-lost">
        <div class="result-title">Alas! Defeated...</div>
        <div class="result-text">The riddle proved too cunning this time.</div>
        <div class="result-answer">The answer was: {answer}</div>
    </div>
    """, unsafe_allow_html=True)
