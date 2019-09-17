from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    book_author = models.CharField(default="",max_length=100)
    publisher = models.CharField(default="",max_length=100)
    content = models.TextField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    issued = models.BooleanField(default=False)
    issued_to = models.CharField(default="",max_length=100,null=False)
    issue_to_phone_number = models.CharField(default="",max_length=10)

    issued_on = models.DateTimeField(null=True, blank=True, verbose_name='Issued on')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk' : self.pk})


class BookIssue(models.Model):
    issue_name = models.CharField(max_length=100,null=False)
    issue_email = models.EmailField(max_length=254)
    issue_phone_number = models.CharField(default="",max_length=10)
    issue_address = models.TextField(max_length=300)
    # issued_book = models.ManyToManyField(Post,default="")
    issued_book = models.CharField(default="",max_length=100)



    def __str__(self):
        return self.issue_name

    def get_absolute_url(self):
        return reverse('blog-home')
        # return reverse('blog-home', kwargs={'pk' : self.pk})
