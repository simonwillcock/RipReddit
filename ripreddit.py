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

def download_file(url, filepath):
	""" Try and download the file from the URL and save to 'filepath'

	It will not download the same file more than once
	"""

	ext_whitelist = ['image/jpeg', 'image/png', 'image/gif']

	# Check to see if file exists 
	try:
		with open(filepath):
			print "URL (%s) has already been downloaded." % url

	except IOError:
		response = urlopen(url)
		info = response.info()

		# Check file type
		if 'content-type' in info.keys():
			filetype = info['content-type']
		elif url.endswith('.jpg') or url.endswith('.jpeg'):
			filetype = 'image/jpeg'
		elif url.endswith('.png'):
			filetype = 'image/png'
		elif url.endswith('.gif'):
			filetype = 'image/gif'
		else:
			filetype = 'unrecognised'

		if not filetype in ext_whitelist:
			
			print "URL (%s) has incorrect file type: %s" % (url, filetype)

		# Save data to file
		filedata = response.read()
		with open(filepath, 'wb') as new_file:
			new_file.write(filedata)
		



if __name__ == '__main__':
	PARSER = ArgumentParser(description='Downloads images from the specified subreddit.')
	PARSER.add_argument('subreddit', metavar='<subreddit>', help='Subreddit name.')
	PARSER.add_argument('dir', metavar='<dest_folder>', help='Directory to put downloaded files in.')
	ARGS = PARSER.parse_args()

	# Check if directory exists and create it if not.
	if not os.path.exists(ARGS.dir):
		os.mkdir(ARGS.dir)

	items = reddit.get_items(ARGS.subreddit)

	total = 0

	for item in items:
		total += 1

		urls = get_urls(item['url'])
		

		for url in urls:
			# Set filename and try to download file
			try:
				
				# Remove any HTTP queries from end of url to get clean ext
				ext = os.path.splitext(url)[1]
				if '?' in ext:
					ext = ext[:ext.index('?')]

				filename = '%s%s' % (item['id'], ext)
				filepath = os.path.join(ARGS.dir, filename)

				download_file(url, filepath)

			except HTTPError as e:
				print '\tReceived HTTP Error (%s) from %s' % (e.code, url)

			
			

