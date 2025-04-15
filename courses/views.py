from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson
from .forms import CourseForm, LessonForm, CourseEnrollmentForm, UserUpdateForm
from .models import Student
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import ListView, DetailView
from .models import Course
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CourseSerializer

class CourseListAPI(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class CourseDetailAPI(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

class EnrollStudentAPI(APIView):
    def post(self, request):
        student_email = request.data.get('email')
        course_id = request.data.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        student, created = Student.objects.get_or_create(email=student_email)
        student.enrolled_courses.add(course)
        return Response({'message': f'{student.email} has been enrolled in {course.title}'})

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['lessons'] = course.lessons.all()

        if self.request.user.is_authenticated:
            try:
                student = Student.objects.get(email=self.request.user.email)
                context['student'] = student
            except Student.DoesNotExist:
                context['student'] = None
        else:
            context['student'] = None

        return context

class CourseCreateView(CreateView):
    model = Course
    fields = ['title', 'description', 'duration', 'thumbnail']
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('/')
    else:
        form = UserCreationForm()
        
    return render(request, 'courses/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'courses/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'courses/profile.html', {'form': form})


# Course List
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

# Course Detail
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()

    student = Student.objects.filter(email=request.user.email).first()

    return render(request, 'courses/course_detail.html', {'course': course, 'lessons': lessons, 'student': student})

# Create Course
@login_required
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Course created successfully!")
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})

# Update Course
@login_required
def course_update(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form})

# Delete Course
@login_required
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

def home(request):
    return render(request, 'courses/index.html')

# def course_list(request):
#     courses= Course.objects.all()
#     return render(request,'courses/index.html',{'courses':courses})
@login_required
def course_details(request,id):
     course= get_object_or_404(Course,id=id)
     lessons=course.lessons.all()
     return render(request,'courses/course-details.html',{'lessons':lessons})
# Create your views here.

# Create Lesson
@login_required
def lesson_create(request):
    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson created successfully!")
            return redirect('course_list')
    else:
        form = LessonForm()
    return render(request, 'courses/lesson_form.html', {'form': form})

# Update Lesson
@login_required
def lesson_update(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson updated successfully!")
            return redirect('course_list')
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'courses/lesson_form.html', {'form': form})

# Delete Lesson
@login_required
def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == "POST":
        lesson.delete()
        messages.success(request, "Lesson deleted successfully!")
        return redirect('course_list')
    return render(request, 'courses/lesson_confirm_delete.html', {'lesson': lesson})

@login_required
def enroll_student(request):
    if request.method == 'POST':
        form = CourseEnrollmentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['student_email']
            name = form.cleaned_data['student_name']
            selected_courses = form.cleaned_data['course']  # ModelMultipleChoiceField in form

            # Get or create the student by email
            student, created = Student.objects.get_or_create(
                email=email,
                defaults={'name': name}
            )

            if not created:
                # Update the student's name if changed
                if student.name != name:
                    student.name = name
                    student.save()

            # Filter out courses the student is already enrolled in
            already_enrolled_courses = student.enrolled_courses.filter(id__in=[c.id for c in selected_courses])
            new_courses = [course for course in selected_courses if course not in already_enrolled_courses]

            if not new_courses:
                messages.warning(request, "this email already enrolled in the selected course(s).")
                return redirect('enroll_student')

            # Enroll student in new courses
            student.enrolled_courses.add(*new_courses)

            messages.success(request, f"Enrollment successful! You have been enrolled in {len(new_courses)} course(s).")
            return render(request, 'courses/enrollment_success.html', {
                'student': student,
                'courses': new_courses,
            })
        else:
            messages.error(request, "There was an error with your form. Please try again.")
    else:
        form = CourseEnrollmentForm()

    return render(request, 'courses/enroll_student.html', {'form': form})

@login_required
def course_students(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = course.students.all()  # reverse relation from ManyToManyField
    return render(request, 'courses/course_students.html', {
        'course': course,
        'students': students
    })

