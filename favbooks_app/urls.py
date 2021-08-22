from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('user/create', views.create_user),
    path('user/login', views.login_user),
    path('books', views.welcome),
    path('book/create', views.create_book),
    path('user/evaluate/<int:book_id>', views.evaluate_user),
    path('books/addfavorite/<int:book_id>', views.add_favorite),
    path('books/removefavorite/<int:book_id>', views.remove_favorite),
    path('books/<int:book_id>', views.details),
    path('books/user/<int:book_id>', views.user_details),
    path('books/update/<int:book_id>', views.update),
    path('<int:user_id>/delete', views.user_delete),
    #path('<int:user_id>/update', views.update_user),
    path('<int:book_id>/delete', views.book_delete),
    path('<int:this_book_id>/delete', views.book_delete1),
    path('database', views.all),
    path('logout', views.logout)
]