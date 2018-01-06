from braces.views._access import UserPassesTestMixin


class FullMemberRequired(UserPassesTestMixin):

    def test_func(self, user):
        if user.is_authenticated and not user.tournament_only:
            return True
        return False
