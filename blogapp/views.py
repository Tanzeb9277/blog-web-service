from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
# <HINT> Import any new Models here
from .models import Author, Post, Comment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NewCommentSerializer
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.

# Create your views here.
from django.http import HttpResponse

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'blogapp/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            Author.objects.create_user(email=email, username=username, password=password)
            login(request, user)
            return redirect("blogapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'blogapp/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blogapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'blogapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'blogapp/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('blogapp:index')


def check_if_author(user, post):
    is_author = False
    
    if user.id is not None:
        # Check if user enrolled
        
        if post.author_id == user.id:
            is_author = True
    return is_author


def create_post(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'blogapp/create_post_bootstrap.html', context)
    elif request.method == 'POST':
        print(list(request.POST))
        username = request.POST['username']
        title = request.POST['title']
        text = request.POST['text']
        author_id = Author.objects.get(username =username)
        Post.objects.create(title=title, author_name=username, author = author_id, text=text )
    return redirect('blogapp:index')

class PostListView(generic.ListView):
    template_name = 'blogapp/post_list_bootstrap.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        user = self.request.user
        author = Author.objects.filter(username = user.username)
        posts = Post.objects.order_by('date')[:10]
        for post in posts:
            if user.is_authenticated:
                post.is_author = check_if_author(author[0], post)
        return posts
    
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blogapp/post_edit_bootstrap.html'


def edit_post(request, post_id):
    context = {}
    title = request.POST['title']
    text = request.POST['text']
    Post.objects.filter(pk = post_id).update(title = title, text = text)
    return redirect('blogapp:index')
    

def AppPostList(request):
    posts = Post.objects.order_by('date').order_by('-date')
    posts_json = serializers.serialize('json', posts)
    return HttpResponse(posts_json, content_type='application/json')

def PostDetail(request, pk):
    print("working")
    post = Post.objects.filter(pk = pk)
    post_json = serializers.serialize('json', post)
    return HttpResponse(post_json, content_type='application/json')




class NewComment(APIView):
    print("working")
    serializer_class = NewCommentSerializer
    @csrf_exempt
    def post(self, request, post_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            text = serializer.data.get('text')
            post = Post.objects.get(pk = post_id)
            comment = Comment(text = text, post = post)
            comment.save()
            return Response(NewCommentSerializer(comment).data, status=status.HTTP_200_OK)
        
def GetComments(request, post_id):
    comments = Comment.objects.filter(post_id = post_id).order_by('-date')
    comments_json = serializers.serialize('json', comments)
    return HttpResponse(comments_json, content_type='application/json')