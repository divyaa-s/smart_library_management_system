from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render
from django.utils import timezone
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


from django.db import transaction  # Import transaction
from django.contrib import messages
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = 'User'  # Since signup is only for users, role is set to 'user'

        # Hash the password (you should use a secure hashing method in production)
        password_hash = password

        try:
            # Begin a transaction block
            with transaction.atomic():
                # Create the User instance
                user = User.objects.create(
                    username=username,
                    email=email,
                    password_hash=password_hash,
                    role=role,
                    total_penalty=0.0,  # Default penalty to 0
                    created_at=timezone.now()
                )
                user.save()
                #Create default ReadingHistory (optional)
                reading_history = ReadingHistory(user=user, book=None, read_date=timezone.now())
                reading_history.save()
                print(f"ReadingHistory created: {reading_history}")

                # Create default AIRecommendation (optional)
                ai_recommendation = AIRecommendation(user=user, book=None, score=0.0, created_at=timezone.now())
                ai_recommendation.save()
                print(f"AIRecommendation created: {ai_recommendation}")

                # Optionally, create a default AIRecommendations record (you may choose to have this after some activity)
                AIRecommendation.objects.create(
                    user=user,  # Link the new user instance
                    book_id=None,  # No recommendations yet, set it to None or placeholder
                    score=0.0,  # Default score to 0
                    created_at=timezone.now()
                )

            # If all operations succeed, show a success message and redirect
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')

        except Exception as e:
            # If any exception occurs (e.g., if one of the records cannot be created), the transaction will be rolled back
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'signup.html')

    return render(request, 'signup.html')



def logout(request):
    request.session.flush()  # Clear all session data
    return redirect('login')  # Redirect to login page after logging out



from django.shortcuts import render, get_object_or_404
from .models import User, Genre, Book

def home(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, user_id=user_id)

    # Fetch personalized recommendations based on the user's preferences
    recommendations = []
    if user.preferences:
        preferred_genre_name = user.preferences
        try:
            genre = Genre.objects.get(genre_name=preferred_genre_name)
            books = Book.objects.filter(genre=genre)
            recommendations = books
        except Genre.DoesNotExist:
            recommendations = []  # Handle case where genre doesn't exist

    return render(request, 'home.html', {'user': user, 'recommendations': recommendations})



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


from django.shortcuts import render, redirect, get_object_or_404
from slms_website.models import User, ReadingHistory, Book, Author
def profile(request):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect to login if not logged in

    # Retrieve user information and reading history
    user = get_object_or_404(User, user_id=user_id)

    # Get the reading history entries for the user
    reading_history_details = []

    try:
        # Fetch all the reading history records for the user
        reading_history = ReadingHistory.objects.filter(user=user)

        if not reading_history.exists():
            # If there's no reading history, handle this case accordingly
            reading_history_details.append({
                'message': "No reading history found for this user."
            })
        else:
            # Iterate over each reading history entry
            for entry in reading_history:
                entry_data = {
                    'read_date': entry.read_date,
                    'books': []  # Initialize an empty list for books
                }
                
                try:
                    # Loop through the book_ids stored in the JSON field
                    for book_id in entry.book_ids:
                        print(book_id)
                        # Get the book using the book_id from the JSON field
                        book = Book.objects.get(book_id=book_id)

                        # Append book details to the entry
                        book_data = {
                            'title': book.title,
                            'author': book.author.name,  # Assuming Book model has author as a foreign key
                            'book_id': book.book_id
                        }
                        entry_data['books'].append(book_data)

                except Book.DoesNotExist:
                    # Handle case where a book ID doesn't exist
                    entry_data['books'].append({
                        'message': f"Book with ID {book_id} does not exist."
                    })
                
                # Add the entry data to the list of reading history details
                reading_history_details.append(entry_data)

    except ReadingHistory.DoesNotExist:
        reading_history_details.append({
            'message': "Reading history does not exist for this user."
        })

    # Return the response with reading history
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
'''
def get_recommendations(user):
    # Get the genres of books the user has borrowed
    borrowed_genres = BorrowedBook.objects.filter(user=user).values_list('book__genre', flat=True)
    
    # Recommend books of similar genres that the user has not read
    recommended_books = Book.objects.filter(genre__in=borrowed_genres).exclude(
        book_id__in=ReadingHistory.objects.filter(user=user).values_list('book_id', flat=True)
    ).distinct()[:5]  # Limit recommendations to top 5 for simplicity
    
    return recommended_books
'''

def user_dashboard(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, user_id=user_id)

    # Fetch borrowed and reserved books
    borrowed_books = BorrowedBook.objects.filter(user=user)
    reserved_books = Reservation.objects.filter(user=user)

    # Generate recommendations based on updated logic
    recommended_books = recommend_books(user)

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

def recommend_books(user):
    # Assuming user preferences are stored as genre name
    if user.preferences:
        preferred_genre_name = user.preferences
        
        # Attempt to get the Genre object using the genre name stored in preferences
        try:
            genre = Genre.objects.get(genre_name=preferred_genre_name)
        except Genre.DoesNotExist:
            genre = None

        # If genre exists, find books in that genre
        if genre:
            books = Book.objects.filter(genre=genre)

            if books.exists():
                return books  # Return the list of recommended books

    return []  # Return empty if no books found or preference not set

'''


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages


def add_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Role should be chosen in form: "User", "Staff", etc.

        if not username or not password or not role:
            messages.error(request, "Please fill in all required fields.")
            return redirect('add_user')
        
        # Create new user
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        
        messages.success(request, f"User {username} added successfully.")
        return redirect('manage_users')
    
    return render(request, 'add_user.html')


def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')

        user.username = username if username else user.username
        user.email = email if email else user.email
        # Here, set any additional fields as needed
        user.save()

        messages.success(request, f"User {user.username} updated successfully.")
        return redirect('manage_users')

    context = {
        'user': user
    }
    return render(request, 'edit_user.html', context)



def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        username = user.username
        user.delete()
        messages.success(request, f"User {username} deleted successfully.")
        return redirect('manage_users')

    context = {
        'user': user
    }
    return render(request, 'delete_user.html', context)



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def manage_users(request):
    user_id = request.session.get('user_id')
    
    user = get_object_or_404(User, id=user_id)
    users = User.objects.all()
    context = {
        'users': users
    }

    return render(request, 'manage_users.html', context)
'''



# Add User
def add_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Role should be chosen in form: "User", "Staff", etc.

        if not username or not password or not role:
            messages.error(request, "Please fill in all required fields.")
            return redirect('add_user')
        
        # Create new user (password is automatically hashed)
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.is_staff = role == "Admin"  # Set role if Admin or Staff
        new_user.save()
        
        if role == "User":
            # Add a default Penalty record (if required)
            Penalty.objects.create(user=new_user, penalty_amount=0, reason="No Penalty", created_at=new_user.date_joined)
        
        messages.success(request, f"User {username} added successfully.")
        return redirect('manage_users')
    
    return render(request, 'add_user.html')


# Edit User
def edit_user(request, user_id):
    # Fetch the user from the database
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')

        # Update the fields
        user.username = username if username else user.username
        user.email = email if email else user.email
        user.is_staff = role == "Admin"  # Update role to Admin or Staff
        user.save()

        messages.success(request, f"User {user.username} updated successfully.")
        return redirect('manage_users')

    context = {
        'user': user
    }
    return render(request, 'edit_user.html', context)


# Delete User
def delete_user(request, user_id):
    # Fetch the user from the database
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        username = user.username

        # Delete related records in other tables before deleting the user
        BorrowedBook.objects.filter(user=user_id).delete()  # Delete all borrowed books by this user
        #Penalty.objects.filter(user=user_id).delete()  # Delete all penalties for this user
        Reservation.objects.filter(user=user_id).delete()  # Delete all reservations by this user
        user.delete()
        messages.success(request, f"User {username} deleted successfully.")
        return redirect('manage_users')
    

    context = {
        'user': user
    }
    return render(request, 'delete_user.html', context)



# Manage Users - Display all users
def manage_users(request):
    # Get the user id from the session
    user_id = request.session.get('user_id')

    # Fetch the logged-in user (admin) using the session's user_id
    user = get_object_or_404(User, user_id=user_id)

    # E
    # Fetch all users for admin to manage
    users = User.objects.all()
    context = {
        'users': users,
        'user': user  # Pass logged-in user info to the template
    }

    return render(request, 'manage_users.html', context)