from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from .models import Post, Music
from .forms import PostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated




@api_view(['GET', "POST"])
@permission_classes([IsAuthenticated])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




@login_required
def profile(request):
    user=request.user
    posts=Post.objects.filter(author=user)
    return render(request,'profile.html', {'user':user,'posts':posts})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)   # 🔥 MUHIM
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('/')


def blog(request):
    return render(request, 'index.html')

def home(request):
    posts = Post.objects.all().order_by('-created')

    per_page = request.GET.get('per_page', 6)

    try:
        per_page = int(per_page)
    except:
        per_page = 10

    if per_page not in [5, 20, 50, 100]:
        per_page = 5

    paginator = Paginator(posts, per_page)
    pages_number = request.GET.get('page')
    page_obj = paginator.get_page(pages_number)

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'per_page': per_page,
    })
def home_get(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'home_get.html', {'post':post})
    

def music(request):
    musics = Music.objects.all()
    return render(request, 'music.html', {'musics':musics})


@login_required # Faqat login qilganlar post qo'shishi uchun
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Formani darrov bazaga saqlamay turamiz (commit=False)
            post = form.save(commit=False)
            
            # 2. Post muallifini hozirgi foydalanuvchiga tenglaymiz
            post.author = request.user
            
            # 3. Endi bazaga saqlaymiz
            post.save()
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})
    
from django.http import HttpResponseForbidden

def update_post(request, id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("Sizda ruxsat yo‘q!")
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PostForm(instance=post)
    return render(request, 'update_post.html', {'form':form})

def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.delete()
        return redirect('/')

    return render(request, 'delete_post.html', {'post': post})

def search(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.none()  # Bo'sh queryset
    return render(request, 'search_results.html', {'posts': posts, 'query': query})

