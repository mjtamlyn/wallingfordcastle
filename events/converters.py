import datetime
import re

from django.conf import settings


class ApiDateConverter:
    regex = r'\d{4}-\d{2}-\d{2}'
    date_format = '%Y-%m-%d'

    def to_python(self, value):
        return datetime.datetime.strptime(value, self.date_format).date()

    def to_url(self, value):
        return value.strftime(self.date_format)


class SlotReferenceConverter:
    regex = r'(\d{4}-\d{2}-\d{2})/([a-z-]+)/(\d{2}:\d{2})/B?(\d+)(A|B)?/'
    named_regex = (
        r'(?P<date>\d{4}-\d{2}-\d{2})/'
        r'(?P<venue>[a-z-]+)/'
        r'(?P<time>\d{2}:\d{2})/'
        r'(?P<brange>B)?(?P<target>\d+)(?P<face>A|B)?/'
    )

    def to_python(self, value):
        match = re.match(self.named_regex, value)
        date = ApiDateConverter().to_python(match.group('date'))
        time = datetime.datetime.strptime(match.group('time'), '%H:%M').time()
        start = datetime.datetime.combine(date, time, tzinfo=settings.TZ)
        face = match.group('face')
        if face:
            face = {'A': 1, 'B': 2}[face]
        return {
            'start': start,
            'venue__slug': match.group('venue'),
            'b_range': bool(match.group('brange')),
            'target': match.group('target'),
            'face': face,
        }

    def to_url(self, value):
        raise ValueError('Not implemented')
