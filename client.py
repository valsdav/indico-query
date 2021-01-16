import logging 
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
import yaml
from indico_query import indico
from pprint import pprint
import json

if __name__ == '__main__':
    cfg = yaml.load(open("tokens.yaml"),Loader=yaml.BaseLoader)
    
    log.info("Starting")
    sess = indico.IndicoSession(cfg['BASE_URL'], cfg['API_KEY'], cfg['SECRET_KEY'])
    
    #obj = sess.get_events_in_category('5783',f='2021-01-10',limit='10')
    #ev = sess.get_event_details('990632')
    contr = sess.get_user_contributions("Valsecchi, Davide", 5783, from_date='2020-08-01')
    
    pprint(contr)
    