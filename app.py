import streamlit as st

# ---- APP PASSWORD ----
APP_PASSWORD = "admin123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    entered = st.text_input("Enter App Access Password", type="password")

    if entered == APP_PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.stop()

# ---- MAIN APP STARTS BELOW ----
import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage
import ssl
import time
import os

st.set_page_config(page_title="Pro Bulk Mailer", layout="wide")
st.title("📧 Professional Bulk Email Sender")

# -----------------------
# Sender Credentials
# -----------------------
st.sidebar.header("Sender Credentials")
sender_email = st.secrets["EMAIL"]
sender_password = st.secrets["PASSWORD"]

delay_seconds = st.sidebar.number_input("Delay Between Emails (seconds)", min_value=0.0, value=2.0)

max_retry = st.sidebar.number_input("Retry Failed Emails (Attempts)", min_value=0, value=1)

mode = st.radio(
    "Is attachment same for all users?",
    ("Yes - Same Attachment", "No - Different Attachment Per Email")
)

# -----------------------
# Template Download
# -----------------------
def generate_template(mode):
    if mode == "Yes - Same Attachment":
        return pd.DataFrame(columns=["To", "CC"])
    else:
        return pd.DataFrame(columns=["To", "CC", "Attachment"])

st.download_button(
    "Download CSV Template",
    generate_template(mode).to_csv(index=False),
    file_name="email_template.csv",
    mime="text/csv"
)

# -----------------------
# Upload CSV
# -----------------------
uploaded_file = st.file_uploader("Upload Filled CSV File", type=["csv"])

df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Email ID Preview")

    if "To" in df.columns:
        preview_df = df[["To", "CC"]] if "CC" in df.columns else df[["To"]]
        st.dataframe(preview_df)

# -----------------------
# Email Composition
# -----------------------
st.subheader("✉ Compose Email")

subject = st.text_input("Subject")

email_format = st.radio("Email Format", ("Plain Text", "HTML"))

body = st.text_area("Email Body", height=200)

if email_format == "HTML":
    st.subheader("🔎 HTML Preview")
    st.markdown(body, unsafe_allow_html=True)

# Attachment UI
attachment = None
if mode == "Yes - Same Attachment":
    attachment = st.file_uploader("Upload Attachment for All Users")

# -----------------------
# Email Sending Logic
# -----------------------
log_data = []

def send_email(row):
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["Subject"] = subject

    if email_format == "HTML":
        msg.add_alternative(body, subtype="html")
    else:
        msg.set_content(body)

    to_list = [x.strip() for x in str(row["To"]).split(";")]
    msg["To"] = ", ".join(to_list)

    recipients = to_list

    if "CC" in row and pd.notna(row["CC"]):
        cc_list = [x.strip() for x in str(row["CC"]).split(";")]
        msg["Cc"] = ", ".join(cc_list)
        recipients += cc_list

    # Same attachment
    if mode == "Yes - Same Attachment" and attachment:
        msg.add_attachment(
            attachment.read(),
            maintype="application",
            subtype="octet-stream",
            filename=attachment.name
        )

    # Different attachments
    if mode == "No - Different Attachment Per Email" and pd.notna(row.get("Attachment")):
        paths = str(row["Attachment"]).split(";")
        for path in paths:
            path = path.strip()
            if os.path.exists(path):
                with open(path, "rb") as f:
                    msg.add_attachment(
                        f.read(),
                        maintype="application",
                        subtype="octet-stream",
                        filename=os.path.basename(path)
                    )

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg, to_addrs=recipients)

# -----------------------
# Send Button
# -----------------------
if st.button("🚀 Send Emails"):

    if not sender_email or not sender_password:
        st.error("Enter sender credentials.")
    elif df is None:
        st.error("Upload CSV file.")
    else:
        total = len(df)
        progress_bar = st.progress(0)
        status_text = st.empty()

        sent = 0
        failed = 0

        for index, row in df.iterrows():

            attempt = 0
            success = False

            while attempt <= max_retry and not success:
                try:
                    send_email(row)
                    success = True
                except Exception as e:
                    attempt += 1
                    if attempt > max_retry:
                        failed += 1
                        log_data.append({
                            "To": row["To"],
                            "Status": "Failed",
                            "Error": str(e)
                        })

            if success:
                sent += 1
                log_data.append({
                    "To": row["To"],
                    "Status": "Sent",
                    "Error": ""
                })

            progress_bar.progress((index + 1) / total)
            status_text.text(f"Processing {index + 1} of {total}")

            time.sleep(delay_seconds)

        st.success(f"Sent: {sent} | Failed: {failed}")

        # -----------------------
        # Logging Dashboard
        # -----------------------
        st.subheader("📊 Sending Log Dashboard")

        log_df = pd.DataFrame(log_data)
        st.dataframe(log_df)

        st.download_button(
            "Download Log Report",
            log_df.to_csv(index=False),
            file_name="email_log.csv",
            mime="text/csv"
        )