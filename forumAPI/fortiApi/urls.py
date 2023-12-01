from django.urls import path
from .views import UserView, main, EmployeeView


urlpatterns = [
    path('', main),
    path('user/', UserView.as_view()),
    path('employee/', EmployeeView.as_view()),
]