import attr


@attr.s
class Classification:
    level = attr.ib(order=True)
    name = attr.ib(order=False)
    identifier = attr.ib(order=False)


A3 = Classification(level=1, name='Archer 3rd class', identifier='A3')
A2 = Classification(level=2, name='Archer 2nd class', identifier='A2')
A1 = Classification(level=3, name='Archer 1st class', identifier='A1')
B3 = Classification(level=4, name='Bowman 3rd class', identifier='B3')
B2 = Classification(level=5, name='Bowman 2nd class', identifier='B2')
B1 = Classification(level=6, name='Bowman 1st class', identifier='B1')
MB = Classification(level=7, name='Master Bowman', identifier='MB')
GMB = Classification(level=8, name='Grand Master Bowman', identifier='GMB')
EMB = Classification(level=9, name='Elite Master Bowman', identifier='EMB')

CLASSIFICATIONS = [A3, A2, A1, B3, B2, B1, MB, GMB, EMB]
CLASSIFICATION_CHOICES = [(c.identifier, c.name) for c in CLASSIFICATIONS]
CLASSIFICATION_LOOKUP = {c.identifier: c for c in CLASSIFICATIONS}
