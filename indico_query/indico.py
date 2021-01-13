import hashlib
import hmac
import time
import requests as req

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def build_indico_request(path, params, api_key=None, secret_key=None, only_public=False, persistent=False):
        items = list(params.items()) if hasattr(params, 'items') else list(params)
        if api_key:
            items.append(('apikey', api_key))
        if only_public:
            items.append(('onlypublic', 'yes'))
        if secret_key:
            if not persistent:
                items.append(('timestamp', str(int(time.time()))))
            items = sorted(items, key=lambda x: x[0].lower())
            url = '%s?%s' % (path, urlencode(items))
            signature = hmac.new(secret_key.encode('utf-8'), url.encode('utf-8'),
                                hashlib.sha1).hexdigest()
            items.append(('signature', signature))
        if not items:
            return path
        return '%s?%s' % (path, urlencode(items))


class IndicoSession():

    def __init__(self, base_url, api_key, secret_key):
        self.base_url = base_url
        self.api_key = api_key
        self.secret_key = secret_key


    def get_events_in_category(self, category, From="today", To="today"):
        path = '/export/categ/{}.json'.format(category)
        params = {
            'from': From, 
            'to': To
        }
        path = build_indico_request(path, params, self.api_key, self.secret_key)
        data = req.get(self.base_url + path)
        if data.status_code == 200:
            return data.json()

    def get_event_details(self, event):
        path = '/export/event/{}.json'.format(event)
        params = {
            'occ':'yes',
            'detail': 'contributions'
        }
        path = build_indico_request(path, params, self.api_key, self.secret_key)
        data = req.get(self.base_url + path)
        if data.status_code == 200:
            return data.json()