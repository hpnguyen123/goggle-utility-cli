import os
import click
import pickle
from . import auth


class Context(object):
    """ Context object for CLI
    """
    def __init__(self):
        self.verbose = False
        self._ensure_directory(os.path.expanduser('~/.gutil'))
        self.credentials = os.path.expanduser('~/.gutil/credentials.json')
        self.client_secret = os.path.expanduser('~/.gutil/client_secret.json')
        self.context = os.path.expanduser('~/.gutil/context.ser')

        if os.path.isfile(self.context):
            self._deserialize()

    def get_service(self, service):
        """ Gets the current session.  If token expired, refresh token
        """
        return auth.get_service(self.get_credentials(), service=service)

    def get_credentials(self):
        """ Get Credentials from GOOGLE
        """
        return auth.get_credentials(self.credentials, self.client_secret)

    def _serialize(self):
        pickle.dump(self, open(self.context, "wb"))

    def _deserialize(self):
        data = pickle.load(open(self.context, "rb"))
        self.__dict__.update(data.__dict__)

    def _ensure_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)


pass_context = click.make_pass_decorator(Context, ensure=True)
