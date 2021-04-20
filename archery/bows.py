import attr


@attr.s
class Bow:
    name = attr.ib()
    ident = attr.ib()


recurve = Bow(name='Recurve', ident='recurve')
compound = Bow(name='Compound', ident='compound')
barebow = Bow(name='Barebow', ident='barebow')
longbow = Bow(name='Longbow', ident='longbow')
american_flatbow = Bow('American Flatbow', ident='flatbow')

BOWSTYLES = [recurve, compound, barebow, longbow, american_flatbow]
BOWSTYLE_CHOICES = [(bowstyle.ident, bowstyle.name) for bowstyle in BOWSTYLES]
