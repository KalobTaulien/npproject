from openai import OpenAI
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Comment, Reply
from .forms import ReplyForm


client = OpenAI(
    # This is the default and can be omitted
    api_key=settings.OPENAI_API_KEY,
)

# TODO:
# - [ ] Add this function to utils.py or something similar
def get_gpt_response(comment: str, reply: str, model='gpt-3.5-turbo') -> str:
    """
    Get a string response from OpenAI's GPT-3.5 API (default). Swappable for other models.

    Ideally, GPT will return a response and a suggestion in the form of: "response::suggestion". Example:
    ```
    yes::Being able to disagree while sharing your opinion in a healthy way is important to help others learn from you.
    ```
    or
    ```
    no::It's OK to feel angry or overly excited, but it's equally important to express yourself in a way that's respectful and constructive.
    ```

    The :: is split to get a binary `yes/no` response, plus a text based suggestion.
    """

    # TODO: It's much more efficient if we fine tuned a gpt to do this task rather than
    #       prompting it with the same large token prompt over and over.
    messages = [{
        "role": "system",
        "content": """You are to become a moderator for online conversations, helping guide conversation in a constructive manner. Confrontation and disagreement are perfectly acceptable as long as they are respectful of other members. The conversations should always maintain it's integrity. No hateful speech, no shutting down opinions without providing a reason, and no trolling other members in the conversation.

        How this will work is: I will provide you with a "Comment" (the initial point in a conversation) and then I'll provide you with a "Reply" which is what you'll be helping moderate. You can assume the "Comment" was acceptable, and you are NOT to take the tone of the comment into consideration. Strictly work with the "Reply". And I will tell you which prompt is the "Reply".

        I'd like you to respond in a specific way. The format will be:
        ```
        {yes|no}::{suggested_healthy_reply}
        ```

        If the "Reply" I supply you is considered constructive, or as a bare minimum it's not damaging to the conversation, then you will start with `yes::` followed by a suggestion to make the conversation even better.

        If the "Reply" is considered damaging, hateful, not constructive, or otherwise ineffective for maintaining a conversation, you would start your response with `no::` follow by a suggestion to make the conversation helpful and supportive to others.

        Here's an example:
        Reply: Star Wars prequels are awful
        Your Response: `no::It's helpful to share why you believe the prequels are not good movies. Helping educate people on your views is beneficial to long term conversations.`

        Here's a second example:
        Reply: I like this article because it's informative and links to it's sources.
        Your Response: `yes::Great job sharing your perspective. Food for thought: how can you keep this healthy conversation going?`"""
    }]

    # I have an idea for a single response prompt thats both information and helpful.
    messages.append({
        "role": "user",
        "content": f"Comment: {comment}"
    })
    messages.append({
        "role": "user",
        "content": f"Reply: {reply}"
    })

    # TODO: Wrap in a try/catch block to catch any errors from the API
    #       See: https://platform.openai.com/docs/guides/error-codes/api-errors
    chat = client.chat.completions.create(
        messages=messages,
        model=model,
    )

    # response = yes|no
    # suggestion = text suggestion from gpt
    response, suggestion = chat.choices[0].message.content.split('::', 1)

    return response, suggestion


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

