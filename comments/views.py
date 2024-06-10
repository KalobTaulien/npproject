from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Comment, Reply
from .forms import ReplyForm


class CommentView(APIView):
    parser_classes = [JSONParser]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        # TODO: Implement pagination for the comments.
        # TODO: Implement a filter for the comments. Namely for the specific webpage this is being used on.
        return Comment.objects.all().order_by("-date_posted")

    def get(self, request, *args, **kwargs):
        comments = self.get_queryset()
        comments = [comment.as_api() for comment in comments]
        return Response(comments)

    # def post(self, request, *args, **kwargs):
    #     # We _could_ support posting to /comments/, but for now this is disabled.
    #     return super().post(request, *args, **kwargs)


class ReplyView(APIView):
    parser_classes = [JSONParser]
    http_method_names = ["post"]

    def get_queryset(self):
        return Reply.objects.none()

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=request.data.get("comment_id"))

        # TODO:
        # - [ ] Add GPT Validation for constructive conversations
        # - [ ] Time permitting, GPT could also verify if the reply is inline with the emoji/agreement value the user selects.

        data = {
            'comment': request.data.get("comment_id"),
            'text': request.data.get("reply"),
        }

        # Let Django and the thousands of people before us handle the form validation.
        # Somethings don't need to be reinvented. That's just my 2 cents.
        form = ReplyForm(data)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.user_id = 1 # request.user  # TODO: Implement user authentication via JWT. Will be simple with `djangorestframework-simplejwt`. Time permitting, this would be ideal.
            reply.save()
            return Response(reply.as_api())
        else:
            print("Error, Will Robinson!")
            return Response({"error": form.errors}, status=400)

