import json, time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

phantom_path = r"C:\Users\Tacocat\OneDrive\Desktop\overabundant_lakes\addresses\church_data\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs"
driver = webdriver.PhantomJS(executable_path=phantom_path)

def get_clerk(addr, wait=0.5):
  time.sleep(wait)
  driver.get('https://mvic.sos.state.mi.us/Clerk')
  addr_text = driver.find_elements_by_id('Address')[0]
  addr_text.send_keys(addr)
  time.sleep(wait)
  addr_text.send_keys(Keys.ENTER)
  time.sleep(wait)
  result_elems = driver.find_elements_by_class_name('card-body')
  result = result_elems[0].text
  if 'Required field' in result: raise Exception
  return result

blobs = [json.loads(l[:-1]) for l in open('churches_w_geocodes.json')]
mbs = [b for b in blobs if b['address'] and b['address'][-2:]=='MI']

# This block of code may need to be run multiple times with
# different wait time until they are all done
for mb in mbs:
  if 'clerk' in mb: continue
  print(mb['address'])
  try:
    res = get_clerk(mb['address'], wait=3)
    mb['clerk'] = res
    print('success')
  except KeyboardInterrupt: break
  except:
    print('failure')
    continue

for mb in mbs:
  open('mi_churches_w_clerks.json', 'a').write(json.dumps(mb)+'\n')




