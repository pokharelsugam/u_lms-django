from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Teacher, Student, BookAuthor, BookCategory,BookPublisher, BookLanguage, Book
from django.http import HttpResponse, Http404
from django.db.models import Q #This class is used to construct complex queries using OR, AND, and NOT operations
import os
from django.conf import settings


# Create your views here.

###########################################################################################

#Login Control
def login_universal(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now successfully logged in as {username}.")
                return redirect('home')  # Redirect to a user profile page or dashboard
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_universal(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')  # Redirect to login page after logout

###########################################################################################
# Registration Control

User = get_user_model()
@login_required
def register_teacher(request):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized", status=401)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone_no = request.POST['phone_no']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        employee_id = request.POST['employee_id']
        level = request.POST['level']
        class_name = request.POST['class_name']
        teacher_type = request.POST['teacher_type']
        employment_status = request.POST['employment_status']
        department = request.POST['department']
        subject = request.POST['subject']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'A user with this username already exists.')
            return render(request, 'register-teacher.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, 'register-teacher.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_no = phone_no,
            first_name = first_name,
            last_name = last_name,
            is_teacher=True
        )
        Teacher.objects.create(
            user=user,
            employee_id=employee_id,
            level=level,
            class_name=class_name,
            teacher_type = teacher_type,
            employment_status = employment_status,
            department = department,
            subject=subject 
        )
        messages.info(request, f"The teacher {first_name} {last_name} was successfully registered.")
        return redirect('register_teacher')

    return render(request, 'register-teacher.html')

@login_required
def register_student(request):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized", status=401)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone_no = request.POST['phone_no']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        registration_no = request.POST['registration_no']
        level = request.POST['level']
        year = request.POST['year']
        faculty = request.POST['faculty']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'A user with this username already exists.')
            return render(request, 'register-student.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, 'register-student.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_no = phone_no,
            first_name = first_name,
            last_name = last_name,
            is_student=True
        )
        Student.objects.create(
            user=user,
            registration_no=registration_no,
            level=level,
            year = year,
            faculty = faculty,
        )
        messages.info(request, f"The student {first_name} {last_name} was successfully registered.")
        return redirect('home')

    return render(request, 'register-student.html')
# Similarly, you can create views for editing and deleting teachers and student

###########################################################################################

# User Control
@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
    }
    if hasattr(user, 'teacher'):
        context['profile'] = user.teacher
    elif hasattr(user, 'student'):
        context['profile'] = user.student

    return render(request, 'profile.html', context)


###########################################################################################

# Public Home View
def home(request): # User defined home function for "home" url to with "request" parameter used to sent http request to server by client
    book_objs = Book.objects.all().order_by('-id')[:2] #Retrive all records from Book model(Book database table) where it sorts in descending order and selects 2 books
    data = {'new_books': book_objs} #data Dictionary key=new_books, value= books_objs
    return render(request,'index.html', context=data) #Pass data dictionary to "index.html" template according to request


###########################################################################################

# BookAuthor Views CRUD
#Read
@login_required
def author_list(request): # User defined author_list function for "author_list" url
    author_objs = BookAuthor.objects.all()  #Retrive all records from BookAuthor model(BookAuthor database table)
    data = {'authors': author_objs}
    return render(request,'author.html',context=data) #Pass data dictionary to author.html template according to request for diaplay

#Create
@login_required
def author_add(request):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    if request.method == 'POST': # Checking request is "POST" or not means form is submitted or not
        name = request.POST.get('name') # Retribe (get) data from field with "name" attribut from request sent form(author-add.html)

        if BookAuthor.objects.filter(name=name).exists(): #Checks if there is already an author with the given name in the BookAuthor model.
            error_message = f"Author with name '{name}' already exists." #If an author with the same name already exists, an error message is generated.
            return render(request, 'author-add.html', {'error_message': error_message}) #The render function then re-renders the author-add.html template, passing the error message to the template for display.

        BookAuthor.objects.create(name=name) # Creates a new author record with the given name in the BookAuthor model.
        messages.info(request, f" The author '{name}' was successfully created ")
        return redirect('author_list')

    return render(request,'author-add.html')# Template is rendered, which display form for adding a new author.

@login_required
def author_edit(request, pk): # pk is a parameter that represents the primary key (id) of the BookAuthor object to be edited.
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    author = get_object_or_404(BookAuthor, id=pk) #Retrieves the BookAuthor object with the given primary key (id=pk).

    if request.method == 'POST':
        name = request.POST.get('name') #  Retrieves the value of the form field with the name attribute 'name' for edit.
        author.name = name # Updates the name attribute of the author object with the new name.
        author.save() # Saves the changes to the database.
        messages.info(request, f" The author named as'{name}' was successfully updated ")
        return redirect('author_list')

    return render(request, 'author-edit.html', {'author': author}) # author object passed to author-edit.html for display

@login_required
def author_delete(request,pk):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    try:
        author= BookAuthor.objects.get(id=pk)
    except:
        return HttpResponse('Data is not Found beacause it may be  deleted. Please go one step back') # Data not found error handeling
    if request.method == 'POST':
        author.delete()
        messages.info(request, f" The author named as'{author.name}' was successfully deleted ")
        return redirect('author_list')

    return render(request, 'author-delete-confirm.html', {'author': author})


###########################################################################################

# BookCategory Views CRUD

@login_required
def category_list(request):
    category_objs = BookCategory.objects.all()
    data = {'categories': category_objs}
    return render(request, 'category.html', context=data)

@login_required
def category_add(request):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    if request.method == 'POST':
        name = request.POST.get('name')

        if BookCategory.objects.filter(name=name).exists():
            error_message = f"Category with name '{name}' already exists."
            return render(request, 'category-add.html', {'error_message': error_message})

        BookCategory.objects.create(name=name)
        messages.info(request, f" The category named as'{name}' was successfully created ")
        return redirect('category_list')

    return render(request, 'category-add.html')

@login_required
def category_edit(request, pk):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    category = get_object_or_404(BookCategory, id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        category.name = name
        category.save()
        messages.info(request, f" The category named as'{name}' was successfully updated ")
        return redirect('category_list')

    return render(request, 'category-edit.html', {'category': category})

@login_required
def category_delete(request,pk):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    try:
        category= BookCategory.objects.get(id=pk)
    except:
        return HttpResponse('Data is not Found beacause it may be  deleted. Please go one step back')    
    if request.method == 'POST':
        category.delete()
        messages.info(request, f" The category named as'{category.name}' was successfully deleted ")
        return redirect('category_list')

    return render(request, 'category-delete-confirm.html', {'category': category})


###########################################################################################

#BookPublisher Views CRUD

@login_required
def publisher_list(request):
    publisher_objs = BookPublisher.objects.all()
    data = {'publishers': publisher_objs}
    return render(request, 'publisher.html', context=data)

@login_required
def publisher_add(request):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')

        if BookPublisher.objects.filter(name=name).exists():
            error_message = f"Publisher with name '{name}' already exists."
            return render(request, 'publisher-add.html', {'error_message': error_message})

        BookPublisher.objects.create(name=name, address=address)
        messages.info(request, f" The publisher named as'{name}' was successfully created ")
        return redirect('publisher_list')

    return render(request, 'publisher-add.html')

@login_required
def publisher_edit(request, pk):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    publisher = get_object_or_404(BookPublisher, id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        publisher.name = name
        publisher.address = address
        publisher.save()
        messages.info(request, f" The publisher named as '{name}' was successfully updated ")
        return redirect('publisher_list')

    return render(request, 'publisher-edit.html', {'publisher': publisher})

@login_required
def publisher_delete(request,pk):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    try:
        publisher= BookPublisher.objects.get(id=pk)
    except:
        return HttpResponse('Data is not Found beacause it may be  deleted. Please go one step back')    
    if request.method == 'POST':
        publisher.delete()
        messages.info(request, f" The publisher named as '{publisher.name}' was successfully deleted ")
        return redirect('publisher_list')

    return render(request, 'publisher-delete-confirm.html', {'publisher': publisher})

###########################################################################################

#BookLanguage View CRUD

@login_required
def language_list(request):
    language_objs = BookLanguage.objects.all()
    data = {'languages': language_objs}
    return render(request, 'language.html', context=data)

@login_required    
def language_add(request):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    if request.method == 'POST':
        name = request.POST.get('name')

        if BookLanguage.objects.filter(name=name).exists():
            error_message = f"Language with name '{name}' already exists."
            return render(request, 'language-add.html', {'error_message': error_message})

        BookLanguage.objects.create(name=name)
        messages.info(request, f" The language named as '{name}' was successfully created ")
        return redirect('language_list')

    return render(request, 'language-add.html')

@login_required
def language_edit(request, pk):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    language = get_object_or_404(BookLanguage, id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        language.name = name
        language.save()
        messages.info(request, f" The language named as '{name}' was successfully updated ")
        return redirect('language_list')

    return render(request, 'language-edit.html', {'language': language})

@login_required
def language_delete(request,pk):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    try:
        language= BookLanguage.objects.get(id=pk)
    except:
        return HttpResponse('Data is not Found beacause it may be  deleted. Please go one step back')
    if request.method == 'POST':
        language.delete()
        messages.info(request, f" The language named as '{language.name}' was successfully deleted ")
        return redirect('language_list')

    return render(request, 'language-delete-confirm.html', {'language': language})

###########################################################################################


#Book Views CRUD
@login_required
def book_list(request):
    book_objs = Book.objects.all()
    data = {'books': book_objs}
    return render(request, 'book.html', context=data)

@login_required
def book_get(request, pk):
    book_objs = get_object_or_404(Book, id=pk)
    return render(request, 'book-get.html', {'book': book_objs})

@login_required
def book_add(request):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401) 
    if request.method == 'POST':
        name = request.POST.get('name') #Retrieves the name of book from single form field.
        author_ids = request.POST.getlist('author')  #Retrives list of authors in the form of id from multi form field.
        category_id = request.POST.get('category')
        edition = request.POST.get('edition')
        publisher_id = request.POST.get('publisher')
        publication_year = request.POST.get('publication_year')
        isbn = request.POST.get('isbn')
        language_id = request.POST.get('language')
        pages = request.POST.get('pages')
        description = request.POST.get('description')
        book_file = request.FILES.get('book_file') # Retrieves the uploaded file for the 'book_file' field.

        book = Book.objects.create(  # Creates a new Book object with the provided values and saves it to the database.
            name=name, 
            category_id=category_id, #Category_id field is assigned the corresponding ID for the category.
            edition=edition, 
            publisher_id=publisher_id, 
            publication_year=publication_year, 
            isbn=isbn, 
            language_id=language_id, 
            pages=pages, 
            description=description, 
            book_file=book_file
        ) 

        book.author.set(author_ids)  # Set the authors lists for the book object, many to many
        messages.info(request, f" The book named as '{name}' was successfully created ")
        return redirect('book_list')

    authors = BookAuthor.objects.all()      # Retrives all data from BookAuthor Model to athors object used to populate in form field
    categories = BookCategory.objects.all()
    publishers = BookPublisher.objects.all()
    languages = BookLanguage.objects.all()

    return render(request, 'book-add.html', {
        'authors': authors,
        'categories': categories,
        'publishers': publishers,
        'languages': languages,
    }) #Retrives authors, categories, publishers, and languages are passed to the book-add.html, making them available for selection in the form.


def book_search(request):
    query = request.GET.get('query', '') # Retrieves the value of the query parameter from the URL. If the query parameter is not provided, it defaults to an empty string ('').

    if query: # Checks if a search query was provided.
        books = Book.objects.filter(
            Q(name__icontains=query) | # Matches books whose name contains the query string (case-insensitive).
            Q(author__name__icontains=query) | # The symbol "|" represent OR operator 
            Q(category__name__icontains=query) |
            Q(publisher__name__icontains=query) |
            Q(isbn__icontains=query)
        ).distinct() # Ensures that the results do not contain duplicate entries
    else:
        books = Book.objects.none() #If no query is provided, it returns an empty queryset.

    context = {
        'books': books, #  This allows the template to access the search results
        'query': query, #  This allows the template to display the current search query
    }
    
    return render(request, 'book-search.html', context)

@login_required
def book_edit(request, pk):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    book = get_object_or_404(Book, id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        author_ids = request.POST.getlist('author')
        category_id = request.POST.get('category')
        edition = request.POST.get('edition')
        publisher_id = request.POST.get('publisher')
        publication_year = request.POST.get('publication_year')
        isbn = request.POST.get('isbn')
        language_id = request.POST.get('language')
        pages = request.POST.get('pages')
        description = request.POST.get('description')

        book.name = name # Pass name value to the book object of name field for update
        book.category_id = category_id
        book.edition = edition
        book.publisher_id = publisher_id
        book.publication_year = publication_year
        book.isbn = isbn
        book.language_id = language_id
        book.pages = pages
        book.description = description

        book.author.set(author_ids) 
        book.save()
        messages.info(request, f" The book named as '{name}' was successfully updated ")
        return redirect('book_get',pk)

    authors = BookAuthor.objects.all()
    categories = BookCategory.objects.all()
    publishers = BookPublisher.objects.all()
    languages = BookLanguage.objects.all()

    return render(request, 'book-edit.html', {
        'book': book,
        'authors': authors,
        'categories': categories,
        'publishers': publishers,
        'languages': languages,
    })

@login_required
def book_delete(request, pk):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized! You are login as either teacher or student. Please login with admin to access full features", status=401)
    try:
        book = Book.objects.get(id=pk)
    except:
        return HttpResponse('Data is not Found beacause it may be deleted. Please go one step back')    
    if request.method == 'POST':
        book.delete()
        messages.info(request, f" The book named as '{book.name}' was successfully deleted ")
        return redirect('book_list')

    return render(request, 'book-delete-confirm.html', {'book': book})


@login_required
def book_download(request, pk):
    book = get_object_or_404(Book, pk=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, str(book.book_file))

    # Check if file exists
    if not os.path.exists(file_path):
        raise Http404("File not found.")

    # Serve the file
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response