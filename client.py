import yaml
from indico_query import indico
from pprint import pprint

if __name__ == '__main__':
    cfg = yaml.load(open("tokens.yaml"),Loader=yaml.BaseLoader)
    
    sess = indico.IndicoSession(cfg['BASE_URL'], cfg['API_KEY'], cfg['SECRET_KEY'])
    
    #obj = sess.get_events_in_category('5783', 'yesterday')
    ev = sess.get_event_details('990632')
    
    pprint(ev.zoomUrl)

    