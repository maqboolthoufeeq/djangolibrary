from django.urls import path
from . import views
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    BookIssueView,
                    BookReturnView,
                    AllBooksView,
                    IssuedBooksView,
                    IssuerDetails,
                    SearchBook,
                    GeneratePdfAll,
                    GeneratePdfIssued,
                    BookAuthorView,
                    #BookPublisherView
                    )

urlpatterns = [
    # path('',views.home, name='blog-home'),
    path('',PostListView.as_view(), name='blog-home'),
    path('pdfgenall/',GeneratePdfAll.as_view(), name='pdf-gen-all'),
    path('pdfgenissued/',GeneratePdfIssued.as_view(), name='pdf-gen-issued'),
    # path('search_book',views.search_book,name='search-book'),
    path('search/',SearchBook.as_view(), name='search-books'),
    path('allbooks/',AllBooksView.as_view(), name='all-books'),
    path('issuedbooks/',IssuedBooksView.as_view(), name='issued-books'),
    path('post/<int:pk>/',PostDetailView.as_view(), name='post-detail'),
    path('post/<str:issue_phone_number>',IssuerDetails.as_view(), name='issuer-detail'),
    path('<str:book_author>',BookAuthorView.as_view(), name='book-author-detail'),
    # path('<str:publisher>',BookPublisherView.as_view(), name='book-publisher-detail'),
    path('post/new/',PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/issue/',BookIssueView.as_view(), name='book-issue'),
    path('post/<int:pk>/return/',BookReturnView.as_view(), name='book-return'),
    path('about/',views.about, name='blog-about'),
]
