from tranzit.starter.apps.hello.views import *

PATH_PREFIX = ''

routes = {
    '/': IndexHandle
}

ws_rules = {
    'push': {
        'notify': WSPushHandle.push_data
    },
    'pull': {
        'get_page': WSPullHandle.get_page
    }
}