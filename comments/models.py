from django.db import models
from django.utils.translation import gettext as _


# Ratings are stored as integers. Small spacing between each number is used to allow for future expansion
# of the rating scale. For example, if a new rating is added between 2 and 0, it can be inserted as -1.
# Can be translated via Django/Python as well, which could help keep the frontend smaller when serving .js files via
# a CDN.
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
    text = models.TextField()  # TODO: Add validation for text length

    class Meta:
        abstract = True


class Comment(CommonFields, models.Model):
    # TODO:
    # - [ ] Add a site/site-url field for comment look ups on specific websites.
    #       This way the comments being stored can be filtered out by our partners.

    def __str__(self):
        return f'{self.user} - {self.date_posted} - {self.comment[0:25]}'


class Reply(CommonFields, models.Model):
    """
    Links this Reply to the Comment model. Replies and Comments are nearly identical since
    they are, essentially, a "Comment on a comment" system (ie. threads).
    """
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user} - {self.date_posted} - {self.reply[0:25]}'
