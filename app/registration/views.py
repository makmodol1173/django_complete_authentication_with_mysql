from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import connection
from decouple import config
import bcrypt

def registration(request):
    auth_token = request.COOKIES.get(config('COOKIE_KEY'))
    if auth_token:
        return redirect('/profile') 

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
            
            if data:
                messages.error(request, "Email already exists")
                return render(request, 'registration.html')
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            
            insert_query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (name, email, hashed_password, "user"))
            connection.commit() 
            
            response = redirect("/profile")
            response.set_cookie(config('COOKIE_KEY'), email, max_age=3600, httponly=True, secure=True)
            return response
    
    return render(request, 'registration.html')
