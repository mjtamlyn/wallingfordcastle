from django.utils import timezone


def age_group(dob, now=None):
    if now is None:
        now = timezone.now()
    year = now.year
    born = dob.year
    birthday_this_year = year - born

    if birthday_this_year < 6:
        return 'U6'
    elif birthday_this_year < 8:
        return 'U8'
    elif birthday_this_year < 10:
        return 'U10'
    elif birthday_this_year < 12:
        return 'U12'
    elif birthday_this_year < 14:
        return 'U14'
    elif birthday_this_year < 15:
        return 'U15'
    elif birthday_this_year < 16:
        return 'U16'
    elif birthday_this_year < 18:
        return 'U18'
    elif birthday_this_year < 21:
        return 'U21'
    elif birthday_this_year < 25:
        return 'Adult (U25)'
    elif birthday_this_year >= 50:
        return '50+'
    return 'Adult'
