# Django User Based Library Management System

A comprehensive user based Library Management System built with Django and SQLite3 or PostgreSQL. This project includes functionalities for managing books, authors, categories, publishers, and languages. It also features search functionalities to easily find books based on various criteria.

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
5. Clone the repository
   <pre><code>
   git clone https://github.com/pokharelsugam/u_elibrary-django.git
   cd elibrary-django
   </code></pre>
6. Create a virtual environment and activate it.
   <pre><code>
   virtualenv env
   env\scripts\activate
   pip install django
   pip install django-phonenumber-field
   </code></pre>
7. Run the migrations
    <pre><code>
    python manage.py makemigrations #may or may not be required
    python manage.py migrate	#must be required
    </code></pre>
8. Create a superuser
    <pre><code>
    python manage.py createsuperuser
    </code></pre>
9. Start the development server
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

## Use PostgreSQL instead of SQLite3 Database
- Do the following things before migration/creating SQLite3 Database
1. PostgreSQL
   - Install PostgreSQL in Computer, Download Link : https://www.postgresql.org/download/
   - For windows
   - Goto 'Edit the system environment variables'→ Environment Variables → System variables → Path → Edit → New → C:\Program Files\PostgreSQL\<version>\bin\ 
   - Test installation by command
     <pre><code>
           psql --version
     </code></pre> 
   - Install psycopg2. Use following code for that
     <pre><code>
           pip install psycopg2
     </code></pre>
   - Goto pgAdmin 4 app
   - Create New Server named as postgre_elibrary-django with
   - HOST : localhost
   - Password: Created duiring PostgreSQL software
   - Goto 'Login/Group Roles()'
   - Create 'Login/Group Role'
   - General → name → 'username_for_database'
   - Defination → password → 'password_for_database'
   - Privilages → Can Login → 'Yes'
   - Save
   - Goto Database()
   - Database → Create → 'Database'
   - General → Database → 'database_name', Owner → 'username_of_database'
   - Save
2. Modify Database Setting in 'settings.py' of Django
   <pre><code>
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'database_name',
        'USER': 'username_of_database',
        'PASSWORD': 'password_of_database',
        'HOST': 'localhost',
        'PORT': '5432', 
      }
   }
   </code></pre>

