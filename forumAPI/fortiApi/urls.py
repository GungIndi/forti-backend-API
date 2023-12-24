from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', main),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('users', UserView.as_view()),
    re_path(r'^users/(?P<id>\d+)$', GetUser.as_view({'get':'search_by_id', 'put':'update_user', 'delete':'delete_user'}),name='user-by-id'),
    path('posts/', PostView.as_view()),
    re_path(r'^posts/(?P<id>\d+)$', GetPost.as_view({'get':'search_by_id', 'put':'update_post', 'delete':'delete_post'}),name='post-by-id'),
    path('replies', RepliesView.as_view()),
    re_path(r'^replies/(?P<id>\d+)$', GetReply.as_view({'get':'search_by_id', 'put':'update_reply', 'delete':'delete_reply'}),name='reply-by-id'),
    path('postFeedback', PostFeedbackView.as_view()),
    re_path(r'^postFeedback/(?P<id>\d+)$', GetPostFeedbackView.as_view({'get':'search_by_id', 'put':'update_feedback'})),
    path('repliesFeedback', RepliesFeedbackView.as_view()),
    re_path(r'^repliesFeedback/(?P<id>\d+)$', GetRepliesFeedbackView.as_view({'get':'search_by_id', 'put':'update_feedback'}))
]