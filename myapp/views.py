from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, BlogPost
from .forms import SignupForm, BlogPostForm

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.user_type == 'doctor':
                return redirect('doctor_dashboard')
            elif user.user_type == 'patient':
                return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Sign up successful. You can now log in.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

@login_required
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, 'Blog post created successfully.')
            return redirect('doctor_dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'blog_post_form.html', {'form': form})

def home(request):
    return render(request, 'home.html')

@login_required
def blog_list(request):
    # Get all non-draft blog posts
    posts = BlogPost.objects.filter(draft=False)

    # Organize posts by category
    categories = {}
    for post in posts:
        if post.category not in categories:
            categories[post.category] = []
        categories[post.category].append(post)
    
    return render(request, 'blog_list.html', {'categories': categories})

@login_required
def blog_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, 'blog_detail.html', {'post': post})

def custom_logout(request):
    # Log out the user
    auth_logout(request)
    # Redirect to the home page or any other page
    return redirect('home')
# myapp/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost

@login_required
def delete_blog(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    if request.user.user_type == 'doctor' and post.author == request.user:
        post.delete()
        return redirect('blog_list')
    else:
        # Handle the case where the user does not have permission
        return redirect('blog_list')

@login_required
def profile(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    return render(request, 'profile.html', {'user': user})