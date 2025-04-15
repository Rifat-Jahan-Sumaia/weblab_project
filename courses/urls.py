
# from django.urls import path
# from .views import home,course_list,course_details
# urlpatterns = [
   
#     #path('courses/',include('courses.urls')),
#     path('', home, name='home'),
#     path('course-list/', course_list, name='course_list'),
#     path('course-list/<int:id>/', course_details, name='course_details'),
# ]

from django.urls import path
from .views import *
from django. contrib. auth import views as auth_views
urlpatterns = [

    path('api/enroll/', EnrollStudentAPI.as_view(), name='api_enroll_student'),
    path('api/courses/', CourseListAPI.as_view(), name='api_course_list'),
    path('api/courses/<int:pk>/', CourseDetailAPI.as_view(), name='api_course_detail'),
    path('', CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    # path('', course_list, name='course_list'),
    # path('<int:course_id>/', course_detail, name='course_detail'),
    path('enroll/', enroll_student, name = 'enroll_student'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    # path('create/', course_create, name='course_create'),
    path('<int:course_id>/update/', course_update, name='course_update'),
    path('<int:course_id>/delete/', course_delete, name='course_delete'),
    path('lesson/create/', lesson_create, name='lesson_create'),
    path('lesson/<int:lesson_id>/update/', lesson_update, name='lesson_update'),
    path('lesson/<int:lesson_id>/delete/', lesson_delete, name='lesson_delete'),
    path('<int:course_id>/students/', course_students, name='course_students'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name = 'profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='courses/password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='courses/password_change_done.html'), name='password_change_done'),
   
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='courses/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='courses/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='courses/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='courses/password_reset_complete.html'), name='password_reset_complete'),

]