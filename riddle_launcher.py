import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from riddle.game import RiddleGame
from utils import (
    inject_css,
    pick_npc_avatar,
    render_title,
    render_stats,
    render_riddle,
    render_victory_banner,
    render_defeat_banner,
    PLAYER_AVATAR,
    DEFAULT_NPC_AVATAR,
)

# --- Page Config ---
st.set_page_config(
    page_title="The Riddle Chamber",
    page_icon="./imgs/crossed_swords.png",
    layout="centered",
)

inject_css()

# --- Session State ---
def init_game():
    st.session_state.game = RiddleGame()
    st.session_state.npc_avatar = pick_npc_avatar()

if "game" not in st.session_state:
    init_game()

game: RiddleGame = st.session_state.game
npc_avatar = st.session_state.get("npc_avatar") or DEFAULT_NPC_AVATAR

# --- Top Controls ---
btn_cols = st.columns([5, 1.2, 1.2])
with btn_cols[1]:
    if game.is_game_running() and st.button("Give Up"):
        game.give_up()
        st.rerun()
with btn_cols[2]:
    if st.button("New Game"):
        init_game()
        st.rerun()

# --- Layout ---
render_title()
render_stats(game.riddle.difficulty.value.capitalize(), game.turns, game.MAX_TURNS)
render_riddle(game.riddle.query)

# --- Chat History ---
for i in range(game.get_game_turns()):
    if i < len(game.guesses):
        with st.chat_message("user", avatar=PLAYER_AVATAR):
            st.markdown(game.guesses[i])
    if i < len(game.hints):
        with st.chat_message("assistant", avatar=npc_avatar):
            st.markdown(game.hints[i])

# --- Game End States ---
if not game.is_game_running():
    if game.get_game_state() == "ended_won":
        render_victory_banner()
    else:
        render_defeat_banner(game.riddle.answer)

# --- Chat Input ---
if game.is_game_running():
    if prompt := st.chat_input("Speak thy guess, adventurer..."):
        with st.chat_message("user", avatar=PLAYER_AVATAR):
            st.markdown(prompt)

        hint = game.add_user_guess(prompt)

        if hint is not None:
            with st.chat_message("assistant", avatar=npc_avatar):
                st.markdown(hint)
        elif game.get_game_state() == "ended_won":
            render_victory_banner()
        else:
            render_defeat_banner(game.riddle.answer)

        st.rerun()
