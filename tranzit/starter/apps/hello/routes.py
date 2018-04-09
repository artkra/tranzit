import os
from tranzit.starter.apps.hello.views import *

PATH_PREFIX = ''

APP_STATIC_DIR = os.path.dirname(__file__) + '/static/'

routes = {
    '/': IndexHandle
}

ws_rules = {
    'get_page': WSPullHandle.get_page,
    'get_hello': WSPushHandle.get_hello
}