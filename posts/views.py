from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Category, Post, Author


def get_author(user):
    return Author.objects.filter(user=user).first()


def homepage(request):
    categories = Category.objects.all()[:3]
    featured = Post.objects.filter(featured=True).select_related('author')
    latest = Post.objects.select_related('author').order_by('-timestamp')[:3]
    
    context = {
        'object_list': featured,
        'latest': latest,
        'categories': categories,
    }
    return render(request, 'homepage.html', context)


def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    latest = Post.objects.select_related('author').order_by('-timestamp')[:3]
    
    context = {
        'post': post,
        'latest': latest,
    }
    return render(request, 'post.html', context)


def about(request):
    return render(request, 'about_page.html')


def search(request):
    queryset = Post.objects.select_related('author').all()
    query = request.GET.get('q', '').strip()
    
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    
    context = {
        'object_list': queryset,
        'query': query,
    }
    return render(request, 'search_bar.html', context)


def postlist(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts_list = Post.objects.filter(
        categories__in=[category]
    ).select_related('author').order_by('-timestamp')
    
    paginator = Paginator(posts_list, 9)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)


def allposts(request):
    posts_list = Post.objects.select_related('author').order_by('-timestamp')
    
    paginator = Paginator(posts_list, 12)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)