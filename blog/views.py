from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import (ListView,
                                DetailView,
                                CreateView,
                                UpdateView,
                                DeleteView)
from .models import Post, BookIssue
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from librarymgmt.utils import render_to_pdf #created in step 4

from datetime import datetime

# Create your views here.

def home(request):
    context={'posts': Post.objects.all()}

    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['title']

    paginate_by = 10


class AllBooksView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/all_books.html'
    context_object_name = 'posts'
    ordering = ['title']
    paginate_by = 10

class IssuedBooksView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/issued_books.html'
    context_object_name = 'posts'
    ordering = ['title']
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post

class IssuerDetails(ListView):
    # model = BookIssue

    def get_queryset(self):
        model = BookIssue.objects.filter(issue_phone_number=self.kwargs.get("issue_phone_number"))
        return model


    template_name = 'blog/issuer_details.html'
    context_object_name = 'model'
    # def get_queryset(self):
    #     user = get_object_or_404(BookIssue, issue_name=self.kwargs.get('issue_name'==self.request.))
    #     return BookIssue.objects.filter(issue_name=user)


class BookAuthorView(ListView):
    model = Post

    def get_queryset(self):
        model = Post.objects.filter(book_author=self.kwargs.get("book_author"))
        return model


    template_name = 'blog/book_authors.html'
    context_object_name = 'model'

# class BookPublisherView(ListView):
#     model = Post
#
#     def get_queryset(self):
#         model = Post.objects.filter(publisher=self.kwargs.get("publisher"))
#         return model
#
#
#     template_name = 'blog/book_publisher.html'
#     context_object_name = 'model'

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','book_author','publisher','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BookIssueView(LoginRequiredMixin,CreateView,Post):
    model = BookIssue

    fields = ['issue_name','issue_email','issue_phone_number','issue_address']
    def form_valid(self, form):
        post = Post.objects.get(id=self.kwargs["pk"])
        post.issued=True
        post.issued_to=form.instance.issue_name
        post.issue_to_phone_number=form.instance.issue_phone_number
        post.issued_on=datetime.now()
        post.save()
        response = super().form_valid(form)
        # form.instance.issued_book.add(post)
        return response
        # post = Post.objects.filter(author=self.request.user).update(issued=True)
        # form.instance.author = self.request.user

        # return super().form_valid(form)


class BookReturnView(LoginRequiredMixin,CreateView,Post):
    model = BookIssue
    template_name = 'blog/bookreturn_form.html'
    fields = []
    def form_valid(self, form):
        post = Post.objects.get(id=self.kwargs["pk"])
        post.issued=False
        post.issued_to=""
        post.issue_to_phone_number=""
        post.save()
        return super().form_valid(form)
# class BookReturnView(LoginRequiredMixin,CreateView,Post):
#     model = BookIssue
#     template_name = 'blog/bookreturn_form.html'
#     fields = []
#     def form_valid(self, form):
#         post = Post.objects.filter(author=self.request.user).update(issued=False)
#         form.instance.author = self.request.user
#         post = Post.objects.filter(author=self.request.user).update(issued_to="")
#         post = Post.objects.filter(author=self.request.user).update(issue_to_phone_number="")
#         return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','book_author','publisher','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class SearchBook(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['title']

    def get_queryset(self): # new
        return Post.objects.filter(
                                 Q(title__icontains=self.request.GET.get('q')) |
                                 Q(book_author__icontains=self.request.GET.get('q')) |
                                 Q(publisher__icontains=self.request.GET.get('q')) |
                                 Q(content__icontains=self.request.GET.get('q'))|
                                 Q(issue_to_phone_number=self.request.GET.get('q'))
                                 )

# def search_book(request):
#     queryset_list = Post.objects.all().order_by('-date_posted')
#     query = request.GET.get("q")
#     if query:
#         queryset_list = queryset_list.filter(Q(title__icontains=request.GET.get('q')) |
#                                              Q(book_author__icontains=request.GET.get('q')) |
#                                              Q(publisher__icontains=request.GET.get('q')) |
#                                              Q(content__icontains=request.GET.get('q'))|
#                                              Q(issue_to_phone_number=request.GET.get('q'))
#                                             )
#
#     return render(request,'blog/home.html',{'posts':queryset_list})
#
# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         data = {
#              'today': 'datetime.date.today()',
#              'amount': 39.99,
#             'customer_name': 'Cooper Mann',
#             'order_id': 1233434,
#         }
#         pdf = render_to_pdf('pdf/invoice.html', data)
#         return HttpResponse(pdf, content_type='application/pdf')

class GeneratePdfIssued(View):

    def get(self, request, *args, **kwargs):

        posts = Post.objects.all().order_by('title')

        template = get_template('pdf/invoiceissued.html')
        context = {'posts': posts
        }
        html = template.render(context)
        pdf = render_to_pdf('pdf/invoiceissued.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Book_Details%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            # response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

class GeneratePdfAll(View):

    def get(self, request, *args, **kwargs):

        posts = Post.objects.all().order_by('title')

        template = get_template('pdf/invoiceall.html')
        context = {'posts': posts
        }
        html = template.render(context)
        pdf = render_to_pdf('pdf/invoiceall.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Book_Details%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            # response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

def about(request):
    return render(request,'blog/about.html',{'title':'About'})
