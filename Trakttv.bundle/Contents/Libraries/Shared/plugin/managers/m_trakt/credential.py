from plugin.managers.core.base import Manager, Update
from plugin.models import TraktBasicCredential, TraktOAuthCredential

from trakt import Trakt
import logging

log = logging.getLogger(__name__)


class UpdateBasicCredential(Update):
    keys = ['password', 'token']

    def from_dict(self, basic_credential, changes):
        # Update `TraktBasicCredential`
        if not super(UpdateBasicCredential, self).from_dict(basic_credential, changes):
            return False

        return True


class TraktBasicCredentialManager(Manager):
    update = UpdateBasicCredential

    model = TraktBasicCredential


class UpdateOAuthCredential(Update):
    keys = ['code', 'access_token', 'refresh_token', 'created_at', 'expires_in', 'token_type', 'scope']

    def from_dict(self, oauth_credential, changes):
        # Update `TraktOAuthCredential`
        if not super(UpdateOAuthCredential, self).from_dict(oauth_credential, changes):
            return False

        return True

    def from_pin(self, oauth, pin, save=True):
        # Exchange `pin` for token authorization
        authorization = Trakt['oauth'].token_exchange(pin, 'urn:ietf:wg:oauth:2.0:oob')

        if not authorization:
            log.warn('Token exchange failed')
            return None

        # Update `OAuthCredential`
        data = {'code': pin}
        data.update(authorization)

        return self(oauth, data, save=save)


class TraktOAuthCredentialManager(Manager):
    update = UpdateOAuthCredential

    model = TraktOAuthCredential
