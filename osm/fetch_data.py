import string
import os
from urllib.parse import quote

from ediblepickle import checkpoint

from .filter_address import filter_address


dir_path = os.path.dirname(os.path.realpath(__file__))

def key_namer(args, kwargs):
  return args[0].replace('/', '_') + '.pkl'

@checkpoint(
  key=key_namer,
  work_dir=dir_path + '/../cache/summary/'
)
def fetch_summary(addr, sesion):
  quote_addr = quote(addr)
  response = session.get(f'https://nominatim.openstreetmap.org/search/{quote_addr}?format=json&countrycodes=us')
  if (response.status_code != 200):
    print(response.status_code)
  return response.json()

@checkpoint(
  key=string.Template('{0}.pkl'),
  work_dir=dir_path + '/../cache/detail/'
)
def fetch_detail(osm_id, sesion):
  response = session.get(f'https://nominatim.openstreetmap.org/lookup?osm_ids={osm_id}&format=json')
  if (response.status_code != 200):
    print(response.status_code)
  return response.json()

def fetch_summary_detail(session=None, tqdm=lambda x: x):
  addresses = filter_address()
  summaries_list = [fetch_summary(addr, session) for addr in tqdm(addresses)]

  details = []
  for summaries in tqdm(summaries_list):
    for summary in summaries:
      osm_id = summary['osm_type'][0].upper() + str(summary['osm_id'])
      details += fetch_detail(osm_id, session)

  return summaries_list, details
