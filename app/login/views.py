from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from decouple import config
import bcrypt

def login(request):
    auth_token = request.COOKIES.get(config('COOKIE_KEY'))
    if auth_token:
        return redirect('/profile')
    
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if not email or not password:
            messages.error(request, "All fields are required")
            return render(request, 'login.html')

        with connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query,(email,))
            data = cursor.fetchone()
               
            if not data:
                messages.error(request, "No user found with that email address.")
                return render(request, 'login.html')
                
            check_password = bcrypt.checkpw(password.encode('utf-8'), data[3].encode('utf-8'))
            
            if check_password:
                response = redirect("/profile")
                response.set_cookie(config('COOKIE_KEY'), email, max_age=3600, httponly=True, secure=True)
                return response
            else:
                    messages.error(request, "Invalid password. Please try again.")
                    
    return render(request, 'login.html')
