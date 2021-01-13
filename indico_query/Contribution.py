from pprint import pprint 

class Contribution():

    def __init__(self, data):
        self.startDate = data['startDate']
        self.endDate = data['endDate']
        self.speakers = [] 
        for speak in data['speakers']:
            self.speakers.append({
                'first_name': speak['first_name'],
                'last_name': speak['last_name'],
                'affiliation': speak['affiliation'],
                'person_id': speak['person_id']
            })
        self.attachments = [ ] 
        for folder in data['folders']:
            for att in folder['attachments']:
                if att['type'] == 'file':
                    self.attachments.append({
                        'download_url': att['download_url'],
                        'filename': att['filename'],
                        'title': att['title'],
                        'content_type': att['content_type'],
                        'modified_dt': att['modified_dt']
                    })
                elif att['type'] == 'link':
                    self.attachments.append({
                        'link_url': att['link_url'],
                        'title': att['title'],
                        'modified_dt': att['modified_dt']
                    })
