from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Comment, Reply


class CommentView(APIView):
    parser_classes = [JSONParser]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        # TODO: Implement pagination for the comments.
        # TODO: Implement a filter for the comments. Namely for the specific webpage this is being used on.
        return Comment.objects.all().order_by("-date_posted")

    def get(self, request, *args, **kwargs):
        return super.get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     # We _could_ support posting to /comments/, but for now this is disabled.
    #     return super().post(request, *args, **kwargs)


class ReplyView(APIView):
    parser_classes = [JSONParser]
    http_method_names = ["post"]

    def get_queryset(self):
        return Reply.objects.none()

    def post(self, request, *args, **kwargs):
        # Let's test this before assuming the next batch of work gets built on top of this.
        return Response({
            "hello": "world"
        }, status=200)
