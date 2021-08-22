from django.db import models
from django.db.models.deletion import CASCADE
from time import gmtime, strftime
import re
import bcrypt

class usermanager(models.Manager):
    def register_validator(self, postData):
        #email_regex = re.compile()
        errors = {}
        existing_users = users.objects.filter(email = postData['email'])
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        #if postData['email'] == existing_users.email[0]:
        #    errors["email"] = "This email has already been registered"
        if postData['password'] !=  postData['confirm_password']:
            errors["password"] = "Passwords do not match"
        if len(postData['password']) < 8:
            errors['pass_length'] = "Password must be at least 8 characters"
        return errors  

    def login_validator(self, postData):
        errors = {}
        existing_users = users.objects.filter(email = postData['email'])
        if len(postData['email']) == 0:
            errors["email"] = "Email Required"
        elif len(existing_users) == 0:
            errors["not_found"] = "Email not found"
        if len(postData['password']) == 0:
            errors["password"] = "password required"
        #elif not bcrypt.checkpw(postData['password'].encode(), existing_users[0].password.encode()):
        #    errors["mismatch"] = "Please reenter your email and password"
        return errors

class bookmanager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        existing_books = books.objects.filter(title = postData['title'])
        if len(postData['title']) == 0:
            errors["title"] = "Book Title required"
        if len(postData['description']) >= 0 and len(postData['description']) < 5:
            errors["description"] = "Description should be at least 5 characters"
        return errors

class users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email =  models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = usermanager()

class books(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField()
    uploaded_by = models.ForeignKey(users, related_name="books_uploaded", on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(users, related_name = "liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = bookmanager()

