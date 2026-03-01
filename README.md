\# 📧 Bulk Mailer App



This is a \*\*Streamlit-based bulk email sender\*\* app that allows users to:



\- Upload a CSV list of email addresses

\- Compose email subject and body (plain text or HTML)

\- Send emails with optional attachments

\- Preview email list before sending

\- Control send delay to avoid spam limits

\- View send progress and logs



---



\## 🔗 Live App



👉 Hosted at: https://bulk-mailer-app.streamlit.app/



This app is publicly accessible and can be used to send emails.



---



\## 🛠 Features



✔ Upload email list as CSV  

✔ Multiple `To` and `CC` fields with `;` separator  

✔ Support for HTML email content  

✔ Optional attachments  

✔ Delay control to avoid spam limits  

✔ Progress bar during send  

✔ Logging dashboard with download option



---



\## 📄 CSV Templates



\### \*\*Same Attachment for All\*\*



Download the template from the UI — contains:



| To | CC |

|----|----|

| user1@example.com;user2@example.com | cc1@example.com |



---



\### \*\*Different Attachment Per Email\*\*



Download the template from the UI — contains:



| To | CC | Attachment |

|----|----|------------|

| user@example.com | cc@example.com | path/to/file1.pdf;path/to/file2.pdf |



Note: The attachment file paths must be valid paths accessible to the server.



---



\## ▶️ How to Use



1\. Go to the app URL

2\. Upload your filled CSV

3\. Enter email subject

4\. Enter email body (plain text or HTML)

5\. Upload attachment (if same for all)

6\. Set delay (optional)

7\. Click \*\*Send Emails\*\*



You will see a progress bar and a log dashboard.



---



\## 🧪 Sample HTML Email Body



You can write HTML content directly in the body field:



```html

<h2>Monthly Update</h2>

<p>Dear customer,</p>

<p>Your statement is ready.</p>

<p>Regards,</p>

🎯 Supported CSV Columns



Same attachment mode:



To



CC (optional)



Different attachment mode:



To



CC (optional)



Attachment (paths separated by ;)



⚠ Important Notes

📌 Gmail Authentication



Gmail blocks login with normal password.



Use an App Password if using Gmail SMTP.



Do not hardcode your credentials in code.

Use UI input or environment secrets.



📌 Gmail Limits



Free Gmail accounts have daily limits (~500 emails/day)



Sending many emails quickly may trigger Gmail restrictions



Use delay between sends



📌 Security



This app is public and can be abused if hosted without authentication.



For production use:



Add authentication



Use secure credentials storage



Use enterprise-grade SMTP (Outlook / Office 365 / SendGrid)



🛠 Deployment

📦 Requirements



Python 3.7+



streamlit



pandas



📌 Deploy on Streamlit Cloud



Push code to GitHub repo



Go to: https://share.streamlit.io



Create New App



Select repo, branch, and main file (app.py)



Deploy



No special environment variables required if email credentials are entered in UI.



📌 Local Run

pip install streamlit pandas

streamlit run app.py

🧠 Future Improvements



User authentication



OAuth-based email sending



Database-backed logs



Personalization support



Scheduling capability



📄 License



MIT License

