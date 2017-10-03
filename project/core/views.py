from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'index.html', context)

def blogs(request):
    context = {}
    return render(request, 'blogs.html', context)

def posts(request):
    context = {}
    return render(request, 'posts.html', context)

def post_page(request, id):
    context = {'Id' : id}
    return render(request, 'post_page.html', context)

def user_profile(request):
    context = {}
    return render(request, 'user_profile.html', context)




