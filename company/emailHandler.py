import os

from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from dotenv import load_dotenv

load_dotenv()
env = os.environ


def ApplicantStatus(data=dict):
    html_content = render_to_string("company/status.html", data)

    # Create the EmailMultiAlternatives object
    subject = f'Application to {data["company"]}'
    from_email = env.get('EMAIL_USER')
    to_email = [data["email"]]
    msg = EmailMultiAlternatives(subject, strip_tags(html_content), from_email, to_email)

    # Attach the HTML content
    msg.attach_alternative(html_content, "text/html")

    # Send the email
    try:
        msg.send()
        email_sent = True
    except Exception as e:
        email_sent = False
        # Notify of error
        print(f"Error sending email: {e}")

    return email_sent
