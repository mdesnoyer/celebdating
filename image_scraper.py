import urllib2
import simplejson
import cStringIO
import urllib
import os

def get_request_url(searchTerm, index):
  searchTerm = searchTerm.replace(' ', '%20')
  return "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + searchTerm + "&start=" + str(index)

def get_images(searchTerm):
  fetcher = urllib2.build_opener()
  urls = []
  while len(urls) < 20:
    searchUrl = get_request_url(searchTerm, len(urls))
    f = fetcher.open(searchUrl)
    do = simplejson.load(f)['responseData']
    data = do['results']
    for i in data:
      urls.append(i['unescapedUrl'])
    print 'URLs found: %i'%(len(urls))
  return urls

def get_20_imgs(searchTerm):
  dest = '/Users/neon/Desktop/celebrities'
  dest = os.path.join(dest, searchTerm.replace(' ', '_'))
  try:
    os.mkdir(dest)
  except:
    print 'Cant make directory'
  urls = get_images(searchTerm)
  for n,u in enumerate(urls):
    print 'Saving %i image'%(n)
    filetype = u.split('.')[-1]
    filetype = filetype.split('/')[0]
    filetype = filetype.split('.')[0]
    filetype = filetype.split('?')[0]
    try:
      urllib.urlretrieve(u, os.path.join(dest, str(n)) + '.' + filetype)
    except:
      pass

f = open('/Users/neon/Desktop/celeb_2dl').read().split('\n')
for n,i in enumerate(f):
  print 'Getting %i/%i for %s'%(n, len(f), i)
  get_20_imgs(i)