from pprint import pprint
import re
from .Contribution import Contribution
import logging 
log = logging.getLogger(__name__)

class Event():

    def __init__(self, data):
        #pprint(data)
        log.info("Loading event: {}".format(data['id']))
        self.category = data['category']
        self.categoryId = data['categoryId']
        self.startDate = data['startDate']
        self.endDate = data['endDate']
        self.id = data['id']
        self.url = data['url']
        self.title = data['title']
        self.description = data['description']
        self.chairs = [] 
        for ch in data['chairs']:
            self.chairs.append({
                'first_name': ch['first_name'],
                'last_name': ch['last_name'],
                'affiliation': ch['affiliation'],
                'person_id': ch['person_id']
            })
        #extract zoom room from the description
        match = re.search(r'https:\/\/cern\.zoom\.us\S*(?=\s|$)',data['description'])
        if match:
            self.zoomUrl = match.group()
        self.contributions = []
        for contribution_data in data.get('contributions',[]):
            self.contributions.append(Contribution(self, contribution_data))

    def filter_user(self, user):
        contribs = []
        for contr in self.contributions:
            for speaker in contr.speakers:
                if speaker['full_name'] == user:
                    contribs.append(contr)
        if len(contribs)==0: return False
        #keep only user's contribution
        self.contributions = contribs
        return True

    
    def __repr__(self):
        s = "[event:{}] {} >> {}".format(self.id, self.title, self.url )
        for c in self.contributions:
            s += "\n" + str(c)
        return s

    def __str__(self):
        s = "[event:{}] {} >> {}".format(self.id, self.title, self.url )
        for c in self.contributions:
            s += "\n" + str(c)
        return s