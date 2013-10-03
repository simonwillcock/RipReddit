import json
from urllib2 import urlopen, Request, HTTPError

def get_items(subreddit, sort='hot'):
	""" Returns a list of items from a subreddit, optionally sorted by
	hot, new, controversial or top. """

	BASE_URL = 'http://www.reddit.com/r/%s/%s.json' % (subreddit, sort)

	HEADER = { 'User-Agent' : 'RipReddit script' }

	try: 
		request = Request(BASE_URL, headers=HEADER)
		raw_json = urlopen(request).read()
		json_data = json.JSONDecoder().decode(raw_json)
		items = [x['data'] for x in json_data['data']['children']]
	except HTTPError as ERROR:
		print '\t%s HTTP Error received for %s' % (ERROR.code, BASE_URL)
		items = []
	return items

if __name__ == '__main__':
	
	print "Recent items from the Wallpaper subreddit:"
	items = get_items('wallpaper')
	for item in items:
		print '\t%s - %s' % (item['title'], item['url'])

	print "\nRecent items from the Wallpaper subreddit, sorted by Top:"
	items = get_items('wallpaper', 'top')
	for item in items:
		print '\t%s - %s' % (item['title'], item['url'])
