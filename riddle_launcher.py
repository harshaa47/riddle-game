import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from riddle.game import RiddleGame



st.title("Riddle Game")

if "game" not in st.session_state:
    st.session_state.game = RiddleGame()

col1, col2 = st.columns(2)
col1.metric("Difficulty", st.session_state.game.riddle.difficulty.value.capitalize())
col2.metric("Turn", f"{st.session_state.game.turns} / {st.session_state.game.MAX_TURNS}")

with st.chat_message('system'):
    st.markdown(f"Riddle Query: {st.session_state.game.riddle.query}")

for i in range(st.session_state.game.get_game_turns()):
    if i < len(st.session_state.game.guesses):
        with st.chat_message('user'):
            st.markdown(f"{st.session_state.game.guesses[i]}")
    if i < len(st.session_state.game.hints):
        with st.chat_message('assistant'):
            st.markdown(f"{st.session_state.game.hints[i]}")

if not st.session_state.game.is_game_running():
    if st.session_state.game.get_game_state() == 'ended_won':
        st.markdown("Congratulations! You guessed it right!")
    else:
        st.markdown(f"Game Over! The answer was {st.session_state.game.riddle.answer}")

if prompt := st.chat_input('Guess what?'):
    with st.chat_message('user'):
        st.markdown(prompt)
    hint = st.session_state.game.add_user_guess(prompt)

    if hint is not None:
        with st.chat_message('assistant'):
            st.markdown(hint)
    else:
        if st.session_state.game.get_game_state() == 'ended_won':
            st.markdown("Congratulations! You guessed it right!")
        else:
            st.markdown(f"Game Over! The answer was {st.session_state.game.riddle.answer}")
    st.rerun()
