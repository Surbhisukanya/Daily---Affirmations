from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.db.models import Q
from .models import Affirmation, UserProfile, UserRating
import random
import logging

logger = logging.getLogger(__name__)

def home(request):
    context = {}
    try:
        affirmations = Affirmation.objects.all()
        if affirmations.exists():
            affirmation = random.choice(affirmations)
            affirmation.update_average_rating()
        else:
            affirmation = Affirmation.objects.create(
                affirmation="I am capable of achieving anything I set my mind to.",
                category="Motivation"
            )
        context['affirmation'] = affirmation
    except Exception as e:
        logger.error(f"Error in home view: {str(e)}")
        context['affirmation'] = {
            'affirmation': "Welcome to Daily Affirmations!",
            'rating': 0,
            'category': 'General'
        }
        messages.error(request, "There was an issue loading the affirmation. Please try again later.")
    return render(request, 'home.html', context)

@login_required
def rate_affirmation(request, affirmation_id):
    if request.method == 'POST':
        affirmation = get_object_or_404(Affirmation, id=affirmation_id)
        try:
            rating = int(request.POST.get('rating', 4))
            rating = max(1, min(5, rating))
            
            UserRating.objects.update_or_create(
                user=request.user,
                affirmation=affirmation,
                defaults={'rating': rating}
            )
            
            affirmation.update_average_rating()
            messages.success(request, "Rating submitted successfully!")
        except ValueError:
            messages.error(request, "Invalid rating value.")
        except Exception as e:
            logger.error(f"Error in rate_affirmation view: {str(e)}")
            messages.error(request, "There was an error submitting your rating.")
    return redirect('home')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('home')
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
        user_profile.set_password(password)
        user_profile.save()
        
        messages.success(request, "Your account has been created successfully.")
        return redirect('login')

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
        
        # Save the affirmation with default rating of 4
        affirmation = Affirmation.objects.create(
            affirmation=affirmation_text,
            category=category,
            user=request.user,
            rating=4  # Set default rating to 4
        )
        messages.success(request, "Your affirmation has been submitted!")
        return redirect('home')
        
    return render(request, 'suggest_affirmation.html')

@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    suggested_affirmations = Affirmation.objects.filter(user=request.user).order_by('-id')
    
    context = {
        'user_profile': user_profile,
        'suggested_affirmations': suggested_affirmations,
    }
    return render(request, 'profile.html', context)

def logout_view(request):
    auth.logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')
