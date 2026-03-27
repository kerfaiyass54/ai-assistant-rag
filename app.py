# app.py — Streamlit frontend for the RAG assistant

import streamlit as st

from chain.chain import build_chain, query
from config.config import APP_TITLE, APP_SUBTITLE, OLLAMA_MODEL

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RAG Assistant",
    page_icon="🔍",
    layout="centered",
)

# ── Custom styling ────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    /* Dark terminal background */
    .stApp {
        background-color: #0d0f12;
        color: #e2e8f0;
    }

    /* Title */
    .rag-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.8rem;
        font-weight: 600;
        color: #38bdf8;
        letter-spacing: -0.5px;
        margin-bottom: 0;
    }

    .rag-subtitle {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
        color: #475569;
        margin-top: 4px;
        margin-bottom: 28px;
    }

    /* Chat bubbles */
    .bubble-user {
        background: #1e293b;
        border-left: 3px solid #38bdf8;
        border-radius: 6px;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 0.93rem;
        color: #cbd5e1;
    }

    .bubble-bot {
        background: #111827;
        border-left: 3px solid #34d399;
        border-radius: 6px;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 0.93rem;
        color: #d1fae5;
        white-space: pre-wrap;
    }

    .label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 4px;
        color: #64748b;
    }

    /* Input box */
    .stTextInput > div > div > input {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
        color: #e2e8f0 !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.92rem !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #0ea5e9 !important;
        color: #0d0f12 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.45rem 1.2rem !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        background-color: #38bdf8 !important;
    }

    /* Divider */
    hr {
        border-color: #1e293b;
        margin: 20px 0;
    }

    /* Spinner text */
    .stSpinner > div {
        color: #38bdf8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f'<div class="rag-title">{APP_TITLE}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="rag-subtitle">{APP_SUBTITLE} &nbsp;·&nbsp; model: {OLLAMA_MODEL}</div>', unsafe_allow_html=True)
st.markdown("---")

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []   # list of {"role": "user"|"bot", "text": str}

if "chain" not in st.session_state:
    with st.spinner("Loading model…"):
        st.session_state.chain = build_chain()

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown('<div class="label">You</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bubble-user">{msg["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="label">Assistant</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bubble-bot">{msg["text"]}</div>', unsafe_allow_html=True)

# ── Input area ────────────────────────────────────────────────────────────────
st.markdown("---")
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        label="question",
        placeholder="Ask anything — I'll search the web in real time…",
        label_visibility="collapsed",
        key="user_input",
    )

with col2:
    send = st.button("Send →")

# ── Handle send ───────────────────────────────────────────────────────────────
if send and user_input.strip():
    question = user_input.strip()

    # Store user message
    st.session_state.messages.append({"role": "user", "text": question})

    # Run the RAG chain
    with st.spinner("🔍 Searching & thinking…"):
        try:
            answer = query(st.session_state.chain, question)
        except Exception as e:
            answer = f"⚠️ Error: {e}"

    # Store bot reply
    st.session_state.messages.append({"role": "bot", "text": answer})

    # Rerun to refresh the chat display
    st.rerun()

# ── Clear button ──────────────────────────────────────────────────────────────
if st.session_state.messages:
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()