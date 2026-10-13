from django.contrib.auth.mixins import UserPassesTestMixin


class FullMemberRequired(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_authenticated and not self.request.user.tournament_only:
            return True
        return False
