import smtplib, ssl


def send_email(email, password):

    port = 465  # For SSL

    message = """Subject: Somebody rang the bell!
    \n
    A sound event that seems to be your door buzzer just occurred. """

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, email, message)


if __name__ == '__main__':

    send_email()