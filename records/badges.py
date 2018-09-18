from django.utils.text import slugify

import attr


@attr.s
class BadgeGroup:
    name = attr.ib()
    slug = attr.ib()

    @slug.default
    def get_slug(self):
        return slugify(self.name)


@attr.s
class Badge:
    name = attr.ib()
    group = attr.ib()
    slug = attr.ib()

    @slug.default
    def get_slug(self):
        return slugify(self.name)


WA_BEGINNERS = BadgeGroup(name='WA beginners')
BADGE_GROUPS = [
    WA_BEGINNERS,
]
BADGES = [
    Badge(name='Red Feather', group=WA_BEGINNERS),
    Badge(name='Gold Feather', group=WA_BEGINNERS),
    Badge(name='White Arrow', group=WA_BEGINNERS),
    Badge(name='Black Arrow', group=WA_BEGINNERS),
    Badge(name='Blue Arrow', group=WA_BEGINNERS),
]

BADGE_GROUP_CHOICES = [(group.slug, group.name) for group in BADGE_GROUPS]
BADGE_CHOICES = [(badge.slug, badge.name) for badge in BADGES]
