import streamlit as st
import requests
from pathlib import Path

# ---------- CONFIG ----------
st.set_page_config(
    page_title="Emotional Wellbeing Assistant",
    page_icon="💛",
    layout="wide",
)

# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>
    body {
        background: radial-gradient(circle at top left, #ffdee9 0%, #b5fffc 35%, #1f2933 80%);
        color: #f9fafb;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }
    .main-card {
        background: rgba(15, 23, 42, 0.85);
        border-radius: 24px;
        padding: 2.5rem 2.2rem;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.25rem 0.9rem;
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.18);
        font-size: 0.8rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #e5e7eb;
    }
    .title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-top: 0.8rem;
        margin-bottom: 0.4rem;
    }
    .subtitle {
        color: #cbd5f5;
        font-size: 0.98rem;
    }
    .feature-card {
        background: rgba(15, 23, 42, 0.85);
        border-radius: 18px;
        padding: 1.2rem 1.1rem;
        border: 1px solid rgba(148, 163, 184, 0.35);
        font-size: 0.9rem;
    }
    .feature-title {
        font-weight: 600;
        margin-bottom: 0.15rem;
        font-size: 0.95rem;
    }
    .send-btn button {
        background: linear-gradient(135deg, #fb7185, #f97316);
        border-radius: 999px !important;
        border: none;
        color: white;
        font-weight: 600;
        padding: 0.4rem 1.5rem;
        box-shadow: 0 10px 30px rgba(248, 113, 113, 0.45);
    }
    .send-btn button:hover {
        filter: brightness(1.05);
        transform: translateY(-1px);
    }
    .response-card {
        margin-top: 1.5rem;
        padding: 1.4rem 1.2rem;
        border-radius: 18px;
        border: 1px solid rgba(129, 140, 248, 0.5);
        background: radial-gradient(circle at top left, rgba(129, 140, 248, 0.25), rgba(15,23,42,0.9));
    }
    .response-heading {
        font-size: 1.1rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin-bottom: 0.4rem;
    }
    .small-note {
        font-size: 0.78rem;
        color: #9ca3af;
        margin-top: 0.2rem;
    }
    .footer-note {
        font-size: 0.75rem;
        color: #9ca3af;
        margin-top: 1.8rem;
        text-align: center;
    }
    textarea {
        border-radius: 18px !important;
        border: 1px solid rgba(148, 163, 184, 0.6) !important;
        background-color: rgba(15, 23, 42, 0.65) !important;
        color: #f9fafb !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- LAYOUT ----------
assets_dir = Path(__file__).parent / "assets"
image_path = assets_dir / "calm.png"

col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    st.markdown(
        """
        <div class="main-card">
            <div class="pill">💛 Emotional Support · Private · Non-judgmental made by deepthi </div>
            <div class="title">Emotional Wellbeing Assistant</div>
            <div class="subtitle">
                I'm here to support your feelings. You can vent, reflect, or just put your thoughts into words —
                no need to be perfect.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_right:
    if image_path.exists():
        st.image(str(image_path), use_container_width=True)
    else:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">🌱 A gentle space for you</div>
                <div>Share what’s on your mind. I’ll help you name emotions, suggest small coping steps, 
                and offer reflection prompts.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("")

# Features row
fc1, fc2, fc3 = st.columns(3, gap="medium")
with fc1:
    st.markdown(
        '<div class="feature-card"><div class="feature-title">💬 Name your feelings</div>'
        'Tell me what’s happening, and I’ll try to gently reflect what you might be feeling.</div>',
        unsafe_allow_html=True,
    )
with fc2:
    st.markdown(
        '<div class="feature-card"><div class="feature-title">🧩 Tiny next steps</div>'
        'Get small, realistic coping ideas—not pressure, just possibilities.</div>',
        unsafe_allow_html=True,
    )
with fc3:
    st.markdown(
        '<div class="feature-card"><div class="feature-title">📓 Journaling prompts</div>'
        'If it feels right, I can offer prompts to help you process your thoughts.</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------- CHAT SECTION ----------
st.subheader("Your message:")

user_text = st.text_area(
    "",
    placeholder="You can start with something like: “I feel overwhelmed and I don’t know why.”",
    height=140,
)

col_send, _ = st.columns([1, 3])
with col_send:
    with st.container():
        st.markdown('<div class="send-btn">', unsafe_allow_html=True)
        send_clicked = st.button("Send")
        st.markdown("</div>", unsafe_allow_html=True)

if send_clicked:
    if not user_text.strip():
        st.warning("It’s okay to write just a few words. Try sharing even a tiny piece of what you feel.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"text": user_text},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            st.markdown(
                """
                <div class="response-card">
                    <div class="response-heading">🧠 Assistant Response</div>
                """,
                unsafe_allow_html=True,
            )
            st.write(data.get("response", "I'm here with you."))
            st.markdown(
                '<div class="small-note">This is supportive guidance, not a substitute for professional help.</div></div>',
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.error("Something went wrong while contacting the support agent.")
            st.caption(str(e))

st.markdown(
    """
    <div class="footer-note">
    ⚠️ This space is for gentle emotional support and reflection. It is not medical or crisis care.  
    If you feel unsafe or at risk of harm, please contact local emergency services or a crisis hotline in your area.
    </div>
    """,
    unsafe_allow_html=True,
)
