import json, time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

phantom_path = r"C:\Users\Tacocat\OneDrive\Desktop\overabundant_lakes\addresses\church_data\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs"
driver = webdriver.PhantomJS(executable_path=phantom_path)

def get_clerk(addr, wait=0.5):
  # use web driver to get ground truth clerk for an address
  time.sleep(wait)
  driver.get('https://mvic.sos.state.mi.us/Clerk')
  addr_text = driver.find_elements_by_id('Address')[0]
  addr_text.send_keys(addr)
  time.sleep(wait)
  addr_text.send_keys(Keys.ENTER)
  time.sleep(2+wait)
  county = driver.find_elements_by_class_name('local-clerk-county-name')[0].text
  title = driver.find_elements_by_class_name('card-title')[0].text
  body = driver.find_elements_by_class_name('card-body')[0].text
  if 'Required field' in body: raise Exception
  return dict(county=county, title=title, body=body)

blobs = [json.loads(l[:-1]) for l in open('churches_w_geocodes.json')]
#mbs = [b for b in blobs if b['address'] and b['address'][-2:]=='MI']
mbs = [json.loads(l[:-1]) for l in open('mi_churches_w_clerks_and_counties.json')]

n_fail, n_success = 0, 0
for mb in mbs:
  if 'clerk' in mb: continue
  #if 'Po Box' in mb['address']: continue
  print(mb['address'])
  try:
    res = get_clerk(mb['address'], wait=2.5)
    mb['clerk'] = res
    print('success')
    n_success += 1
  except KeyboardInterrupt: break
  except Exception as e:
    print('failure', e)
    n_fail += 1
  print('fail', n_fail, 'success', n_success)

# Save out results
for mb in mbs:
  open('mi_churches_w_clerks_and_counties.json', 'a').write(json.dumps(mb)+'\n')

# Get FIPS codes for our churches
template = 'https://gisago.mcgi.state.mi.us/arcgis/rest/services/OpenData/michigan_geographic_framework/MapServer/2/query?where=1%3D1&geometry={lng}%2C{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=true&returnTrueCurves=false&returnIdsOnly=false&returnCountOnly=false&returnZ=false&returnM=false&returnDistinctValues=false&returnExtentOnly=false&featureEncoding=esriDefault&f=pjson'
n_success, n_fail = 0, 0
for i, m in enumerate(mbs):
  if 'fipscode' in m: continue
  print(i)
  try:
    loc = m['geocode']['results'][0]['geometry']['location']
    url = template.format(**loc)
    resp = requests.get(url).json()
    m['fipscode'] = resp['features'][0]['attributes']['FIPSCODE']
    #print(m['fipscode'])
    n_success += 1
  except: n_fail += 1
  print('success', n_success, 'fail', n_fail)


# Get our clerks using FIPS codes
our_url = 'https://raw.githubusercontent.com/mail-my-ballot/elections-officials/master/public/michigan.json'

offs = requests.get(our_url).json()
fip2clerks = {}
for o in offs:
  fip2clerks[o['fipscode']] = fip2clerks.setdefault(o['fipscode'], [])+[o]

for m in mbs:
  try: m['our_clerks'] = fip2clerks[m['fipscode']]
  except: print('error')

# Save out results
for mb in mbs:
  open('mi_misses.json', 'a').write(json.dumps(mb)+'\n')


# Compare
def comp2clerks(gt_clerk, our_clerks):
  # Pass if the ground truth clerk matches ANY of our clerks.
  # Matching determined by looking at email addresses
  for oc in our_clerks:
    for em in oc['emails']:
      if em in gt_clerk['body']: return True
  return False

# Do comparisons only for addresses that have a ground truth
to_compare = [m for m in mbs if 'clerk' in m ]
misses = [m for m in to_compare if 'our_clerk' in m
  and not comp2clerks(m['clerk'], m['our_clerks'])]

error_rate = len(misses)*1.0/len(to_compare)
print('Error rate:', error_rate*100, '%')

for mb in misses:
  open('misses.json', 'a').write(json.dumps(mb)+'\n')

for mb in misses[:5]:
  print(10*'*')
  print(mb['address'])
  print(mb['clerk'])
  print(mb['our_clerks'])
  print('\n\n')


