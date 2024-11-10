from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render


from django.shortcuts import render, redirect
from .models import User  # Assuming you have a custom User model

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        selected_role = request.POST.get('role')  # Get selected role

        # Query the Users table directly
        try:
            # Check if user with the username, password, and selected role exists
            user = User.objects.get(username=username, password_hash=password, role=selected_role)

            # Log the user in by storing their ID in the session
            request.session['user_id'] = user.user_id  # Store user ID in session
            return redirect('home')  # Redirect to home after successful login

        except User.DoesNotExist:
            # Show error if user doesn't exist or role is incorrect
            return render(request, 'login.html', {'error': 'Invalid credentials or incorrect role selection.'})

    return render(request, 'login.html')



def logout(request):
    request.session.flush()  # Clear all session data
    return redirect('login')  # Redirect to login page after logging out




def home(request):
    user_id = request.session.get('user_id')
    
    user = get_object_or_404(User, user_id=user_id)
    
    return render(request, 'home.html', {
        'user': user,  # Pass the user object to the template
    })


def about(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, user_id=user_id)
    return render(request, 'about.html', {
        'user': user,  # Pass the user object to the template
    })






def contact(request):
    user_id = request.session.get('user_id')
    
    user = get_object_or_404(User, user_id=user_id)
    return render(request, 'contact.html', {
        'user': user,  # Pass the user object to the template
    })

def admin_dashboard(request):
    user_id = request.session.get('user_id')
    
    user = get_object_or_404(User, user_id=user_id)
    return render(request, 'admin_dashboard.html', {
        'user': user,  # Pass the user object to the template
    })

def staff_dashboard(request):
    user_id = request.session.get('user_id')
    
    user = get_object_or_404(User, user_id=user_id)
    return render(request, 'staff_dashboard.html', {
        'user': user,  # Pass the user object to the template
    })



def book_details(request):
    user_id = request.session.get('user_id')
    
    user = get_object_or_404(User, user_id=user_id)
    # Initialize an empty book variable
    book = None
    similar_books = []

    # Check if 'id' is in the GET request
    book_id = request.GET.get('id')
    if book_id:
        # Fetch the book by book_id instead of id
        book = get_object_or_404(Book, book_id=book_id)
        # Fetch similar books (e.g., same genre)
        similar_books = Book.objects.filter(genre=book.genre).exclude(book_id=book.book_id)

    # Render the template with the found book and similar books
    return render(request, 'book_details.html', {'user' : user, 'book': book, 'similar_books': similar_books})



def profile(request):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    
    user = get_object_or_404(User, user_id=user_id)
    if not user_id:
        return redirect('login')  # Redirect to login if not logged in

    # Retrieve user information and reading history
    try:
        user = User.objects.get(user_id=user_id)

        # Initialize a list to hold reading history details
        reading_history_details = []
        read_history = ReadingHistory.objects.get(user_id=user_id)
        book = Book.objects.get(book_id=read_history.book_id)  # Ensure you are fetching the correct Book instance
        author = Author.objects.get(author_id=book.author_id)

        # Prepare the data for this entry
        entry_data = {
            'read_date': read_history.read_date,
            'title': book.title,
            'book_id': book.book_id,
            'author': author.name  # Assuming a ManyToMany relationship
        }

        # Append this entry's data to the list
        reading_history_details.append(entry_data)

    except User.DoesNotExist:
        return redirect('login')  # Redirect to login if user not found

    return render(request, 'profile.html', {
        'user': user,
        'reading_history': reading_history_details
    })


def edit_profile(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)

    if request.method == 'POST':
        # Get updated information from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Update the user fields
        user.username = username
        user.email = email

        if password:  # Only update if a new password is provided
            user.password_hash = password  # Ensure you hash the password here

        user.save()  # Save the changes to the database
        return redirect('user-dashboard')  # Redirect to the user dashboard after update

    return render(request, 'edit_profile.html', {'user': user})


def update_preferences(request):
    return redirect('set_preferences')  # Redirect if accessed without POST






from django.shortcuts import render
from .models import Book, Author, Genre

def search_results(request):
    user_id = request.session.get('user_id')
    
    user = get_object_or_404(User, user_id=user_id)
    # Initialize an empty query set for the books
    search_results = Book.objects.all()
    genres = Genre.objects.all()  # Fetch all genres for the dropdown
    author = Author.objects.all() 

    # Check if the request method is GET and has search parameters
    if request.method == 'GET':
        genre = request.GET.get('genre')
        title = request.GET.get('author')
        availability = request.GET.get('availability')

        # Filter by genre if provided
        if genre and genre != 'all':
            search_results = search_results.filter(genre__genre_name=genre)

        # Filter by book title if provided
        if title:  # Use the variable 'title' for the book's title input
            # Filter books by the title
            search_results = search_results.filter(title__icontains=title) 

        # Filter by availability
        if availability == 'available':
            search_results = search_results.filter(availability=True)
        elif availability == 'borrowed':
            search_results = search_results.filter(availability=False)  # Assuming borrowed means not available
        # You may need to add additional logic for reserved status based on your models

    # Render the search results template with the results and genres
    return render(request, 'search_results.html', {
        'search_results': search_results,
        'genres': genres,
        'author': author,
        'user': user,
    })


# main/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User, Book  # Ensure you import the correct User model

def get_recommendations(user):
    # Get the genres of books the user has borrowed
    borrowed_genres = BorrowedBook.objects.filter(user=user).values_list('book__genre', flat=True)
    
    # Recommend books of similar genres that the user has not read
    recommended_books = Book.objects.filter(genre__in=borrowed_genres).exclude(
        book_id__in=ReadingHistory.objects.filter(user=user).values_list('book_id', flat=True)
    ).distinct()[:5]  # Limit recommendations to top 5 for simplicity
    
    return recommended_books


def user_dashboard(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, user_id=user_id)

    # Fetch borrowed and reserved books
    borrowed_books = BorrowedBook.objects.filter(user=user)
    reserved_books = Reservation.objects.filter(user=user)

    # Generate recommendations based on updated logic
    recommended_books = get_recommendations(user)

    context = {
        'user': user,
        'recommended_books': recommended_books,
        'borrowed_books': borrowed_books,
        'reserved_books': reserved_books,
    }
    return render(request, 'user_dashboard.html', context)


from django.shortcuts import render, redirect
from .forms import GenrePreferenceForm
from .models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404

def set_preferences(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, user_id=user_id) 
    if request.method == 'POST':
        form = GenrePreferenceForm(request.POST)
        if form.is_valid():
            selected_genre = form.cleaned_data['genres']  
            user.preferences = selected_genre  
            user.save()
            return redirect('home')  
    else:
        form = GenrePreferenceForm(initial={'genres': user.preferences})
    return render(request, 'set_preferences.html', {'form': form})
