import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai_key"])

def ask_openai(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Or "gpt-4" if available
            messages=messages,
            max_tokens=500,
            temperature=1.0,
            top_p=1.0,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"
