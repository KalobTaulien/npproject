from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Comment, Reply
from .forms import ReplyForm
from .utils import get_gpt_response


class CommentView(APIView):
    parser_classes = [JSONParser]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        # TODO: Implement pagination for the comments. DRF is best for that.
        # TODO: Implement a filter for the comments. Namely for the specific webpage this is being used on.
        return Comment.objects.all().order_by("-date_posted")

    def get(self, request, *args, **kwargs):
        comments = self.get_queryset()
        comments = [comment.as_api() for comment in comments]
        return Response(comments)


class ReplyView(APIView):
    parser_classes = [JSONParser]
    http_method_names = ["post"]

    def get_queryset(self):
        return Reply.objects.none()

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=request.data.get("comment_id"))

        if settings.OPENAI_API_KEY and settings.GPT_ENABLED:
            # TODO:
            # - [ ] Time permitting, GPT could also verify if the reply is inline with the emoji/agreement value the user selects.
            response, suggestion = get_gpt_response(comment.text, request.data.get("reply"))

            if response.lower() == "no":
                return Response(suggestion, status=400)

        data = {
            'comment': request.data.get("comment_id"),
            'text': request.data.get("reply"),
            'agreement': request.data.get("agreement"),
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
            # TODO: In my opinion, error validation is VERY important. If I write a well thought out comment or reply,
            #       and it fails to go through with no support, I'm likely to leave the site/service and never return.
            #       So this should have _a lot_ of care and attention to detail. Just my 2 cents based on
            #       personal frusstrations. Users first, always.
            print("Error, Will Robinson!")
            return Response({"error": form.errors}, status=400)

