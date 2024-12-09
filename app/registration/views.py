from django.shortcuts import redirect, render
from django.contrib import messages

def registration(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if not name or not email or not password:
            messages.error(request, "All fields are required")
            return render(request, 'registration.html')
        

    
    return render(request, 'registration.html')
