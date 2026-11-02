import os
import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="ContentSpark AI", page_icon="📝", layout="wide")

# Initialize Groq Client
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = os.getenv("GROQ_API_KEY", "")

if not api_key:
    st.error("🚨 Groq API Key not found! Please configure it in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# UI Header
st.title("📝 ContentSpark AI Studio")
st.markdown("Instantly generate SEO strategies, blog outlines, and multi-platform social media campaigns using **Groq**.")

# Sidebar Inputs
with st.sidebar:
    st.header("1. Campaign Details")
    topic = st.text_input("Core Topic or Product", "AI automation for small businesses")
    target_audience = st.text_input("Target Audience", "Founders and startup operators")
    
    tone = st.selectbox(
        "Brand Tone",
        ["Professional & Authoritative", "Casual & Engaging", "Bold & Provocative", "Educational"]
    )
    
    # Updated to Groq's available open-weight OpenAI models
    model_choice = st.selectbox(
        "Choose Groq Model",
        ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]
    )

# Main Dashboard Tabs
tab1, tab2, tab3 = st.tabs(["📊 SEO & Blog Outline", "🚀 Social Media Campaign", "💬 Content Assistant"])

# --- TAB 1: SEO & Blog Outline ---
with tab1:
    st.subheader("SEO Strategy & Blog Outline")
    if st.button("Generate SEO & Outline"):
        if not topic.strip():
            st.warning("Please enter a core topic in the sidebar.")
        else:
            with st.spinner("Generating SEO blueprint..."):
                prompt = f"""
                Create an SEO and blog outline for the topic: '{topic}' targeting '{target_audience}'. Tone: {tone}.
                
                Provide:
                1. 3 Catchy SEO Meta Titles
                2. SEO Meta Description (under 160 characters)
                3. Primary and Secondary Keywords
                4. Comprehensive Blog Post Outline with H2 and H3 headings.
                """
                try:
                    response = client.chat.completions.create(
                        model=model_choice,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.5
                    )
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Groq API Error: {e}")

# --- TAB 2: Social Media Campaign ---
with tab2:
    st.subheader("Multi-Platform Social Pack")
    if st.button("Generate Social Content"):
        if not topic.strip():
            st.warning("Please enter a core topic in the sidebar.")
        else:
            with st.spinner("Crafting social media posts..."):
                prompt = f"""
                Create a cross-platform social media campaign based on the topic: '{topic}' for audience '{target_audience}'. Tone: {tone}.
                
                Provide:
                1. **LinkedIn Post:** Engaging, professional hook with actionable takeaways and hashtags.
                2. **Twitter/X Thread:** A 4-part sequential thread breaking down the core concepts.
                3. **Instagram/Facebook Caption:** Short, punchy caption with a clear Call-to-Action (CTA).
                """
                try:
                    response = client.chat.completions.create(
                        model=model_choice,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7
                    )
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Groq API Error: {e}")

# --- TAB 3: Content Assistant ---
with tab3:
    st.subheader("Refine & Expand Content")
    
    if "content_messages" not in st.session_state:
        st.session_state.content_messages = []

    # Display chat history
    for message in st.session_state.content_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Ask for modifications, tone changes, or extra sections..."):
        st.session_state.content_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Thinking..."):
            system_prompt = f"You are an expert copywriter helping craft content about '{topic}' for '{target_audience}' with a '{tone}' tone."
            messages = [{"role": "system", "content": system_prompt}] + st.session_state.content_messages
            
            try:
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=messages,
                    temperature=0.6
                )
                ai_response = response.choices[0].message.content
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                st.session_state.content_messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Groq API Error: {e}")
