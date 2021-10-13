from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.indexView, name='home'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('course/<int:id>/<str:title>/', views.courseDetailView, name='courseDetails'),
    path('fullcourse/<int:id>/<str:title>/', views.fullCourseDetailView, name='fullcourseDetails'),
    path('pdpcourse/<int:id>/<str:title>/', views.pdpCourseDetailView, name='pdpcourseDetails'),
    path('register/', views.registerationView, name='registeration'),
    path('confirm/', views.confirmRegistation, name='confirmRegistration'),
    path('unenroll/<int:id>/<str:title>/', views.unEnrollView, name='unenroll'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('<str:username>/<int:id>/dashboard/', views.dashboardView, name='dashboard'),
    path('allFullCourses/', views.allFullCoursesView, name='allFullcourses'),
    path('allCourses/', views.allMiniCoursesView, name='allMinicourses'),
    path('allPDPCourses/', views.allPDPCoursesView, name='allPDPcourses'),
    path('learn/<str:username>/<int:course_id>/<str:title>/', views.startCourseView, name='startcourse'),
    path('searchpath/', views.searchView, name='search'),
    path('signUp/', views.signup, name='signup'),
    path('liveSessions/', views.liveSessionView, name="livesessions"),
    path('freedemo/', views.freeDemoSignUp, name='freedemo'),
    path('events/', views.eventListView, name='events'),
    path('events/<int:id>/<str:title>/', views.eventsdetailed, name='eventsdetailed'),
    path('eventregistration/<str:title>/', views.eventregistration, name='eventregistration'),
    path('policy/', views.policy , name='policy'),
    path('terms/', views.terms , name='terms'),
    path('contactus/', views.contactus, name="contactus"),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='eduPlatform/passwordReset.html'), 
    name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='eduPlatform/passwordResetSent.html'), 
    name='password_reset_done'), 

    path('password_reset_form/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='eduPlatform/passwordResetForm.html'), 
    name='password_reset_confirm'),

    path('password_deset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='eduPlatform/passwordResetDone.html'), 
    name='password_reset_complete'),
    
    path('blogs', views.blogs, name='blogs'),
    path('blogs/<int:id>/<str:title>/', views.blogsdetailed, name='blogsdetailed'),    
    path('aboutUs/livetraining', views.livetraining, name='livetraining'),
    path('aboutUs/selfpacedsessions', views.selfpacedsessions, name='selfpacedsessions'),
    path('aboutUs/inofficeprogram', views.inofficeprogram, name='inofficeprogram'),
]
