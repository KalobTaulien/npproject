from django.db import models
from django.utils.translation import gettext as _

from .validators import validate_text_length

# Ratings are stored as integers. Small spacing between each number is used to allow for future expansion
# of the rating scale. For example, if a new rating is added between 2 and 0, it can be inserted as -1.
# Can be translated via Django/Python as well, which could help keep the frontend smaller when serving .js
# files via a CDN.
AGREEMENT_CHOICES = (
    (4,  _("Strongly agree")),
    (2,  _("Yes, but with reservations")),
    (0,  _("It's complicated")),
    (-2, _("No, with reservations")),
    (-4, _("Strongly no"))
)


class CommonFields(models.Model):
    """
    Common fields (DB Columns) for both Comment and Reply models.
    """
    # TODO:
    # - [ ] is_approved field for non-approved users. Default to False.
    #       Could be useful for initial moderation with new users.
    # - [ ] Custom user model to collect points, badges, etc.
    #       Ignored for this prototype, but would be ideal for community building.
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
    )
    date_posted = models.DateTimeField(
        auto_now_add=True,
    )
    anonymous_content = models.BooleanField(default=False)
    agreement = models.IntegerField(
        choices=AGREEMENT_CHOICES,
        default=0,
    )
    text = models.TextField(
        validators=[validate_text_length],
    )

    class Meta:
        abstract = True


class Comment(CommonFields, models.Model):
    # TODO:
    # - [ ] Add a site/site-url field for comment look ups on specific websites.
    #       This way the comments being stored can be filtered out by our partners.
    #       Another model/db table for sites would be ideal for denormalization and smaller tables.

    def as_api(self):
        """
        Using Django Rest Framework would be best for security and efficiency.
        But for the sake of writing readable code for non-Django developers, this method is used.

        # TODO:
        - [ ] `.as_api()` could be moved into `CommonFields` as an Interface with `super().as_api()` being used.
        """
        comment = {
            'id': self.id,
            'text': self.text,
            'date_posted': self.date_posted,
            'user_name': _('Anonymous') if self.anonymous_content else self.user.username,
            'agreement': self.agreement,
            'replies': [reply.as_api() for reply in self.reply_set.all()],
            # 'reply_agreements': [], # TODO: Cluster the agreement values for the replies.
                                      # Something like a tuple of tuples. example:
                                      # ((-2, 100), (0, 50), (2, 365), (4, 1000))
                                      # ^ That would be 100 'no', 50 'it's complicated', 365 'yes, but with reservations', and 1000 'strongly agree'.
                                      # This would ideally be cached since those lookups could be large if we did
                                      # this in real-time..ish.
        }
        return comment

    def __str__(self):
        return f'{self.user} - {self.date_posted} - {self.text[0:25]}'


class Reply(CommonFields, models.Model):
    """
    Links this Reply to the Comment model. Replies and Comments are nearly identical since
    they are, essentially, a "Comment on a comment" system (ie. threads).
    """
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )

    def as_api(self):
        """
        Nearly identical to Comment.as_api().
        """
        reply = {
            'id': self.id,
            'reply': self.text,
            'date_posted': self.date_posted,
            'user_name': _('Anonymous') if self.anonymous_content else self.user.username,
            'agreement': self.agreement,
        }
        return reply

    def __str__(self):
        return f'{self.user} - {self.date_posted} - {self.text[0:25]}'

    class Meta:
        verbose_name_plural = "Replies"
