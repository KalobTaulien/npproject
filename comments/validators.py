from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


def validate_text_length(value):
    # TODO:
    # - [ ] Look into better minimum and maximum numbers. 50 and 5000 are arbitrary based on zero data.
    # - [ ] Apply better error messages
    # - [ ] Consider allowing HTML in comments using a wysiwyg editor. Needs bleaching for security, though.
    #       Security first. This would great for user engagement and adding emphasis to conversations,
    #       Unfortunate I suspect I'll run out of time to implement this.
    if len(value) < 50:
        raise ValidationError(_('Text is too short. Minimum length is 50 characters.'))
    elif len(value) > 5000:
        raise ValidationError(_('Text is too long. Maximum length is 5000 characters.'))

