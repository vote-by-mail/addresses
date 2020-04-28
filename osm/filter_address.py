import json
import os
import gzip
from ediblepickle import checkpoint


dir_path = os.path.dirname(os.path.realpath(__file__))

states = {'WI', 'MI', 'VA', 'ME'}

def _filter_address():
  with gzip.open(dir_path + '/../data/data.jl.gz') as fh:
    for line in fh:
      js = json.loads(line)
      address = js.get('address') or ''
      parts = address.strip().split(' ')
      state = parts[-1] if parts else None
      if state in states:
        yield address

@checkpoint(dir_path + '/../data/filterAddresses.pkl')
def filter_address():
  return [js for js in _filter_address()]

if __name__ == '__main__':
  filter_address()
