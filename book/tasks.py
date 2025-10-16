import time

from celery import shared_task
from django.core.mail import send_mail

from user.models import User


@shared_task
def send_new_book_via_email(book_title):
    users = User.objects.all().values_list('email', flat=True)
    email_list = [email for email in users if email]

    print(email_list)

    subject = f"New Book Added: {book_title}"
    message = f"A new book '{book_title}' has just been added to our library!"
    from_email = "bookManager@app.com"

    for email in email_list:
        send_mail(subject, message, from_email, [email])
        time.sleep(0.5)

    return f"Emails sent to {len(email_list)} users for book: {book_title}"