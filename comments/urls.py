from comments import views
from django.urls import path

urlpatterns = [
    path("comments/", views.CommentView.as_view(), name='comments'),  # GET Comments.
    path("comments/<int:pk>/", views.ReplyView.as_view(), name='reply'),  # POST Replies.

    # This could be a thing to separate A.I. moderation from human comment/reply POST requests.
    # A degree of separation could be useful for moderation purposes, and for billing.
    # path("moderation/", views.LLMPreviewView.as_view(), name='moderate'),
]
