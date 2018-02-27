from django.contrib.auth.models import User
from django.core.mail import send_mass_mail, send_mail, EmailMessage, EmailMultiAlternatives, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.core import mail

connection = mail.get_connection()




date = datetime.datetime.now()
subject = "HXCPDX UPDATE"+ " "+ str(date)
body = ""
from_email = 'mikeynon@gmail.com'
html_content = '<p>This is an <strong>important</strong> message.</p>'

for user in User.objects.all():
    try:
        message = EmailMultiAlternatives(subject, body, from_email, user.Email)
        msg = message.attach_file('design.png',)
        send_mail(msg)
    except ValueError:
        continue

def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['admin@example.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')