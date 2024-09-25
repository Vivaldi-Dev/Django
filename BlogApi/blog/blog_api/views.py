from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from blog_api.models import post


def home(request):
    return render(request, 'paginas/index.html',)

def about (request):
    return render(request,'paginas/about.html',{'posts':posts})

def sobre (request):
    posts = post.objects.all()
    return render(request,'paginas/sobre.html',{'posts':posts})

def detail(request, id):
    posts = get_object_or_404(post, pk=id)
    return render(request, 'paginas/detail.html', {'post': posts})