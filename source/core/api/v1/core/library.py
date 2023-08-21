import logging
import random

from source.core import api
from .tmp import word

__author__ = 'son.hh'

_logger = logging.getLogger(__name__)

class LibraryApi(api.v1.BaseResource, api.v1.BaseApi):

    def get(self):
        return self.return_general(200, message="ok", data="This is the test message!!! Please check the answer @@")
        # return self.return_general(200, message="ok", data=word[int(random.random()*len(word))])
