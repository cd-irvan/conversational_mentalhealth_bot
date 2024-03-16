from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
import streamlit as st
load_dotenv()
api_key = os.getenv("openai_api_key")

client = OpenAI(api_key=api_key)




def get_answer(messages, emotional_context):
    # Combine the emotional context with the initial system message
    system_message = {
        "role": "system",
        "content": f"{emotional_context} You are to act as a therapist to the user. You should ask open questions and emphasize active participation. The conversation should be goal-orientated and have a focus. The conversation should be focused on the current problems and specific situations the user is finding distressing to them presently. You should try to teach the user to understand the therapeutic process, how their thoughts influence their emotions and behavior, and how to identify and evaluate their own thoughts and beliefs. Use the process of guided discovery by questioning thoughts and beliefs to evaluate thinking and adopt more realistic perspectives. The conversation should be structured with a clear start, middle, and end."
    }

    # Prepend the system message with the emotional context to the messages
    messages_with_context = [system_message] + messages

    # Make the API call with the updated messages
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages_with_context
    )

    # Return the text of the first choice
    return response.choices[0].message.content






# working
# def get_answer(messages):
#     system_message = [{"role": "system", "content": "You are to act as a therapist to the user. You should ask open questions and emphasize active participation. The conversation should be goal orientated and have a focus. The conversation should be focussed on the current problems and specific situations the user is finding distressing to them presently. You should try to teach the user to understand the therapeutic process, how their thoughts influence their emotions and behaviour and how to identify and evaluate their own thoughts and beliefs. Use the process of guided discovery by questioning thoughts and beliefs to evaluate thinking and adopt more realistic perspectives. The conversation should be structured with a clear start, middle and end."}]
#     messages = system_message + messages
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo-1106",
#         messages=messages
#     )
#     return response.choices[0].message.content


# def get_answer(messages, context_summary):
#     # Prepend the context to the conversation messages
#     context_message = {"role": "system", "content": context_summary}
#     messages_with_context = [context_message] + messages
    
#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=messages_with_context
#     )
    
#     return response.choices[0].message.content





def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True).t