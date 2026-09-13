import streamlit as st
from database import add_confession

st.title("✍️ Submit a Confession")
st.caption("Your confession is displayed anonymously.")

st.info(
    "This is a placeholder project. For a production system, "
    "privacy, moderation, rate limiting, and security should be reviewed."
)

with st.form("confession_form"):
    confession = st.text_area(
        "Your confession",
        placeholder="Write something you'd like to share...",
        height=180,
        max_chars=2000,
    )

    submitted = st.form_submit_button(
        "Submit anonymously",
        use_container_width=True,
    )

if submitted:
    if not confession.strip():
        st.error("Please enter a confession.")
    else:
        # Placeholder IP value.
        # In production, obtain the client IP only if there is a valid
        # privacy/security reason and handle it according to your policy.
        success = add_confession(confession, ip_address="placeholder-client")

        if success:
            st.success("Your confession was submitted anonymously.")
            st.balloons()
        else:
            st.error("Something went wrong while submitting.")
