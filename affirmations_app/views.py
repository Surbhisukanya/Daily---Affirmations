from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from affirmations_app.models import Affirmation
from affirmations_app import templates
import random

def home(request):
    #affirmation = Affirmation.objects.order_by('?').first()  # Random affirmation
    #return render(request, 'home.html', {'affirmation': affirmation})
    return render(request, 'home.html')
    
def home_view(request):
    # Fetch a random affirmation from the database
    daily_affirmation = random.choice(Affirmation.objects.all())
    context = {
        'daily_affirmation': daily_affirmation,  # Pass the affirmation details to the template
    }
    return render(request, 'home.html', context)
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, "You have successfully logged in.")
            return redirect('home')  # Redirect to the home page
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        email = request.POST['email']
        age = request.POST['age']
        password = request.POST['password']

        # Check if the user ID or email already exists
        if User.objects.filter(username=user_id).exists():
            messages.error(request, "User ID already taken.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken.")
            return render(request, 'register.html')

        # Create the user
        user = User.objects.create_user(username=user_id, email=email, password=password)
        user.profile.age = age  # Assuming you have a profile model to store additional info like age
        user.save()

        messages.success(request, "Your account has been created successfully.")
        return redirect('login')  # Redirect to login page after registration
    
    return render(request, 'register.html')



def search_affirmations(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')

    affirmations = Affirmation.objects.all()

    if query:
        affirmations = affirmations.filter(text__icontains=query)
    
    if category:
        affirmations = affirmations.filter(category=category)
    
    affirmations = affirmations.order_by('-rating')

    context = {
        'affirmations': affirmations,
    }
    return render(request, 'search.html', context)
    
#@login_required
def suggest_affirmation(request):
    if request.method == 'POST':
        affirmation_text = request.POST['affirmation_text']
        category = request.POST['category']
        
        # Save the affirmation
        affirmation = Affirmation.objects.create(
            text=affirmation_text,
            category=category,
            user=request.user
        )
        messages.success(request, "Your affirmation has been submitted!")
        return redirect('home')  # Redirect to home or another page
        
    return render(request, 'suggest_affirmation.html')

@login_required
def profile(request):
    # Access the currently logged-in user
    user = request.user
    
    # Pass user information to the template
    context = {
        'name': user.get_full_name() or user.username,  # Use full name if available, else username
        'email': user.email,
        'member_since': user.date_joined.strftime('%B %Y'),  # Format join date
        'total_affirmations': user.affirmation_set.count() if hasattr(user, 'affirmation_set') else 0  # Example: if affirmations are linked to user
    }
    
    return render(request, 'profile.html', context)