from django.contrib import admin
from .models import Comment, Reply


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_posted', 'anonymous_content', 'agreement', 'text')
    list_filter = ('date_posted', 'anonymous_content', 'agreement')
    # TODO:
    # - [ ] Add filters based on "is_approved" and "agreement" type


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_posted', 'anonymous_content', 'agreement', 'text', 'comment')
    list_filter = ('date_posted', 'anonymous_content', 'agreement', 'text')
    # TODO:
    # - [ ] Add filters based on "is_approved" and "agreement" type
