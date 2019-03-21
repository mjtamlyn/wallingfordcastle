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
CLUB_PORTSMOUTH = BadgeGroup(name='Half Portsmouth')
CLUB_WA_18 = BadgeGroup(name='Half WA 18')
CLUB_OUTDOOR_250 = BadgeGroup(name='Outdoor 250 Award')
BADGES = [
    Badge(name='Red Feather', group=WA_BEGINNERS),
    Badge(name='Gold Feather', group=WA_BEGINNERS),
    Badge(name='White Arrow', group=WA_BEGINNERS),
    Badge(name='Black Arrow', group=WA_BEGINNERS),
    Badge(name='Blue Arrow', group=WA_BEGINNERS),
    Badge(name='White Half Portsmouth (150)', group=CLUB_PORTSMOUTH),
    Badge(name='Black Half Portsmouth (175)', group=CLUB_PORTSMOUTH),
    Badge(name='Blue Half Portsmouth (200)', group=CLUB_PORTSMOUTH),
    Badge(name='Red Half Portsmouth (225)', group=CLUB_PORTSMOUTH),
    Badge(name='Gold Half Portsmouth (250)', group=CLUB_PORTSMOUTH),
    Badge(name='Purple Half Portsmouth (275)', group=CLUB_PORTSMOUTH),
    Badge(name='White Half WA 18 (150)', group=CLUB_WA_18),
    Badge(name='Black Half WA 18 (175)', group=CLUB_WA_18),
    Badge(name='Blue Half WA 18 (200)', group=CLUB_WA_18),
    Badge(name='Red Half WA 18 (225)', group=CLUB_WA_18),
    Badge(name='Gold Half WA 18 (250)', group=CLUB_WA_18),
    Badge(name='Purple Half WA 18 (275)', group=CLUB_WA_18),
    Badge(name='White Outdoor 250 Award (20m)', group=CLUB_OUTDOOR_250),
    Badge(name='Black Outdoor 250 Award (30m)', group=CLUB_OUTDOOR_250),
    Badge(name='Blue Outdoor 250 Award (40m)', group=CLUB_OUTDOOR_250),
    Badge(name='Red Outdoor 250 Award (50m)', group=CLUB_OUTDOOR_250),
    Badge(name='Gold Outdoor 250 Award (60m)', group=CLUB_OUTDOOR_250),
    Badge(name='Purple Outdoor 250 Award (70m)', group=CLUB_OUTDOOR_250),
]

BADGE_GROUPS = [
    WA_BEGINNERS,
    CLUB_PORTSMOUTH,
    CLUB_WA_18,
]
BADGE_GROUP_CHOICES = [(group.slug, group.name) for group in BADGE_GROUPS]
BADGE_CHOICES = [(badge.slug, badge.name) for badge in BADGES]
