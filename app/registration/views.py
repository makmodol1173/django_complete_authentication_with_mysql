from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import connection

def registration(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if not name or not email or not password:
            messages.error(request, "All fields are required")
            return render(request, 'registration.html')
        
        with connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query,(email,))
            data = cursor.fetchone()
            print(data)
        
        print(name, email, password)

    
    return render(request, 'registration.html')
