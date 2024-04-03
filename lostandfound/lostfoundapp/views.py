from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # Import messages
from .forms import MissingItemForm
import logging
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import MissingItem
from django.contrib.auth.forms import UserCreationForm


logger = logging.getLogger(__name__)

"""def loginPage(request):
    # First check if method is equals to POST
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        
        # # validate user
        # try:
        #     user = User.objects.get(username=username)
        # except:
        #     messages.error(request, "Invalid user!")
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('landing_page')
        else:
            messages.error(request, "Warning: Username OR passowrd does not exist.")
        
    context = {}
    return render(request, 'login_registration.html', context)"""

def logoutUser(request):
    logout(request)
    return redirect('/')

def missing_item_detail(request, item_id):
    item = get_object_or_404(MissingItem, pk=item_id)
    return render(request, 'missing_item_detail.html', {'item': item})

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
            return redirect('landing_page')  
        else:
            messages.error(request, "Username or password is incorrect.")
            return render(request, 'login.html')  

    return render(request, 'login.html')


def missing_items_list(request):
    items = MissingItem.objects.all()  # Retrieve all missing items from the database
    return render(request, 'missing_items_list.html', {'items': items})
