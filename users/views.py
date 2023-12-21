from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login, update_session_auth_hash,logout
from django.views.generic import (
    View
)
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
import os
from docxtpl import DocxTemplate
from courses.models import Course
from docx2pdf import convert
from io import BytesIO
import tempfile
import pythoncom
import threading
import win32com.client
from spire.doc import *
from spire.doc.common import *
import random
from datetime import date
from dateutil.relativedelta import relativedelta
import math,cairo
import PyPDF2
import fitz

UserModel = get_user_model()

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_account = form.save()
            return redirect('users:login')
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse_lazy('users:login'))

def send_file(request, course):
    pythoncom.CoInitialize()
    user = request.user
    course = Course.objects.get(pk=course)

    file_path = os.path.join('users', 'certificate-template.docx')
    doc = DocxTemplate(file_path)
    today = date.today()
    context = { 
        'full_name' : f"{user.first_name} {user.last_name}" ,
        'course_name': course.name,
        'n_horas': course.hours,
        'complete_date': f"{user.date_joined.date()} al {user.date_joined.date()+relativedelta(months=course.duration)}",
        'partial_date': today,
    }
    doc.render(context)
    name_file = f"{user.id}_{course.name}_{random.randint(0, 20)}.docx"
    doc.save(name_file)


    document = Document()
    document.LoadFromFile(name_file)

    document.SaveToFile('certificate3.pdf', FileFormat.PDF)
    document.Close()

    os.remove(name_file)

    doc = fitz.open('certificate3.pdf')
    for page in doc:
        # For every page, draw a rectangle on coordinates (1,1)(100,100)
        page.draw_rect([72,64,450,72],  color = (1, 1, 1), width = 8)
    # Save pdf
    doc.save('certificate5.pdf')


    with open('certificate5.pdf', 'rb') as docx_file:
        response = HttpResponse(docx_file.read(), content_type='application/pdf')

    # Set headers to indicate attachment
    response['Content-Disposition'] = 'attachment; filename="generated_doc.pdf"'
    
    return response

