from django.urls import path

from . import views


app_name = 'courses'

urlpatterns = [
    path('summer-2018/', views.Summer2018.as_view(), name='summer-2018'),
    path('summer-2018/book/', views.Summer2018Book.as_view(), name='summer-2018-book'),
    path('summer-2018/<id>/payment/', views.Summer2018Payment.as_view(), name='summer-2018-payment'),
    path('dgs/', views.SchoolSignup.as_view(school='dgs'), name='dgs'),
    path('icknield/', views.SchoolSignup.as_view(school='icknield'), name='icknield'),
    path('home-ed/', views.SchoolSignup.as_view(school='home-ed'), name='home-ed'),
    path('juniors/minis/', views.MinisInterestView.as_view(), name='minis-interest'),
    path('members/courses/', views.MembersCourseList.as_view(), name='members-course-list'),
    path('members/courses/<pk>/book/', views.MembersCourseBooking.as_view(), name='members-course-booking'),
    path('members/courses/pay/', views.NonMembersPayment.as_view(), name='non-members-payment'),
]
