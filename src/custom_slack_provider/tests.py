from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase
from allauth.socialaccount.tests import setup_app
from allauth.account import app_settings
from django.core.management import call_command
from django.test.utils import override_settings

from .provider import SlackProvider
from django.core.management import call_command


class SlackOAuth2Tests(OAuth2TestsMixin, TestCase):
    provider_id = SlackProvider.id
    provider = SlackProvider
    def setUp(self):
        call_command('loaddata', 'organisation', verbosity=0)
        setup_app(self.provider)
        from django.contrib.sites.models import Site
        from allauth.socialaccount.models import SocialApp
        sa = SocialApp.objects.create(name='testcustomslack',
                                      provider=SlackProvider)
        sa.sites.add(Site.objects.get_current())

    def get_mocked_response(self):
        return MockedResponse(200, """{
          "ok": true,
          "url": "https:\\/\\/myteam.slack.com\\/",
          "team": {"name": "My Team", "id": "U0G9QF9C6"},
          "user": {"id": "T0G9PQBBK"},
          "team_id": "T12345",
          "user_id": "U12345"
        }""")  # noqa