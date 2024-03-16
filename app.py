import streamlit as st
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

float_init()

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]

initialize_session_state()

def format_emotional_context(ratings):
    context_parts = [f"{state}: {rating}/10" for state, rating in ratings.items()]
    context = "Emotional state ratings - " + ", ".join(context_parts)
    return context


if "test_message_added" not in st.session_state:
    st.session_state.messages.append({"role": "user", "content": "This is a test message to the bot. say hi"})
    st.session_state.test_message_added = True

col1, col2 = st.columns([1, 2])
with col1:
    st.image("logo.jpg", width=150)

with col2:
    st.markdown("# Free Your Mind")

if "emotional_ratings_submitted" not in st.session_state:
    st.session_state.emotional_ratings_submitted = False

if not st.session_state.emotional_ratings_submitted:
    emotional_states = ["Happiness", "Sadness", "Anger", "Fear", "Surprise"]
    user_emotional_ratings = {}
    with st.expander("Rate Your Emotional States"):
        for state in emotional_states:
            user_emotional_ratings[state] = st.slider(f"Rate your level of {state} from 0 to 10:", min_value=0, max_value=10, value=5, key=f"slider_{state}")

    if st.button("Submit Emotional Ratings", key="submit_emotions"):
        st.session_state.emotional_ratings_submitted = True
        emotional_context = format_emotional_context(user_emotional_ratings)
        st.session_state.emotional_context = emotional_context

footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if audio_bytes:
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        transcript = speech_to_text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)

if st.session_state.emotional_ratings_submitted:
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking🤔..."):
                final_response = get_answer(st.session_state.messages, st.session_state.emotional_context)
            with st.spinner("Generating audio response..."):
                audio_file = text_to_speech(final_response)
                autoplay_audio(audio_file)
            st.write(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})
            os.remove(audio_file)

footer_container.float("bottom: 0rem;")
