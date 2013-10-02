import json, os, urlparse
from urllib2 import urlopen, Request, HTTPError, URLError

def get_json_data_from_subreddit(subreddit, category, limit="10"):
	BASE_URL = "http://www.reddit.com/r/"
	full_url = BASE_URL + subreddit + "/" + category + ".json?limit=" + str(limit)
	print full_url
	raw = urlopen(full_url)
	json_data = json.load(raw)
	return json_data

def get_image_urls_from_json(json_data):
	img_urls = []
	for post in json_data['data']['children']:
		if 'imgur' in post['data']['domain']:
			img_urls.append(post['data']['url'])
	return img_urls

def dlfile(url):
    # Open the url
    DOWNLOADS_DIR = './downloads/'
    try:
        f = urlopen(url)
        print "downloading " + url

        # Open our local file for writing
        with open(DOWNLOADS_DIR + os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


def save_imgs_from_links(img_urls):
	for url in img_urls:
		filename = url.split('/')[-1]
		dlfile(url)

def rip_reddit():
	sub = raw_input("Name of subreddit (eg. Aww): ")
	cat = raw_input("Hot, Top, Controversial or New: ")
	limit = raw_input("Post limit (default = 10): ")
	json_data = get_json_data_from_subreddit(sub,cat.lower(), limit)
	img_urls = get_image_urls_from_json(json_data)
	save_imgs_from_links(img_urls)
	return True
def main():
	success = rip_reddit()
	if success:
		print "Success!"

if __name__ == '__main__':
	main()