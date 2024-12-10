from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from decouple import config

def profile(request):
    
    auth_token = request.COOKIES.get(config('COOKIE_KEY'))
    if not auth_token:
        return redirect('/login')
        
    with connection.cursor() as cursor:
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query,(auth_token,))
        data = cursor.fetchone()
        user = {'name':data[1], 'email': data[2]}
    return render(request, 'profile.html',user)
