from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Affirmation, UserProfile
import random

def home_view(request):
    affirmation = Affirmation.objects.order_by('?').first()  # Random affirmation
    return render(request, 'home.html', {'affirmation': affirmation})

def home(request):
    # Fetch a random affirmation from the database
    daily_affirmation = random.choice(Affirmation.objects.all())
    context = {
        'daily_affirmation': daily_affirmation,
    }
    return render(request, 'home.html', context)
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)  # Log the user in
            messages.success(request, "You have successfully logged in.")
            return redirect('home')  # Redirect to the home page
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('user_id')
        age = request.POST.get('age')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken.")
            return render(request, 'register.html')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create the user profile with encrypted password
        user_profile = UserProfile(user=user, age=age, email=email)
        user_profile.set_password(password)  # This will encrypt and save the password
        
        messages.success(request, "Your account has been created successfully.")
        return redirect('login')  # Redirect to login page after registration

    return render(request, 'register.html')

def search_affirmations(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')

    affirmations = Affirmation.objects.all()

    if query:
        affirmations = affirmations.filter(affirmation__icontains=query)
    
    if category:
        affirmations = affirmations.filter(category=category)
    
    affirmations = affirmations.order_by('-rating')

    context = {
        'affirmations': affirmations,
    }
    return render(request, 'search.html', context)
    
@login_required
def suggest_affirmation(request):
    if request.method == 'POST':
        affirmation_text = request.POST.get('affirmation_text')
        category = request.POST.get('category')
        
        # Save the affirmation
        affirmation = Affirmation.objects.create(
            affirmation=affirmation_text,
            category=category,
            user=request.user
        )
        messages.success(request, "Your affirmation has been submitted!")
        return redirect('home')
        
    return render(request, 'suggest_affirmation.html')

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    suggested_affirmations = Affirmation.objects.filter(user=request.user)
    return render(request, 'profile.html', {
        'user_profile': user_profile,
        'suggested_affirmations': suggested_affirmations
    })

def logout_view(request):
    auth.logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')
