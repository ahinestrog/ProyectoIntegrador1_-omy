from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Nomy
from restaurant.models import Restaurant
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        "Usuario anónimo"

    restaurants = Restaurant.objects.all()

    searchTerm = request.GET.get('searchNomy')
    if searchTerm:
        nomys = Nomy.objects.filter(title__icontains=searchTerm)
    else:
        nomys = Nomy.objects.all()
    return render(request,'home.html', {'searchTerm':searchTerm, 'nomys': nomys, 'restaurants': restaurants})

def about(request):
    return render(request,'about.html')

def map(request):
    return render(request,'map.html')

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.info(request,'Username OR password is incorrect')
        
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + user)

            return redirect('home')



    context = {'form': form}
    return render(request,'register.html', context)

load_dotenv('api_keys_2.env')

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
default_whatsapp_number = os.getenv('DEFAULT_WHATSAPP')

client = Client(account_sid, auth_token)

def report(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        
        try:
            client.messages.create(
                body=message,
                from_=twilio_number,
                to=default_whatsapp_number
            )
            return render(request, 'report.html', {'success': 'Mensaje enviado exitosamente.'})
        except Exception as e:
            error_message = str(e)
            return render(request, 'report.html', {'error': f"Ocurrió un error: {error_message}"})
    
    return render(request, 'report.html')