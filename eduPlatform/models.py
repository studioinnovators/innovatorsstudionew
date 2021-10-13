from django.db import models
from django.contrib.auth.models import User
from django.db.models import query
from django.db.models.expressions import F
from datetime import datetime, date

# Create your models here.
class MiniCourse(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    fee = models.FloatField()
    thumbnail = models.FileField(upload_to='course_thumbnail/')
    syllabus = models.FileField(upload_to='course_syllabus/')
    course_preview_video = models.FileField(upload_to='course_preview_videos/', null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    offline = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
    self_paced = models.BooleanField(default=False)
    next_batch_starting_date = models.DateField(null=True)
    high_price = models.FloatField(default=0)
    class_link = models.CharField(max_length=1000, null=True, blank=True)
    
    class Meta:
        ordering = ['-date_added']   

    def __str__(self):
        return self.title

    @property
    def avgRating(self):
        ratings = self.minicourserating_set.all()
        avg=0.0
        i=0
        for rating in ratings:
            i+=1
            avg += rating.points_given
        if(i>0):
            avg = avg//i
        return avg
    
    @property
    def teacher(self):
        teacher = self.minicourseteacher_set.all()
        return teacher

    @property
    def all_topics(self):
        topics = self.topic_set.all()
        return topics

    @property
    def get_duration(self):
        topics = self.topic_set.all()
        duration = 0
        for topic in topics:
            duration += topic.duration_in_hours
        return duration

class Topic(models.Model):
    mini_course = models.ForeignKey(MiniCourse, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    duration_in_hours = models.IntegerField()
    class_link = models.CharField(max_length=1000, null=True, blank=True)
    lecture_video = models.FileField(upload_to='courseTutorials/', null=True, blank=True)

    def __str__(self):
        return str(self.mini_course) + "_" + self.title

class MiniCourseTeacher(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True)
    subject = models.ForeignKey(MiniCourse, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='minicourseteacherimages/')
    phone_no = models.CharField(max_length=11)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.first_name +" "+ self.last_name +" instructor for "+ str(self.subject)
    
class PersonalDevelopmentCourse(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    fee = models.FloatField()
    thumbnail = models.FileField(upload_to='course_thumbnail/')
    syllabus = models.FileField(upload_to='course_syllabus/')
    course_preview_video = models.FileField(upload_to='course_preview_videos/', null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    offline = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
    self_paced = models.BooleanField(default=False)
    next_batch_starting_date = models.DateField(null=True)
    high_price = models.FloatField(default=0)
    class_link = models.CharField(max_length=1000, null=True, blank=True)
    
    class Meta:
        ordering = ['-date_added']   

    def __str__(self):
        return self.title

    @property
    def avgRating(self):
        ratings = self.personaldevelopmentcourserating_set.all()
        avg=0.0
        i=0
        for rating in ratings:
            i+=1
            avg += rating.points_given
        if(i>0):
            avg = avg//i
        return avg
    @property
    def teacher(self):
        teacher = self.pdpcourseteacher_set.all()
        return teacher

    @property
    def all_topics(self):
        topics = self.pdptopic_set.all()
        return topics

    @property
    def get_duration(self):
        topics = self.pdptopic_set.all()
        duration = 0
        for topic in topics:
            duration += topic.duration_in_hours
        return duration
    
class pdpTopic(models.Model):
    pdp_course = models.ForeignKey(PersonalDevelopmentCourse, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    duration_in_hours = models.IntegerField()
    class_link = models.CharField(max_length=1000, null=True, blank=True)
    lecture_video = models.FileField(upload_to='courseTutorials/', null=True, blank=True)

    def __str__(self):
        return str(self.pdp_course) + "_" + self.title

class PDPCourseTeacher(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True)
    subject = models.ForeignKey(PersonalDevelopmentCourse, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pdpcourseteacherimages/')
    phone_no = models.CharField(max_length=11)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.first_name +" "+ self.last_name +" instructor for "+ str(self.subject)

class FullCourse(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=800,default='null')
    fee = models.FloatField() 
    thumbnail = models.FileField(upload_to='courseThumbnail/')    
    offline = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
    self_paced = models.BooleanField(default=False)
    next_batch_starting_date = models.DateField()
    course_preview_video = models.FileField(upload_to='course_preview_videos/', null=True)
    high_price = models.FloatField(default=0)

    def __str__(self):
        return self.title

    @property
    def all_topics(self):
        topics = self.fullcoursetopic_set.all()
        return topics
    
    @property
    def teacher(self):
        teacher = self.fullcourseteacher_set.all()
        return teacher

    @property
    def get_duration(self):
        topics = self.fullcoursetopic_set.all()
        duration = 0
        for topic in topics:
            duration += topic.duration_in_hours
        return duration

    @property
    def avgRating(self):
        ratings = self.fullcourserating_set.all()
        avg=0.0
        i=0
        for rating in ratings:
            i+=1
            avg += rating.points_given
        if(i>0):
            avg = avg//i
        return avg

class FullCourseTopic(models.Model):
    full_course = models.ForeignKey(FullCourse, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    duration_in_hours = models.IntegerField()
    class_link = models.CharField(max_length=1000, null=True, blank=True)
    lecture_video = models.FileField(upload_to='courseTutorials/', null=True, blank=True)

    def __str__(self):
        return str(self.full_course) + "_" + self.title
    
class FullCourseTeacher(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True)
    subject = models.ForeignKey(FullCourse, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='fullcourseteacherimages/')
    phone_no = models.CharField(max_length=11)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.first_name +" "+ self.last_name +" instructor for "+ str(self.subject)
    
class MiniCoursesInFullCourse(models.Model):
    full_course = models.ForeignKey(FullCourse, on_delete=models.CASCADE)
    mini_course = models.ForeignKey(MiniCourse, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.full_course) +"_"+ str(self.mini_course)

class PersonalDevelopmentCoursesInFullCourse(models.Model):
    full_course = models.ForeignKey(FullCourse, on_delete=models.CASCADE)
    pdp_course = models.ForeignKey(MiniCourse, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.full_course) +"_"+ str(self.pdp_course)

class UserMiniCourse(models.Model):
    mini_course = models.ForeignKey(MiniCourse, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mode = models.CharField(max_length=100, null=True)
    paid = models.BooleanField(default=False)
    phone_no = models.BigIntegerField(default=0)
    certificate = models.FileField(upload_to='userCertificates/miniCourses/', null=True, blank=True)

    def __str__(self):
        return str(self.user) + '_' + str(self.mini_course) + '_' + str(self.mode)
    
class UserPersonalDevelopmentCourse(models.Model):
    mini_course = models.ForeignKey(MiniCourse, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mode = models.CharField(max_length=100, null=True)
    paid = models.BooleanField(default=False)
    phone_no = models.BigIntegerField(default=0)
    certificate = models.FileField(upload_to='userCertificates/miniCourses/', null=True, blank=True)

    def __str__(self):
        return str(self.user) + '_' + str(self.mini_course) + '_' + str(self.mode)

class UserFullCourse(models.Model):
    full_course = models.ForeignKey(FullCourse, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mode = models.CharField(max_length=100, null=True)
    phone_no = models.BigIntegerField(default=0)
    paid = models.BooleanField(default=False)
    certificate = models.FileField(upload_to='userCertificates/fullCourses/', null=True, blank=True)

    def __str__(self):
        return str(self.user) + '_' + str(self.full_course) + '_' + str(self.mode)

    def save(self, *args, **kwargs):
        if(self.paid == True):
            mini_in_full = MiniCoursesInFullCourse.objects.filter(full_course=self.full_course)
            for mini in mini_in_full:
                userminiCourses = UserMiniCourse.objects.filter(mini_course=mini.mini_course)
                print(userminiCourses)
                for course in userminiCourses:
                    course.paid = True
                    course.save()
        else:
            mini_in_full = MiniCoursesInFullCourse.objects.filter(full_course=self.full_course)
            for mini in mini_in_full:
                userminiCourses = UserMiniCourse.objects.filter(mini_course=mini.mini_course)
                for course in userminiCourses:
                    course.paid = False 
                    course.save()           
        super(UserFullCourse, self).save(*args, **kwargs)

class MiniCourseRating(models.Model):
    POINTS = [
        (5,5),(4,4),(3,3),(2,2),(1,1)
    ]
    points_given = models.IntegerField(default=0, choices=POINTS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mini_course = models.ForeignKey(MiniCourse, on_delete=models.CASCADE)  
    review = models.TextField(null=True, blank=True)  

    def __str__(self):
        return str(self.user)

class PersonalDevelopmentCourseRating(models.Model):
    POINTS = [
        (5,5),(4,4),(3,3),(2,2),(1,1)
    ]
    points_given = models.IntegerField(default=0, choices=POINTS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mini_course = models.ForeignKey(PersonalDevelopmentCourse, on_delete=models.CASCADE)  
    review = models.TextField(null=True, blank=True)  

    def __str__(self):
        return str(self.user)

class FullCourseRating(models.Model):
    POINTS = [
        (5,5),(4,4),(3,3),(2,2),(1,1)
    ]
    points_given = models.IntegerField(default=0, choices=POINTS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_course = models.ForeignKey(FullCourse, on_delete=models.CASCADE)
    review = models.TextField(null=True, blank=True)    

    def __str__(self):
        return str(self.user)

class SyllabusDownloadData(models.Model):
    mini_course = models.ForeignKey(MiniCourse, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True)
    phone_no = models.CharField(max_length=11)
    email = models.EmailField()

    def __str__(self):
        return self.first_name

class freeDemoRegistration(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True)
    phone_no = models.CharField(max_length=11)
    email = models.EmailField()
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name    

class moreAboutPdf(models.Model):
    title = models.CharField(max_length=50)
    pdf = models.FileField(upload_to="know_more_pdf/")
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "_pdf"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    speaker = models.CharField(max_length=250, null=True, blank=True)
    date = models.DateTimeField()
    thumbnail =  models.ImageField(upload_to="event_thumbnails/", null=True, blank=True)
    poster = models.ImageField(upload_to="event_posters/", null=True, blank=True)
    image_speaker = models.ImageField(upload_to="event_speakers/", null=True, blank=True)
    about_speaker = models.TextField()
    post_views = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return "Event" + self.title
class EventRegistration(models.Model):
    course = models.TextField()
    name = models.CharField(max_length=70)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    description = models.TextField(null=True, blank=True)
    date= models.DateTimeField()
    def __str__(self):
        return self.name + " for " + self.course

class UserQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300)
    query_description = models.TextField()
    resolved = models.BooleanField(default=False, null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title

class Blogcategory(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=80,default="Un-Named")
    author = models.CharField(max_length=30,default="Unknown")
    category = models.ManyToManyField(Blogcategory,default="C Programming")
    img1 = models.ImageField(null=True)
    desc1 = models.TextField(null=True)
    img2 = models.ImageField(blank=True,null=True)
    desc2 = models.TextField(blank=True,null=True,default="")
    img3 = models.ImageField(blank=True,null=True)
    desc3 = models.TextField(blank=True,null=True,default="")
    img4 = models.ImageField(blank=True,null=True)
    desc4 = models.TextField(blank=True,null=True,default="")
    img5 = models.ImageField(blank=True,null=True)
    desc5 = models.TextField(blank=True,null=True,default="")
    date = models.DateField(auto_now_add=True,null=True)
    post_views = models.IntegerField(default=0, null=True, blank=True)
    def __str__(self):
        return self.title
    
class YoutubeVideo(models.Model):
    title = models.CharField(max_length=80,default="Un-Named")
    link = models.TextField(blank=True)
    def __str__(self):
        return self.title
    
class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    description = models.TextField(max_length=500)
    date = models.DateTimeField(null=True, default=False)
    
    def __str__(self):
        return self.name
    
class HomeCarousel(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='homecarousel/')
    link = models.URLField()
    def __str__(self):
        return self.name
    
class IndustryPartner(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='homecarousel/')
    link = models.URLField()
    def __str__(self):
        return self.name