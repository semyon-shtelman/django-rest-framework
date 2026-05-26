import re

from rest_framework.serializers import ValidationError

def validate_links(value):
    links = re.findall(r'https?://\S+', value)
    for link in links:
        if 'youtube.com' not in link:
            raise ValidationError(
                "Разрешены ссылки только на YouTube"
            )