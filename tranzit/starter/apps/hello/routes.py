from tranzit.starter.apps.hello.views import *

PATH_PREFIX = ''

routes = {
    '/': IndexHandle
}

ws_rules = {
    'get_page': WSPullHandle.get_page,
    'get_hello': WSPushHandle.get_hello
}