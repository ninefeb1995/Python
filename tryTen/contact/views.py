from django.shortcuts import render
from .form import contactForm
from django.core.mail import send_mail
# Create your views here.

def contact(request):
    form = contactForm(request.POST or None)
    form.name = ' test'
    if form.is_valid():
        print(form.cleaned_data['email'])
    context = {
        'title': "Contact",
        'form': form,
    }
    template = 'contact.html'
    return render(request, template, context)