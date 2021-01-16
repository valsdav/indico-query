import hashlib
import hmac
import time
import requests as req
from .Event  import Event
from .Category import Category
import logging 
log = logging.getLogger(__name__)


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


    def get_events_in_category(self, category, f="today", t="today", fetch_contributions=False, limit=20, skip=0):
        path = '/export/categ/{}.json'.format(category)
        params = {
            'from': f, 
            'to': t,
            'limit': limit,
            'offset': skip
        }
        if fetch_contributions: 
            params['detail'] =  'contributions'

        path = build_indico_request(path, params, self.api_key, self.secret_key)
        log.debug(path)
        r = req.get(self.base_url + path)
        
        if r.status_code == 200:
            data =  r.json()
            events = [ ] 
            for result in data['results']:
                events.append(Event(result))
            return events 
        raise Exception("Category not found")

    def get_event_details(self, event):
        path = '/export/event/{}.json'.format(event)
        params = {
            'detail': 'contributions',
        }
        path = build_indico_request(path, params, self.api_key, self.secret_key)
        log.debug("Getting event details: " , path)
        r = req.get(self.base_url + path)
        if r.status_code == 200:
            data = r.json()
            ev = Event(data['results'][0])
            return ev

    def get_user_contributions(self, person_fullname, category, from_date, to_date='now'):
        results = [] 
        more_events = True
        nreq = 0
        nstep = 10
        while(more_events):
            try:
                log.debug("requesting")
                events = self.get_events_in_category(category, f=from_date, t=to_date, 
                                                fetch_contributions=True, limit=nstep, skip=nreq*nstep )
                if len(events)==0: more_events = False
                for ev in events:
                    if ev.filter_user(person_fullname):
                        results.append(ev)
                nreq+=1
            except Exception as e:
                print("Error", e)
                more_events = False
        return results
