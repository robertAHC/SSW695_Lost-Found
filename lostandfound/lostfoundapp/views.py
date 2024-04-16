from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# from lostandfound.lostandfound.settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER  # Import messages
from .forms import MissingItemForm
import logging
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import MissingItem
from django.contrib.auth.forms import UserCreationForm

# robert added librery
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import smtplib, ssl
from email.mime.text import MIMEText
# robert end of added libreries

logger = logging.getLogger(__name__)

@login_required
def logoutUser(request):
    logout(request)
    return redirect('/')

@login_required
def missing_item_detail(request, item_id):
    item = get_object_or_404(MissingItem, pk=item_id)
    return render(request, 'missing_item_detail.html', {'item': item})

# Function that sends email confirmation after user sucessfully send a missing item request
def send_email_summary(request):
    if request.method == 'POST':
        # robert code                
        EMAIL_HOST = 'live.smtp.mailtrap.io'
        EMAIL_HOST_USER = 'api'
        EMAIL_HOST_PASSWORD = '8639332f866ce9d7bac33228451edf83'
        EMAIL_PORT = 587

        # getting the posted information
        username = request.POST.get('username')
        lastname = request.POST.get('lastname')  
        email = request.POST.get('email')
        itemname = request.POST.get('name')
        description = request.POST.get('description')         
        color = request.POST.get('color')
        datelost = request.POST.get('date_lost')  

        subject = "Missing Item Report - Summary"
        body = "\n Hi, Robert this is a summary of the report you created: \n Full Name: " + username + " " + lastname + "\n Email: " + email + "\n Item Name: " + itemname + "\n Description: "  + description + "\n Color: " + color + "\n Date Lost: " + datelost + "\n  \n Thank you. \n Lost & Found team"
                
        sender = "mailtrap@demomailtrap.com" 
        recipients = ["robert.ahc27@gmail.com"]

        msg = MIMEText(body)

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        context = ssl.create_default_context()
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp_server:
           smtp_server.ehlo() 
           smtp_server.starttls(context=context)
           smtp_server.ehlo() 
           smtp_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
           smtp_server.sendmail(sender, recipients, msg.as_string())

@login_required
def report_missing_item(request):
    if request.method == 'POST':
        form = MissingItemForm(request.POST, request.FILES)
        if form.is_valid():
            missing_item = form.save(commit=False)
            try:
                user = User.objects.get(pk=1)  # Consider changing this to request.user if appropriate
                missing_item.user = user
                missing_item.save()
                item_detail_url = reverse('missing_item_detail', args=[missing_item.pk])

                messages.success(request, mark_safe(f'Your report for the missing item has been submitted successfully! <a href={item_detail_url}>View item</a>'))
                
                # Send email confirmation
                send_email_summary(request)
                    
                return redirect('report_missing_item')  # Or redirect to another page as needed
            except User.DoesNotExist:
                messages.error(request, 'The specified user does not exist.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MissingItemForm()

    return render(request, 'report_missing_item.html', {'form': form})


def landing_page(request):
    return render(request, 'index.html')


def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in
            return redirect('landing_page')  # Redirect to a landing page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('missing_items_list')  
        else:
            messages.error(request, "Username or password is incorrect.")
            return render(request, 'login.html')  

    return render(request, 'login.html')

def contactUs(request):
    if request.method == 'POST':
        # Information from the index.html
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Send Notification
        # robert code                
        EMAIL_HOST = 'live.smtp.mailtrap.io'
        EMAIL_HOST_USER = 'api'
        EMAIL_HOST_PASSWORD = '8639332f866ce9d7bac33228451edf83'
        EMAIL_PORT = 587

        subject = "Information Request"
        body = "\nTeam, \n \n" + str(name) + " sent the following message....\n\n" + str(message) + "\n\nYou can conctat the person using the following email address: \n" + str(email) 
                
        sender = "mailtrap@demomailtrap.com" 
        recipients = ["robert.ahc27@gmail.com"]

        msg = MIMEText(body)

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        context = ssl.create_default_context()
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp_server:
            smtp_server.ehlo()
            smtp_server.starttls(context=context)
            smtp_server.ehlo()
            smtp_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        
    return landing_page(request)
    

@login_required
def missing_items_list(request):
    items = MissingItem.objects.all()  # Retrieve all missing items from the database
    return render(request, 'missing_items_list.html', {'items': items})
