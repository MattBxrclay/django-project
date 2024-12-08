from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from pages.models import User
from pages.forms import UserForm
from django.core.mail import send_mail

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

def UserCreate(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email is confirmed
            user.save()

            # Generate email confirmation token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            email_subject = 'Confirm your Email'
            email_body = render_to_string('email_confirmation.html', {
                'user': user,
                'domain': 'localhost:8000',  # Change to your domain in production
                'uid': uid,
                'token': token,
            })

            # Send email
            send_mail(
                email_subject,
                email_body,
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )

            return HttpResponse('A confirmation email has been sent to your email address.')
    else:
        form = UserForm()
    return render(request, 'user_create.html', {'form': form})

def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        return HttpResponse('Thank you for confirming your email. You can now log in.')
    else:
        return HttpResponse('The confirmation link is invalid or has expired.')

# Test email sending (registration confirmation)
send_mail(
    'Subject Here',                 # Subject of the email
    'Message here',                 # Body of the email
    'your_email@gmail.com',         # From email address (can be the same as your Gmail)
    ['user1@gmail.com'],            # To email address
    fail_silently=False,
)
