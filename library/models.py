from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from phonenumber_field.modelfields import PhoneNumberField
import os # Used for operating system-dependent functionality

# Create your models here.

#User Control

class User(AbstractUser):
    email = models.EmailField(unique = True)
    phone_no = PhoneNumberField(unique = True)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email','phone_no', 'first_name', 'last_name']

    # Override save method to set admin flag for superuser and assign groups
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_admin = True
        super().save(*args, **kwargs)

        # Assign user to the appropriate group
        if self.is_teacher:
            group, created = Group.objects.get_or_create(name='Teacher')
            self.groups.add(group)
        elif self.is_student:
            group, created = Group.objects.get_or_create(name='Student')
            self.groups.add(group)
        elif self.is_admin:
            group, created = Group.objects.get_or_create(name='Admin')
            self.groups.add(group)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_id = models.CharField(max_length=32, unique=True)
    level = models.CharField(max_length=32)
    class_name = models.CharField(max_length=16)
    teacher_type = models.CharField(max_length=32)
    employment_status = models.CharField(max_length=16)
    department = models.CharField(max_length=32)
    subject = models.CharField(max_length=16)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    registration_no = models.CharField(max_length=32, unique=True)
    level = models.CharField(max_length=16)
    year =  models.IntegerField()
    faculty = models.CharField(max_length=32)

#Model Control

class BookAuthor(models.Model): # "BookAuthor" database table
    name = models.CharField(max_length=64)  # "name" field of database table that store string of maximum length 64

class BookCategory(models.Model):
    name = models.CharField(max_length=32)

class BookPublisher(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)

class BookLanguage(models.Model):
    name = models.CharField(max_length=32)

class Book(models.Model):
    name = models.CharField(max_length=128)
    author = models.ManyToManyField(BookAuthor) # "author" field which have Many-to-many relationship with the BookAuthor table, allowing a book to have multiple authors.
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null= True) # One to Many "ForeginKey Relationship"
    edition = models.CharField(max_length=32)
    publisher = models.ForeignKey(BookPublisher,on_delete=models.SET_NULL, null= True)
    publication_year = models.IntegerField()
    isbn = models.CharField(max_length=13)
    language = models.ForeignKey(BookLanguage, on_delete=models.SET_NULL, null= True)
    pages = models.IntegerField()
    description = models.TextField()
    book_file = models.FileField(upload_to='books/')

    def delete(self, *args, **kwargs): # "delete" method to remove associated file from book file directory
        if self.book_file: # Retrieves the path of the file.
            if os.path.isfile(self.book_file.path): # Checks if the file exists
                os.remove(self.book_file.path) # Removes the file from the filesystem.
        super().delete(*args, **kwargs) #calls the delete method to perform the deletion of the Book object from the database.
