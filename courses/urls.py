from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('holidays/', views.Holidays.as_view(), name='holidays'),
    path('holidays/book/', views.HolidaysBook.as_view(), name='holidays-book'),
    path('holidays/pay/', views.HolidaysPay.as_view(), name='holidays-payment'),
    path('dgs/', views.SchoolSignup.as_view(school='dgs'), name='dgs'),
    path('sbs/', views.SchoolSignup.as_view(school='sbs'), name='sbs'),
    path('maiden-erlegh/', views.SchoolSignup.as_view(school='maiden-erlegh'), name='maiden-erlegh'),
    # path('icknield/', views.SchoolSignup.as_view(school='icknield'), name='icknield'),
    # path('home-ed/', views.SchoolSignup.as_view(school='home-ed'), name='home-ed'),
    path('juniors/minis/', views.MinisInterestView.as_view(), name='minis-interest'),
    path('members/courses/', views.MembersCourseList.as_view(), name='members-course-list'),
    path('members/courses/external/', views.NonMembersCourseList.as_view(), name='non-members-course-list'),
    path('members/courses/<pk>/book/', views.MembersCourseBooking.as_view(), name='members-course-booking'),
    path(
        'members/courses/external/<pk>/book/',
        views.NonMembersCourseBooking.as_view(),
        name='non-members-course-booking',
    ),
    path('members/courses/pay/', views.NonMembersPayment.as_view(), name='non-members-payment'),
]
