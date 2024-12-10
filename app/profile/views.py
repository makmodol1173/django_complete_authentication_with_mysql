from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from decouple import config
import bcrypt

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


def change_password(request):
    auth_token = request.COOKIES.get(config('COOKIE_KEY'))
    if not auth_token:
        return redirect('/login')
    
    if request.method == 'GET':
        return redirect('/profile')
    
    with connection.cursor() as cursor:
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query,(auth_token,))
        data = cursor.fetchone()
        user = {'name':data[1], 'email': data[2]}

    if request.method == 'POST':
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        
        if not current_password or not new_password or not confirm_password:
            messages.error(request, "All fields are required")
            return render(request, 'profile.html')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match")
            return render(request, 'profile.html', user)
        
        check_password = bcrypt.checkpw(current_password.encode('utf-8'), data[3].encode('utf-8'))

        if not check_password:
            messages.error(request, "Current password is incorrect.")
            return render(request, 'profile.html', user)
        
        with connection.cursor() as cursor:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            update_query = "UPDATE users SET password = %s WHERE email = %s"
            cursor.execute(update_query, (hashed_password, auth_token))
            connection.commit()
                
    return render(request, 'profile.html',user)

def logout(request):
    response = redirect('/login')
    response.delete_cookie('auth_token')
    return response