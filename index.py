import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Streamlit app title
st.title("Contact Form")

# Create form for user input
name = st.text_input("Name")
subject = st.text_input("Subject")
email = st.text_input("Email")

# Create a button to submit the form
if st.button("Submit"):
    # Check if all fields are filled
    if name and subject and email:
        # Set up email parameters
        sender_email = "your_email@gmail.com"
        receiver_email = "receiver_email@gmail.com"  # Change to your recipient's email
        password = "your_password"  # Change to your email password

        # Create message object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Email body
        body = f"Name: {name}\nEmail: {email}\nSubject: {subject}"
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please fill in all fields.")
