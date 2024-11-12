from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'blog/home.html')

def post_single(request):
    return render(request, 'blog/single.html')