from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib import messages  # Import messages
from .forms import MissingItemForm


@csrf_exempt
def report_missing_item(request):
    item_added = None  # Initialize variable to check if item was added

    if request.method == 'POST':
        form = MissingItemForm(request.POST, request.FILES)
        if form.is_valid():
            missing_item = form.save(commit=False)
            user_id = request.POST.get('user_id')

            try:
                missing_item.user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise Http404("User does not exist")

            missing_item.save()
            item_added = missing_item
            # Add a success message
            messages.success(request, 'Item added successfully!')

            # Redirect to the same page (or another page as per your requirement)
            # Make sure 'report_missing_item' is the name of your URL pattern for this view
            return redirect('report_missing_item')

    else:
        form = MissingItemForm()

    return render(request, 'index.html', {'form': form,
                                          'item_added': item_added})
