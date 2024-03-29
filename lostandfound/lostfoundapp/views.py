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


logger = logging.getLogger(__name__)

# robert added code
def loginPage(request):
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
            return redirect('report_missing_item')
        else:
            messages.error(request, "Warning: Username OR passowrd does not exist.")
        
    context = {}
    return render(request, 'login_registration.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')

# robert ended added code


def missing_item_detail(request, item_id):
    item = get_object_or_404(MissingItem, pk=item_id)
    return render(request, 'missing_item_detail.html', {'item': item})


def report_missing_item(request):
    if request.method == 'POST':
        form = MissingItemForm(request.POST, request.FILES)
        if form.is_valid():
            missing_item = form.save(commit=False)
            try:
                # Assuming user with pk=1 always exists for simplicity
                user = User.objects.get(pk=1)
                missing_item.user = user
                missing_item.save()
                item_detail_url = reverse(
                    'missing_item_detail', args=[missing_item.pk])

                messages.success(request, mark_safe(
                    f'Your report for the missing item has been submitted successfully! <a href="{item_detail_url}">View item</a>'))

                # Redirect back to the report_missing_item view
                return redirect('report_missing_item')
            except User.DoesNotExist:
                messages.error(request, 'The specified user does not exist.')
        else:
            # Form is not valid, so fall through to the render call which will display form errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MissingItemForm()

    return render(request, 'report_missing_item.html', {'form': form})

def landing_page(request):
    return render(request, 'index.html')
