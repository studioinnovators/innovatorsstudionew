import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from . import models
from django.contrib.auth.models import User
from .forms import UserForm, SyllabusDownloadForm, freeDemoForm, UserFullCourseRegistrationForm,UserMiniCourseRegistrationForm,UserPersonalDevelopmentCourseRegistrationForm,userQueryForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import time


from django.urls import reverse
from urllib.parse import urlencode
from eduPlatform.models import EventRegistration, Message

# Create your views here.
def indexView(request):
    carousel = models.HomeCarousel.objects.all()
    industrypartner = models.IndustryPartner.objects.all()
    youtube = models.YoutubeVideo.objects.all()
    minicourses = models.MiniCourse.objects.all()
    fullcourses = models.FullCourse.objects.all()
    pdpcourses = models.PersonalDevelopmentCourse.objects.all()
    topcourses = []
    for minicourse in minicourses:
        if(minicourse.avgRating>3.0):
            topcourses.append(minicourse)
    for fullcourse in fullcourses:
        if(minicourse.avgRating>3.0):
            topcourses.append(fullcourse)
    for pdpcourse in pdpcourses:
        if(pdpcourse.avgRating>3.0):
            topcourses.append(pdpcourse)
    print(topcourses)

    #### getting user and courses opted by user ####
    userCourses = []
    user = request.user
    if(user.is_authenticated):
        user_mini_courses = models.UserMiniCourse.objects.filter(user = user)
        for course in user_mini_courses:
            userCourses.append(course.mini_course)
        user_full_courses = models.UserFullCourse.objects.filter(user=user)
        for course in user_full_courses:
            userCourses.append(course.full_course)
            userfullcourse = models.MiniCoursesInFullCourse.objects.filter(full_course = course.full_course)
            for c in userfullcourse:
                userCourses.append(c.mini_course)
    
    if(request.method == 'POST'):
        search_q = request.POST.get('search-query')       
        base_url = reverse('search') 
        query_string =  urlencode({'search_q': search_q})  
        url = '{}?{}'.format(base_url, query_string) 
        return redirect(url)


    context = {
                'demoform':freeDemoForm,
                'carousels':carousel,
                'industrypartners':industrypartner,
                'minicourses':minicourses, 
                'fullcourses':fullcourses, 
                'pdpcourses':pdpcourses,
                'topcourses':topcourses,
                'youtubevideos':youtube,
                'user':user, 
                'userCourses':userCourses, 
             }
    return render(request, 'eduPlatform/index.html', context)

def aboutUs(request):
    pdfs = models.moreAboutPdf.objects.all() 
    context = {
        'pdfs':pdfs,
        'demoform':freeDemoForm,
    }
    return render(request, 'eduPlatform/aboutUs.html', context)

def searchView(request):
    title = request.GET.get('search_q')   
    result_courses = [course for course in models.MiniCourse.objects.filter(description__icontains=title)]
    result_courses.extend([course for course in models.FullCourse.objects.filter(description__icontains=title)])
    result_courses.extend([course for course in models.PersonalDevelopmentCourse.objects.filter(description__icontains=title)])
    
    userCourses = []
    user = request.user
    if(user.is_authenticated):
        user_mini_courses = models.UserMiniCourse.objects.filter(user = user)
        for course in user_mini_courses:
            userCourses.append(course.mini_course)
        user_full_courses = models.UserFullCourse.objects.filter(user=user)
        for course in user_full_courses:
            userCourses.append(course.full_course)
            userfullcourse = models.MiniCoursesInFullCourse.objects.filter(full_course = course.full_course)
            for c in userfullcourse:
                userCourses.append(c.mini_course)     

    context={
        'title':title, 
        "result_courses":result_courses, 
        'demoform':freeDemoForm,
        'userCourses':userCourses,
        }
    return render(request, 'eduPlatform/searchView.html',context)

def courseDetailView(request, id, title):  
    rate_flag = False
    paidFlag=False
    rating=0
    given_review=""
    getsyllabusForm = SyllabusDownloadForm() 
    course = models.MiniCourse.objects.get(id=id, title=title) 
    allreviews = models.MiniCourseRating.objects.filter(mini_course = course)
    userCourses = []
    user = request.user
    if(user.is_authenticated):
        user_mini_courses = models.UserMiniCourse.objects.filter(user = user)
        for m_course in user_mini_courses:
            userCourses.append(m_course.mini_course)            
        user_full_courses = models.UserFullCourse.objects.filter(user=user)
        for f_course in user_full_courses:
            userCourses.append(f_course.full_course)
            userfullcourse = models.MiniCoursesInFullCourse.objects.filter(full_course = f_course.full_course)
            for c in userfullcourse:
                userCourses.append(c.mini_course)
        try:
            rating = models.MiniCourseRating.objects.get(user = user, mini_course=course).points_given
            rate_flag=True
        except:
            rating = 0
    
    if(course in userCourses):
        try:
            given_review = models.MiniCourseRating.objects.get(user=user, mini_course=course).review
        except:
            given_review=""
        paidStatus = models.UserMiniCourse.objects.get(user=user, mini_course=course)
        if(paidStatus.paid):
            paidFlag = True

    if(request.method == 'POST'):
        if('getSyllabus' in request.POST):
            getsyllabusForm = SyllabusDownloadForm(request.POST)
            if(getsyllabusForm.is_valid()):
                getsyllabusForm.save()
                
            return redirect('/media/'+str(course.syllabus))
        elif('rateBtn' in request.POST):
            rating = request.POST.get('rating')
            review = request.POST.get('review')
            rating_given = models.MiniCourseRating.objects.create(
                points_given=int(rating),
                user = request.user,
                mini_course = course,
                review = review,
            )
            rating_given.save()
            rate_flag = True   

        elif('reRate' in request.POST):
            rating = request.POST.get('rating')
            review = request.POST.get('review')
            rating_given = models.MiniCourseRating.objects.get(
                user = request.user,
                mini_course = course,
            )
            rating_given.points_given = rating
            rating_given.review = review
            rating_given.save()
            rate_flag = True 


    context = {
                'course':course,
                'userCourses':userCourses,
                'getsyllabusForm':getsyllabusForm,
                'demoform':freeDemoForm,
                'paidFlag':paidFlag,               
                'rating':rating,
                'rate_flag': rate_flag,
                'rangeRating':range(int(rating)),
                "given_review":given_review,
                "allreviews":allreviews,
            }

    return render(request, 'eduPlatform/courseDetail.html', context)

def pdpCourseDetailView(request, id, title):  
    rate_flag = False
    paidFlag=False
    rating=0
    given_review=""
    getsyllabusForm = SyllabusDownloadForm() 
    course = models.PersonalDevelopmentCourse.objects.get(id=id, title=title) 
    #allreviews = models.PersonalDevelopmentCourseRating.objects.filter(pdp_course = course)
    userCourses = []
    user = request.user
    if(user.is_authenticated):
        user_pdp_courses = models.UserPersonalDevelopmentCourse.objects.filter(user = user)
        for m_course in user_pdp_courses:
            userCourses.append(m_course.pdp_course)            
        user_full_courses = models.UserFullCourse.objects.filter(user=user)
        for f_course in user_full_courses:
            userCourses.append(f_course.full_course)
            userfullcourse = models.PersonalDevelopmentCoursesInFullCourse.objects.filter(full_course = f_course.full_course)
            for c in userfullcourse:
                userCourses.append(c.pdp_course)
        try:
            rating = models.PersonalDevelopmentCourseRating.objects.get(user = user, pdp_course=course).points_given
            rate_flag=True
        except:
            rating = 0
    
    if(course in userCourses):
        try:
            given_review = models.PersonalDevelopmentRating.objects.get(user=user, pdp_course=course).review
        except:
            given_review=""
        paidStatus = models.UserPersonalDevelopmentCourse.objects.get(user=user, pdp_course=course)
        if(paidStatus.paid):
            paidFlag = True

    if(request.method == 'POST'):
        if('getSyllabus' in request.POST):
            getsyllabusForm = SyllabusDownloadForm(request.POST)
            if(getsyllabusForm.is_valid()):
                getsyllabusForm.save()
                
            return redirect('/media/'+str(course.syllabus))
        elif('rateBtn' in request.POST):
            rating = request.POST.get('rating')
            review = request.POST.get('review')
            rating_given = models.PersonalDevelopmentCourseRating.objects.create(
                points_given=int(rating),
                user = request.user,
                pdp_course = course,
                review = review,
            )
            rating_given.save()
            rate_flag = True   

        elif('reRate' in request.POST):
            rating = request.POST.get('rating')
            review = request.POST.get('review')
            rating_given = models.PersonalDevelopmentCourseRating.objects.get(
                user = request.user,
                pdp_course = course,
            )
            rating_given.points_given = rating
            rating_given.review = review
            rating_given.save()
            rate_flag = True 


    context = {
                'course':course,
                'userCourses':userCourses,
                'getsyllabusForm':getsyllabusForm,
                'demoform':freeDemoForm,
                'paidFlag':paidFlag,               
                'rating':rating,
                'rate_flag': rate_flag,
                'rangeRating':range(int(rating)),
                "given_review":given_review,
                #"allreviews":allreviews,
            }

    return render(request, 'eduPlatform/pdpcoursedetail.html', context)

def fullCourseDetailView(request, id, title):
    rate_flag = False
    rating=0
    course = models.FullCourse.objects.get(id=id, title=title)
    userCourses = []
    user = request.user
    given_review = ""
    allreviews = models.FullCourseRating.objects.filter(full_course = course)
    if(user.is_authenticated):
        user_mini_courses = models.UserMiniCourse.objects.filter(user = user)
        for m_course in user_mini_courses:
            userCourses.append(m_course.mini_course)            
        user_full_courses = models.UserFullCourse.objects.filter(user=user)
        for f_course in user_full_courses:
            userCourses.append(f_course.full_course)
            userfullcourse = models.MiniCoursesInFullCourse.objects.filter(full_course = f_course.full_course)
            for c in userfullcourse:
                userCourses.append(c.mini_course)
        try:
            rating = models.MiniCourseRating.objects.get(user = user, mini_course=course).points_given
            rate_flag=True
        except:
            rating = 0

    miniCourseInFull = models.MiniCoursesInFullCourse.objects.filter(full_course = course)
    mini_course_list = []
    for miniCourse in miniCourseInFull:
        mini_course_list.append(miniCourse.mini_course)

    paidFlag = False
    if(course in userCourses):
        try:
            given_review = models.FullCourseRating.objects.get(user=user, mini_course=course).review
        except:
            given_review=""
        paidStatus = models.UserFullCourse.objects.get(user=user, full_course=course)
        if(paidStatus.paid):
            paidFlag = True
    
    getsyllabusForm = SyllabusDownloadForm() 
    if(request.method == 'POST'):
        if('getSyllabus' in request.POST):
            getsyllabusForm = SyllabusDownloadForm(request.POST)
            if(getsyllabusForm.is_valid()):
                getsyllabusForm.save()
                
            return redirect('/media/'+str(course.syllabus))
        elif('rateBtn' in request.POST):
            rating = request.POST.get('rating')
            review = request.POST.get('review')
            rating_given = models.FullCourseRating.objects.create(
                points_given=int(rating),
                user = request.user,
                full_course = course,
                review = review
            )
            rating_given.save()
            rate_flag = True   

        elif('reRate' in request.POST):
            rating = request.POST.get('rating')
            review = request.POST.get('review')
            rating_given = models.FullCourseRating.objects.get(
                user = request.user,
                full_course = course,
                
            )
            rating_given.points_given = rating
            rating_given.review = review
            rating_given.save()
            rate_flag = True 

    context = {
        "course":course,
        "userCourses":userCourses,
        "mini_course_list":mini_course_list,
        'getsyllabusForm':getsyllabusForm,
        "paidFlag":paidFlag,
        'rating':rating,
        'rate_flag': rate_flag,
        'rangeRating':range(int(rating)),
        'demoform':freeDemoForm,
        "given_review":given_review,
        "allreviews":allreviews
    }
    return render(request, "eduPlatform/fullCourseDetail.html", context)

def signup(request):
    userForm = UserForm()
    if(request.user.is_authenticated):
        return redirect('home')

    if(request.method == 'POST'):
        userForm = UserForm(request.POST)
        
        if(userForm.is_valid()):
            user = userForm.save()
            user.email = user.username            
            user.save()   
            # send_mail(
            # 'Innovator Studio - SignUp confirmation',
            # '',
            # 'from',
            # [user.email],
            # fail_silently=False,
            # )   
            user = authenticate(request, username=userForm.cleaned_data['username'], password=userForm.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
    
    context={
        'userForm':userForm,
        'demoform':freeDemoForm,
    }
            
    return render(request, 'eduPlatform/signup.html', context)

def registerationView(request):
    courseId, courseTitle = request.GET.get('courseEnrollBtn').split(',')
    mode = request.GET.get('courseMode')
    userForm = UserForm()
    userMiniCourseRegistrationForm = UserMiniCourseRegistrationForm()
    userFullCourseRegistrationForm = UserFullCourseRegistrationForm()
    userPersonalDevelopmentCourseRegistrationForm = UserPersonalDevelopmentCourseRegistrationForm()

    if models.MiniCourse.objects.filter(id=courseId, title=courseTitle.strip()).exists():
        course = models.MiniCourse.objects.get(id=courseId, title=courseTitle.strip())
        fullCourseFlag = False
        miniCourseFlag = True
        pdpCourseFlag = False
    elif models.FullCourse.objects.filter(id=courseId, title=courseTitle.strip()).exists():
        course = models.FullCourse.objects.get(id=courseId, title=courseTitle.strip())
        fullCourseFlag = True
        miniCourseFlag = False
        pdpCourseFlag = False
    else:
        course = models.PersonalDevelopmentCourse.objects.get(id=courseId, title=courseTitle.strip())
        fullCourseFlag = False
        miniCourseFlag = False
        pdpCourseFlag = True

    if(request.method == 'POST'):
        if(not request.user.is_authenticated):
            userForm = UserForm(request.POST)
            if(fullCourseFlag):
                userFullCourseRegistrationForm = UserFullCourseRegistrationForm(request.POST)
                if(userForm.is_valid() and userFullCourseRegistrationForm.is_valid()):
                    user = userForm.save()
                    user.email = user.username
                    user.save()
                    details = userFullCourseRegistrationForm.save()
                    details.user = user
                    details.mode = mode
                    details.full_course = course
                    details.save()
                    mini_in_full = models.MiniCoursesInFullCourse.objects.filter(full_course = course)
                    for mini_course in mini_in_full:
                        miniC = models.UserMiniCourse.objects.create(
                            mini_course=mini_course.mini_course, 
                            user=user,
                            mode=mode,
                            phone_no=details.phone_no,
                            )
                        miniC.save()
                #     send_mail(
                #     'Innovator Studio - Registration Confirm for'+selectedCourse.title,
                #     '',
                #     'from',
                #     [user.email],
                #     fail_silently=False,
                # )                    
                    messages.success(request, user.username+" sucessfully registered for "+course.title)
                    return redirect('confirmRegistration')
            elif miniCourseFlag:
                userMiniCourseRegistrationForm = UserMiniCourseRegistrationForm(request.POST)
                if(userForm.is_valid() and userMiniCourseRegistrationForm.is_valid()):
                    user = userForm.save()
                    user.email = user.username
                    user.save()
                    details = userMiniCourseRegistrationForm.save()
                    details.user = user
                    details.mode = mode
                    details.mini_course = course
                    details.save()
                #     send_mail(
                #     'Innovator Studio - Registration Confirm for'+selectedCourse.title,
                #     '',
                #     'from',
                #     [user.email],
                #     fail_silently=False,
                # )                    
                    messages.success(request, user.username+" sucessfully registered for "+course.title)
                    return redirect('confirmRegistration')
            else:
                userPersonalDevelopmentCourseRegistrationForm = UserPersonalDevelopmentCourseRegistrationForm(request.POST)
                if(userForm.is_valid() and userPersonalDevelopmentCourseRegistrationForm.is_valid()):
                    user = userForm.save()
                    user.email = user.username
                    user.save()
                    details = userPersonalDevelopmentCourseRegistrationForm.save()
                    details.user = user
                    details.mode = mode
                    details.pdp_course = course
                    details.save()
                #     send_mail(
                #     'Innovator Studio - Registration Confirm for'+selectedCourse.title,
                #     '',
                #     'from',
                #     [user.email],
                #     fail_silently=False,
                # )                    
                    messages.success(request, user.username+" sucessfully registered for "+course.title)
                    return redirect('confirmRegistration')
        else:
            user = request.user
            if(fullCourseFlag):
                userFullCourseRegistrationForm = UserFullCourseRegistrationForm(request.POST)
                if(userFullCourseRegistrationForm.is_valid()):                    
                    details = userFullCourseRegistrationForm.save()
                    details.user = user
                    details.mode = mode
                    details.full_course = course
                    details.save()
                    mini_in_full = models.MiniCoursesInFullCourse.objects.filter(full_course = course)
                    for mini_course in mini_in_full:
                        miniC = models.UserMiniCourse.objects.create(
                            mini_course=mini_course.mini_course, 
                            user=user,
                            mode=mode,
                            phone_no=details.phone_no,
                            )
                        miniC.save()
                #     send_mail(
                #     'Innovator Studio - Registration Confirm for'+course.title,
                #     '',
                #     'from',
                #     [user.email],
                #     fail_silently=False,
                # )                    
                    messages.success(request, user.username+" sucessfully registered for "+course.title)
                    return redirect('confirmRegistration')
            elif miniCourseFlag:
                userMiniCourseRegistrationForm = UserMiniCourseRegistrationForm(request.POST)
                if(userMiniCourseRegistrationForm.is_valid()):
                    details = userMiniCourseRegistrationForm.save()
                    details.user = user
                    details.mode = mode
                    details.mini_course = course
                    details.save()
                #     send_mail(
                #     'Innovator Studio - Registration Confirm for'+course.title,
                #     '',
                #     'from',
                #     [user.email],
                #     fail_silently=False,
                # )                    
                    messages.success(request, user.username+" sucessfully registered for "+course.title)
                    return redirect('confirmRegistration')
            else:
                userPersonalDevelopmentCourseRegistrationForm = UserPersonalDevelopmentCourseRegistrationForm(request.POST)
                if(userPersonalDevelopmentCourseRegistrationForm.is_valid()):
                    details = userPersonalDevelopmentCourseRegistrationForm.save()
                    details.user = user
                    details.mode = mode
                    details.pdp_course = course
                    details.save()
                #     send_mail(
                #     'Innovator Studio - Registration Confirm for'+course.title,
                #     '',
                #     'from',
                #     [user.email],
                #     fail_silently=False,
                # )                    
                    messages.success(request, user.username+" sucessfully registered for "+course.title)
                    return redirect('confirmRegistration')

        

    context = { 
            'course':course, 
            'userForm':userForm, 
            'userMiniCourseRegistrationForm': userMiniCourseRegistrationForm, 
            'userFullCourseRegistrationForm': userFullCourseRegistrationForm, 
            'userPersonalDevelopmentCourseRegistrationForm': userPersonalDevelopmentCourseRegistrationForm,
            'fullCourseFlag':fullCourseFlag,
            'demoform':freeDemoForm,
            }
    return render(request, 'eduPlatform/register.html', context)

def confirmRegistation(request):
    context = {
        'demoform':freeDemoForm,
    }
    return render(request, 'eduPlatform/confirmRegistration.html', context)

def unEnrollView(request, id, title):
    
    try:
        course=models.MiniCourse.objects.get(id=id, title=title)
        fullCourseFlag = False
    except:
        course=models.FullCourse.objects.get(id=id, title=title)
        fullCourseFlag = True
    if(request.method == 'POST'):
        username=request.POST.get('username')
        email=request.POST.get('email')
        user=User.objects.get(username=username, email=email)
        if(fullCourseFlag):
            userCourses = models.UserFullCourse.objects.filter(user=user, full_course=course)
            for userCourse in userCourses:
                mini_in_full = models.MiniCoursesInFullCourse.objects.filter(full_course=course)
                for miniCourse in mini_in_full:
                    userminiCourse = models.UserMiniCourse.objects.get(mini_course=miniCourse.mini_course)
                    userminiCourse.delete()
            userCourse.delete()
        else:
            userCourse = models.UserMiniCourse.objects.get(user=user, mini_course=course)
            userCourse.delete()       

        return redirect('home')
    context = {
        'demoform':freeDemoForm,
    }

    return render(request, 'eduPlatform/unEnrollView.html', context)

def loginView(request):
    if(request.user.is_authenticated):
        return redirect('home') 

    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Invalid Username or Password")
            return redirect('login')
    context = {
        'demoform':freeDemoForm,
    }
    return render(request, 'eduPlatform/login.html', context)

def logoutView(request):
    logout(request)
    return redirect('home')

def allFullCoursesView(request):
    courses = models.FullCourse.objects.all()
    userCourses=[]
    if(request.user.is_authenticated):
        userFullCourses = models.UserFullCourse.objects.filter(user = request.user)
        for course in userFullCourses:
            userCourses.append(course.full_course)    

    context = {
        "courses":courses,
        "userCourses":userCourses,
        'demoform':freeDemoForm,
    }

    return render(request, 'eduPlatform/allFullCourses.html', context)

def allMiniCoursesView(request):
    courses = models.MiniCourse.objects.all()
    userCourses=[]
    if(request.user.is_authenticated):
        userMiniCourses = models.UserMiniCourse.objects.filter(user = request.user)
        for course in userMiniCourses:
            userCourses.append(course.mini_course)    

    context = {
        "courses":courses,
        "userCourses":userCourses,
        'demoform':freeDemoForm,
    }

    return render(request, 'eduPlatform/allMiniCourses.html', context)


@login_required(login_url='login')
def dashboardView(request, username, id):
    user = request.user
    allTag = True
    miniTag=False
    fullTag=False
    liveTag=False
    events = models.Event.objects.all()
    new_events = []
    for event in events:
        if(event.date.month>=datetime.datetime.now().month):
            if(event.date.day>=datetime.datetime.now().day):
                new_events.append(event)
                     
    queryForm = userQueryForm()
    queries = models.UserQuery.objects.filter(user = user)
    if(request.method == 'POST'):
        if('queryBtn' in request.POST):
            queryForm = userQueryForm(request.POST)
            if(queryForm.is_valid):    
                queryform = queryForm.save()
                queryform.user = user
                queryform.save()
                return redirect('/'+username+'/'+str(id)+'/dashboard')

        if('livecourse' in request.POST ):
            liveTag = True
            allTag = False
            userFullCourses = models.UserFullCourse.objects.filter(user=user, mode = "liveO2O") 
            userMiniCourses = models.UserMiniCourse.objects.filter(user=user,  mode = "liveO2O")
            courses = [course for course in userFullCourses]
            courses.extend([course for course in userMiniCourses])
            context={
                "courses":courses,
                "demoform":freeDemoForm,
                "allTag":allTag,
                "miniTag": miniTag,
                "fullTag": fullTag,
                "liveTag": liveTag,
                "events":new_events,
                "queryForm":queryForm,
                "queries":queries,
            }
            return render(request, 'eduPlatform/dashboard.html', context)
        if('fullcourse' in request.POST ):
            fullTag = True
            allTag = False
            userFullCourses = models.UserFullCourse.objects.filter(user=user)            
            courses = [course for course in userFullCourses]            
            context={
                "courses":courses,
                "demoform":freeDemoForm,
                "allTag":allTag,
                "miniTag": miniTag,
                "fullTag": fullTag,
                "liveTag": liveTag,
                "events":new_events,
                "queryForm":queryForm,
                "queries":queries,
            }
            return render(request, 'eduPlatform/dashboard.html', context)
        if('minicourse' in request.POST ):
            miniTag = True
            allTag = False
            userMiniCourses = models.UserMiniCourse.objects.filter(user=user)            
            courses = [course for course in userMiniCourses]            
            context={
                "courses":courses,
                "demoform":freeDemoForm,
                "allTag":allTag,
                "miniTag": miniTag,
                "fullTag": fullTag,
                "liveTag": liveTag,
                "events":new_events,
                "queryForm":queryForm,
                "queries":queries,
            }
            return render(request, 'eduPlatform/dashboard.html', context)

    userFullCourses = models.UserFullCourse.objects.filter(user=user) 
    userMiniCourses = models.UserMiniCourse.objects.filter(user=user)
    courses = [course for course in userFullCourses]
    courses.extend([course for course in userMiniCourses])
    certificates = [course.certificate for course in courses]
    context={
       "courses":courses,
        "demoform":freeDemoForm,
        "allTag":allTag,
                "miniTag": miniTag,
                "fullTag": fullTag,
                "liveTag": liveTag,
                "certificates":certificates,
                "events":new_events,
                "queryForm":queryForm,
                "queries":queries,
            }
    return render(request, 'eduPlatform/dashboard.html', context)

def allPDPCoursesView(request):
    courses = models.PersonalDevelopmentCourse.objects.all()
    userCourses=[]
    if(request.user.is_authenticated):
        userMiniCourses = models.UserPersonalDevelopmentCourse.objects.filter(user = request.user)
        for course in userMiniCourses:
            userCourses.append(course.mini_course)    

    context = {
        "courses":courses,
        "userCourses":userCourses,
        'demoform':freeDemoForm,
    }

    return render(request, 'eduPlatform/allPDPCourses.html', context)

@login_required(login_url='login')
def startCourseView(request, username, course_id, title):
    course = models.MiniCourse.objects.get(id=course_id, title=title)
    userCourse = models.UserMiniCourse.objects.get(user = request.user, mini_course=course)     
    context={        
        'course':course,
        "userCourse":userCourse,
        'demoform':freeDemoForm,
    }

    return render(request, 'eduPlatform/startcourse.html', context)

def liveSessionView(request):
    liveminicourses = models.MiniCourse.objects.filter(live_one_to_one=True)    
    livecourses=[courses for courses in liveminicourses]
    showCourse = None
    selectedcourse = None
    if(len(livecourses)>0):
        showCourse = livecourses[0].title
        selectedcourse = livecourses[0]
    userCourses = []
    user = request.user
    if(user.is_authenticated):
        user_mini_courses = models.UserMiniCourse.objects.filter(user = user)
        for course in user_mini_courses:
            userCourses.append(course.mini_course)

    if(request.method == 'POST'):      
        showCourse = request.POST.get('course').split(',-,')[0]
        showCourseid = request.POST.get('course').split(',-,')[1]
        try:
            selectedcourse = models.MiniCourse.objects.get(id=showCourseid, title=showCourse)
        except:
            selectedcourse = models.FullCourse.objects.get(id=showCourseid, title=showCourse)

        context = {
            'livecourses':livecourses,
            'showCourse':showCourse,
            'selectedcourse':selectedcourse,
            'userCourses':userCourses, 
            'demoform':freeDemoForm,         
        }
        return render(request, 'eduPlatform/liveSessions.html', context)

    context={
        'showCourse':showCourse,
        'livecourses':livecourses,
        'selectedcourse':selectedcourse,
        'demoform':freeDemoForm,
    }
    return render(request, 'eduPlatform/liveSessions.html', context)

def freeDemoSignUp(request):
    context = {'demoform':freeDemoForm,}
    if(request.method=='POST'):
        freedemoform = freeDemoForm(request.POST)
        if(freedemoform.is_valid):
            freedemoform.save()
            return render(request, 'eduPlatform/freedemoconfirmation.html')
        else:  return redirect('home')
    return render(request, 'eduPlatform/freedemoconfirmation.html', context)

def eventListView(request):
    events = models.Event.objects.all()

    context = {
        'events':events,
        'demoform':freeDemoForm,
    }
    return render(request, 'eduPlatform/Events.html', context)

def eventsdetailed(request, id, title):
    events = models.Event.objects.all()
    event1 = models.Event.objects.get(id=id, title= title)
    event1.post_views = event1.post_views + 1
    event1.save()
    if(request.method == 'POST'):
        event1 = models.Event.objects.get(id=id+1)
        context={
        'event1': event1,
        'events':events,
        }
        return render(request, 'eduPlatform/eventsdetailed.html', context)
        

    context={
        'event1': event1,
        'events':events,
    }
    return render(request, 'eduPlatform/eventsdetailed.html', context)

def eventregistration(request, title):
    event1=models.Event.objects.get(title=title)
    context={
        'event1': event1,
    }
    if request.method == 'POST':
        course = title
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        description=request.POST.get('description')
        eventregistration=EventRegistration(name=name, email=email, phone=phone, description=description, course=course, date=datetime.datetime.today())
        eventregistration.save()
        return redirect('home')
    return render(request, 'eduPlatform/eventregistration.html', context)
    
    

def policy(request):
    return render(request, 'eduPlatform/Privacy.html')

def terms(request):
    return render(request, 'eduPlatform/terms.html')
def contactus(request):
    context = {
        'messages' : messages,
    }
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        description=request.POST.get('description')
        message=Message(name=name, email=email, phone=phone, description=description, date=datetime.datetime.today())
        message.save()
        return redirect('home')
    return render(request, 'eduPlatform/contactUs.html', context)

def blogs(request):
    blogs = models.Blog.objects.all()
    context={
        'blogs':blogs,
    }
    return render(request, 'eduPlatform/blogs.html', context)

def blogsdetailed(request, id, title):
    blogs = models.Blog.objects.all()
    blog1 = models.Blog.objects.get(id=id, title= title)
    blog1.post_views = blog1.post_views + 1
    blog1.save()
    latest = models.Blog.objects.last()
    if id==latest.id:
        id=0
    blog2 = models.Blog.objects.get(id=id+1) 
    context={
        'blog1': blog1,
        'blog2': blog2,
        'blogs':blogs,
    }
    return render(request, 'eduPlatform/blogsdetailed.html', context)

def livetraining(request):
    return render(request, "eduPlatform/livetraining.html")

def selfpacedsessions(request):
    return render(request, 'eduPlatform/selfpacedsessions.html')

def inofficeprogram(request):
    return render(request, 'eduPlatform/inofficeprogram.html')