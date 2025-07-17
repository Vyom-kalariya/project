from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

def home(request):
    searchTerm = request.GET.get('searchEnroll')
    if searchTerm:
        students = Student.objects.filter(enroll__icontains=searchTerm)
    else:
        students = Student.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'students': students})

@login_required
def detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.user.groups.filter(name='faculty').exists():
        return render(request, 'detail.html', {'student': student, 'is_faculty': True})

    if hasattr(request.user, 'student_profile') and student.user == request.user:
        return render(request, 'detail.html', {'student': student, 'is_faculty': False})

    return HttpResponseForbidden("YOU DO NOT HAVE ACCESS")

class MarksForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['Python', 'FSD', 'TOC']

@login_required
def edit_marks(request, student_id):
    if not request.user.groups.filter(name='faculty').exists():
        return HttpResponseForbidden("YOU DO NOT HAVE ACCESS")

    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = MarksForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('detail', args=[student_id]))
    else:
        form = MarksForm(instance=student)
    
    return render(request, 'edit_marks.html', {'form': form, 'student': student})

@login_required
def delete_student(request, student_id):
    if not request.user.groups.filter(name='faculty').exists():
        return HttpResponseForbidden("YOU DO NOT HAVE ACCESS")

    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        student.delete()
        return redirect('home')  # Or your desired redirect after delete

    return render(request, 'delete_student.html', {'student': student})
