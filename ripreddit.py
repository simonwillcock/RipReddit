from urllib2 import urlopen, HTTPError, URLError
import os, reddit
from argparse import ArgumentParser

def handle_imgur_url(url):
	"""
	Takes Imgur URL and checks if direct link has correct extension. 
	"""
	
	# all static imgur files are jpegs so use .jpg extension
	if url.endswith('.png'):
		url = url.replace('.png', '.jpg')
	else:
		# if no extension, add .jpg
		ext = os.path.splitext(os.path.basename(url))[1]
		if not ext:
			url += '.jpg'

	return [url]

def get_urls(url):
	""" Checks to see if URL is imgur.com and handles, otherwise 
	simply returns the given url in a list (for planned imgur gallery suppory).
	"""

	urls = []

	# is valid imgur.com url
	if 'imgur.com' in url:
		urls = handle_imgur_url(url)
	else:
		urls = [url]

	return urls


if __name__ == '__main__':
	PARSER = ArgumentParser(description='Downloads images from the specified subreddit.')
	PARSER.add_argument('subreddit', metavar='<subreddit>', help='Subreddit name.')
	PARSER.add_argument('dir', metavar='<dest_folder>', help='Directory to put downloaded files in.')
	ARGS = PARSER.parse_args()

	# Check if directory exists and create it if not.
	if not os.path.exists(ARGS.dir):
		os.mkdir(ARGS.dir)

	items = reddit.get_items(ARGS.subreddit)

	total = errors = passed = 0

	for item in items:
		total += 1

		urls = get_urls(item['url'])
		
		for url in urls:
			print url

