from pprint import pprint 
import logging 
log = logging.getLogger(__name__)

class Contribution():

    def __init__(self, event, data):
        log.info("Loading contribution: {}".format( data['db_id']) ) 
        self.event_id = event.id
        self.title = data['title']
        self.startDate = data['startDate']
        self.endDate = data['endDate']
        self.id = data['db_id']
        self.speakers = [] 
        for speak in data['speakers']:
            self.speakers.append({
                'first_name': speak['first_name'],
                'last_name': speak['last_name'],
                'full_name': speak['fullName'],
                'affiliation': speak['affiliation'],
                'person_id': speak['person_id']
            })
            log.debug("Speaker: {}".format(speak['fullName']))
        self.attachments = [ ] 
        for folder in data['folders']:
            for att in folder['attachments']:
                if att['type'] == 'file':
                    self.attachments.append({
                        'url': att['download_url'],
                        'filename': att['filename'],
                        'title': att['title'],
                        'content_type': att['content_type'],
                        'modified_dt': att['modified_dt']
                    })
                elif att['type'] == 'link':
                    self.attachments.append({
                        'url': att['link_url'],
                        'title': att['title'],
                        'modified_dt': att['modified_dt']
                    })
    
    def __repr__(self):
        s = "\t>> [event:{}] {} >> {} {}".format(self.event_id, self.title, self.speakers[0]['full_name'], self.attachments[0]['url'])
        return s

    def __str__(self):
        s = "\t>> [event:{}] {} >> {} {}".format(self.event_id, self.title, self.speakers[0]['full_name'], self.attachments[0]['url'])
        return s