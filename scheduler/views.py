from django.shortcuts import render

def calendar_view(request):
    return render(request, 'index.html')

def create_post(request):
    return render(request, 'create_post.html')
