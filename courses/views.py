from django.shortcuts import render
from django.http import HttpResponse
from .models import Course

# Create your views here.
def index(request):
    courses = Course.objects.all()
    context = {
        'course_list': courses,
    }
    print(context)
    return render(request, 'courses/index.html', context)
