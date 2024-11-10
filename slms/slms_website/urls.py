# slms_website/urls.py

from django.urls import path
from .views import *


urlpatterns = [
    path('', login , name='login'),
    path('logout/', logout, name='logout'),
    path('edit-profile/', edit_profile, name='edit_profile'),#####
    path('update-preferences/', update_preferences, name='update_preferences'),####
    path('about/', about , name='about'),
    path('contact/', contact , name='contact'),
    path('home/', home, name='home'),
    path('profile/', profile, name='profile'),
    path('user-dashboard/', user_dashboard, name='user-dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('staff-dashboard/', staff_dashboard, name='staff-dashboard'),
    path('search-results/', search_results, name='search-results'),
    path('book-details/', book_details, name='book_details'),
    path('set_preferences/', set_preferences, name='set_preferences'),
    path('recommend_books/', recommend_books, name='recommend_books'),
    
    
]