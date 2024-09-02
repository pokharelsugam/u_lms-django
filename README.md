# Django User Based Library Management System

A comprehensive user based Library Management System built with Django. This project includes functionalities for managing books, authors, categories, publishers, and languages. It also features search functionalities to easily find books based on various criteria.

## Features

- User based permission like teacher, student and admin.
- Add, update, and delete books, authors, categories, publishers, and languages.
- Search books by name, author, category, publisher, ISBN
- File upload for book files and download
- Recently added books display on the homepage
- Mobile friendly responsive design.

## Project Structure


<pre><code>

Coming Soon
      
</code></pre>
## Getting Started

### Prerequisites

- Python 3.6+
- Django 3.2+
- Git

### Installation

1. Install Python
2. Install Django
   <pre><code>
   pip install django
   </code></pre>
3. Install Django PhoneNumberField
   <pre><code>
   pip install django-phonenumber-field
   </code></pre>   
4. Install Virtual Environment
   <pre><code>
   pip install virtualenv
   </code></pre>   
6. Clone the repository
   <pre><code>
   git clone https://github.com/pokharelsugam/elibrary-django.git
   cd elibrary-django
   </code></pre>
8. Create a virtual environment and activate it.
   <pre><code>
   virtualenv env
   env\scripts\activate
   pip install django
   pip install django-phonenumber-field
   </code></pre>
10. Run the migrations
    <pre><code>
    python manage.py makemigrations #may or may not be required
    python manage.py migrate	#must be required
    </code></pre>
12. Create a superuser
    <pre><code>
    python manage.py createsuperuser
    </code></pre>
14. Start the development server
    <pre><code>
    python manage.py runserver
    </code></pre>

## Usage
<ul>
<li>Navigate to http://127.0.0.1:8000/admin to access the admin interface and manage your library data.</li>
<li>Login with superuser account.</li>
<li>Create teacher/student from registration form.</li>
<li>Use the navigation bar to add and view books, authors, categories, publishers, and languages.</li>
<li>Use the search functionality to find books based on various criteria.</li>
</ul>
