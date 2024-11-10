# slms_website/models.py
from django.db import models

class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'authors'


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'genres'


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    synopsis = models.TextField()
    availability = models.BooleanField(default=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'books'


class BookCopy(models.Model):
    copy_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    branch_id = models.IntegerField()  # Adjust as per your schema
    status = models.CharField(max_length=50)  # e.g., 'available', 'borrowed'
    
    class Meta:
        db_table = 'bookcopies'


from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    total_penalty = models.DecimalField(decimal_places=2, max_digits=6)
    preferences = models.CharField(max_length=255, null=True, blank=True)  # Changed to CharField
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'



class BorrowedBook(models.Model):
    borrow_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    penalty_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    qr_code = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'borrowedbooks'


class Penalty(models.Model):
    penalty_id = models.AutoField(primary_key=True)
    borrow = models.ForeignKey(BorrowedBook, on_delete=models.CASCADE)
    reason = models.TextField()
    penalty_amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'penalties'


class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    expiration_date = models.DateField()
    
    class Meta:
        db_table = 'reservations'


class ReadingHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_date = models.DateField()
    
    class Meta:
        db_table = 'readinghistory'


class BookReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bookreviews'


class AIRecommendation(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'airecommendations'


class LibraryEvent(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'libraryevents'


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'staff'



