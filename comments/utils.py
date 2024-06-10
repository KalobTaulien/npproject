from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
)

def get_gpt_response(comment: str, reply: str, model='gpt-3.5-turbo') -> tuple:
    """
    Get a tuple response from OpenAI's GPT-3.5 API (default). Swappable for other models.

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

        How this will work is: I will provide you with a "Comment" (the initial point in a conversation) and then I'll provide you with a "Reply" which is what you'll be helping moderate. You can assume the "Comment" was acceptable, and you are NOT to take the tone of the comment into consideration. Strictly work with the "Reply". And I will tell you which prompt is the "Reply". The Comment and the Reply are likely written by different people, so when you provide a suggestion make sure you are not mixing the Comment and the Reply.

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
