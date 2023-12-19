from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('', main),
    path('users/', UserView.as_view()),
    path('users/search/', GetUser.as_view({'get':'search_by_parameter'}),name='user-search'),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('post/', PostView.as_view()),
    path('reply/', ReplyView.as_view()),
    path('postFeedback/', PostFeedbackView.as_view()),
    path('repliesFeedback/', RepliesFeedbackView.as_view()),
    path('employee/', EmployeeView.as_view())
]