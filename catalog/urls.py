from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('books/', views.BookListView.as_view(), name='books'),
        path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
        path('author/',views.AuthorListView.as_view(),name='author'),
        path('author/<int:pk>',views.AuthorDetailView.as_view(),name='author-detail'),
        path('genre/',views.GenreListView.as_view(),name='genre'),
        path('genre/<str:name>',views.genre_extended,name='genre-extend'),
]


urlpatterns += [   
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]
urlpatterns += [   
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [   
    path('search_student/', views.search_student, name='search-student'),
    path('search_book/', views.search_book, name='search-book'),
]
