from django.shortcuts import render, redirect, HttpResponse
from .models import books, users, usermanager
from django.contrib import messages
import bcrypt

def index(request):
    request.session.flush()
    context = {
    }
    return render(request, 'register.html', context)

def create_user(request):
    if request.method != "POST":
        return redirect('/')
    errors = users.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    pw_hash = bcrypt.hashpw('password'.encode(), bcrypt.gensalt()).decode()
    new_user = users.objects.create(
        first_name = request.POST['first_name'],
        last_name= request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash
    )
    request.session['user_id'] = new_user.id
    messages.success(request, "Successfully registered. Proceed to Login.")
    return redirect('/')

def login_user(request):
    if request.method != "POST":
        return redirect('/')
    errors = users.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    this_user = users.objects.filter(email = request.POST['email'])[0]
    request.session['user_id'] = this_user.id
    return redirect('/books')

def welcome(request):
    if 'user_id' not in request.session:
        return redirect('/')
    one_user = users.objects.get(id = request.session['user_id'])
    context = {
        "this_user": one_user,
        "all_books": books.objects.all()
    }
    return render(request, 'welcome.html', context)

def create_book(request):
    if request.method != "POST":
        return redirect('/')
    errors = books.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/books')
    new_book = books.objects.create(
        title = request.POST['title'],
        description = request.POST['description'],
        uploaded_by = users.objects.get(id = request.session['user_id'])
    )
    request.session['book_id'] = new_book.id
    messages.success(request, "Book successfully added.")
    this_user = users.objects.get(id = request.session['user_id'])
    this_user.liked_books.add(new_book.id)
    new_book.users_who_like.add(this_user)
    return redirect('/books')

def evaluate_user(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = users.objects.get(id = request.session['user_id'])
    this_book = books.objects.get(id = book_id)
    if this_book.uploaded_by.id != this_user.id:
        return redirect(f'/books/{this_book.id}')
    else:
        return redirect(f'/books/user/{this_book.id}')

def add_favorite(request, book_id):
    this_book = books.objects.get(id = book_id)
    this_user = users.objects.get(id = request.session['user_id'])
    this_user.liked_books.add(this_book)
    this_book.users_who_like.add(this_user)
    if this_user.id == this_book.uploaded_by.id:
        return redirect(f'/books/user/{this_book.id}')
    else:
        return redirect(f'/books/{this_book.id}')
    

def remove_favorite(request, book_id):
    this_book = books.objects.get(id = book_id)
    this_user = users.objects.get(id = request.session['user_id'])
    this_user.liked_books.remove(this_book)
    this_book.users_who_like.remove(this_user)
    if this_user.id == this_book.uploaded_by.id:
        return redirect(f'/books/user/{this_book.id}')
    else:
        return redirect(f'/books/{this_book.id}')
        

def details(request, book_id):
    one_user = users.objects.get(id = request.session['user_id'])
    one_book = books.objects.get(id = book_id)
    context = {
    "this_book": one_book,
    "this_user": one_user,
    "all_books": books.objects.all()
    }
    return render(request, "details.html", context)

def user_details(request, book_id):
    one_user = users.objects.get(id = request.session['user_id'])
    one_book = books.objects.get(id = book_id)
    context = {
    "this_book": one_book,
    "this_user": one_user,
    "all_books": books.objects.all()
    }
    return render(request, "user_detail.html", context)

def all(request):
    context = {
    "all_users": users.objects.all(),
    "all_books": books.objects.all()
    }
    return render(request, "database.html", context)

def update (request, book_id):
    errors = books.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/books/user/{book_id}')
    else:
        updated_book =  books.objects.get(id = book_id)
        updated_book.title = request.POST['title']
        updated_book.description = request.POST['description']
        updated_book.save()
        messages.success(request, "Book successfully updated")
        return redirect(f'/books/user/{book_id}')

"""def update_user (request, user_id):
    errors = users.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/books')
    else:
        updated_user =  users.objects.get(id = user_id)
        updated_user.first_name = request.POST['first_name']
        updated_user.last_name = request.POST['last_name']
        updated_user.email = request.POST['email']
        updated_user.password = request.POST['password']
        updated_user.save()
        messages.success(request, "User info successfully updated")
        return redirect(f'/books')"""

def logout(request):
    request.session.flush()
    return redirect('/')

def book_delete(request, book_id):
    deleted_book = books.objects.get(id = book_id)
    deleted_book.delete()
    return redirect('/books')

def book_delete1(request, this_book_id):
    deleted_book = books.objects.get(id = this_book_id)
    deleted_book.delete()
    return redirect('/database')

def user_delete(request, user_id):
    deleted_user = books.objects.get(id = user_id)
    deleted_user.delete()
    return redirect('/books')
