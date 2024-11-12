# slms_website/urls.py

from django.urls import path
from .views import *


urlpatterns = [
    path('', login , name='login'),
    path('signup/', signup, name='signup'), 
    path('logout/', logout, name='logout'),
    path('edit-profile/', edit_profile, name='edit_profile'),#####
    path('update-preferences/', update_preferences, name='update_preferences'),####
    path('about/', about , name='about'),
    path('contact/', contact , name='contact'),
    path('home/', home, name='home'),
    path('profile/', profile, name='profile'),
    path('user-dashboard/', user_dashboard, name='user-dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('manage-users/', manage_users, name='manage_users'), #new
    path('add-user/', add_user, name='add_user'), #new
    path('edit-user/<int:user_id>/', edit_user, name='edit_user'), #new
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'), #new
    path('add-book/', add_book, name='add_book'),
    path('edit-book/<int:book_id>/', edit_book, name='edit_book'),
    path('delete-book/<int:book_id>/', delete_book, name='delete_book'),
    path('manage-books/', manage_books, name='manage_books'),
    path('staff-dashboard/', staff_dashboard, name='staff-dashboard'),
    path('search-results/', search_results, name='search-results'),
    path('book-details/', book_details, name='book_details'),
    path('set_preferences/', set_preferences, name='set_preferences'),
    path('recommend_books/', recommend_books, name='recommend_books'),
    path('reserve/<int:book_id>/', reserve_book, name='reserve_book'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('books/', view_books, name='book_list'),

    
    
]