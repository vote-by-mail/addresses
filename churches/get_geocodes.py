'''
Getting geocode information on churches

Preconditions:
- churches.json file produced by the crawler
- google_api_key.txt file with api key.  Make sure billing enabled.

Postcondition:
- churches_w_geocodes.json
  Look at all church JSON blobs in the target states,
  shuffle randomly, and then one-at-a-time geocode them
  and add the geocoding as a new field in the JSON blob
  and save it to this file.
'''

import json, random, time, requests

target_states = [
  'fl', #  'Florida'
  'ga', #  'Georgia'
  'mn', #  'Minnesota'
  'ne', #  'Nebraska'
  'me', #  'Maine'
  'md', #  'Maryland'
  'va', #  'Virginia'
  'nv', #  'Nevada'
  'mi', #  'Michigan'
  'wi'  #  'Wisconsin'
]

API_KEY = open('google_api_key.txt').read()

def get_geo_blob(ch):
  addr = ch['address'].replace(' ','+').replace('&','').replace('++', '+')
  url_base = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'
  url = url_base % (addr, API_KEY)
  x = requests.request(url=url,method='GET')
  return x.json()

def get_churches():
	church_blobs = [json.loads(l) for l in open('churches.json').readlines()]
	church_blobs_target_states = [b for b in church_blobs
		if b['url'].split('/')[2] in target_states]
	# Shuffle so that the first K blobs are a good sample of whole distribution,
	# in case geocoding is only done for some of the churches
	random.shuffle(church_blobs_target_states)
	return church_blobs_target_states
	#pd.Series([b['url'].split('/')[2] for b in church_blobs_target_states]).value_counts()

def main():
	church_blobs_target_states = get_churches()
	start = time.time()
	for i, blb in enumerate(church_blobs_target_states):
	  if 'geocode' in blb: continue
	  try: geo = get_geo_blob(blb)
	  except:
		geo = None
		print('WARNING: got an error')
	  blb['geocode'] = geo
	  try: open('churches_w_geocodes.json', 'a').write(json.dumps(blb)+'\n')
	  except: continue
	  if i%10==0: print('did ', i, ' in ', time.time()-start, ' seconds')

if __name__ != '__main__':
    main()