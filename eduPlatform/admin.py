from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MiniCourse)
admin.site.register(Topic)
admin.site.register(MiniCourseTeacher)
admin.site.register(PersonalDevelopmentCourse)
admin.site.register(pdpTopic)
admin.site.register(PDPCourseTeacher)
admin.site.register(FullCourse)
admin.site.register(FullCourseTopic)
admin.site.register(FullCourseTeacher)
admin.site.register(MiniCoursesInFullCourse)
admin.site.register(PersonalDevelopmentCoursesInFullCourse)
admin.site.register(UserMiniCourse)
admin.site.register(UserFullCourse)
admin.site.register(UserPersonalDevelopmentCourse)
admin.site.register(SyllabusDownloadData)
admin.site.register(moreAboutPdf)
admin.site.register(MiniCourseRating)
admin.site.register(PersonalDevelopmentCourseRating)
admin.site.register(HomeCarousel)
admin.site.register(IndustryPartner)
admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(UserQuery)
admin.site.register(Blog)
admin.site.register(Blogcategory)
admin.site.register(YoutubeVideo)
admin.site.register(Message)

class FreeDemoAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_no', 'email', 'date_added')

admin.site.register(freeDemoRegistration, FreeDemoAdmin)

