#!/usr/bin/env python

import flickrapi
import requests
import os
import oauth2 as oauth

FLICKR_KEY = "f5f44d6fb8541eeaadbf8488d6aa6aeb"
SECRET = '5b66d6dc16d9c3dc'
USER_ID = "91593015@N06"
SET_ID = '72157639372536095'

def make_url(photo):
    # url_template = "http://farm{farm-id}.staticflickr.com/
    #                 {server-id}/{id}_{secret}_[mstzb].jpg"
    photo['filename'] = "%(id)s_%(secret)s_z.jpg" % photo
    url = ("http://farm%(farm)s.staticflickr.com/%(server)s/%(filename)s" 
           % photo)
    return url, photo['filename']

def read_token():
	#opens a file, reads in the token for access
	token = "notfound"
	try:
		fp = open("token")
	except IOError as e:
		if e.errno == errno.EACCESS:
			print "file does not exists"
		# Not a permission error.
		raise
	else:
		with fp:
			token = fp.readline().rstrip('\n')
			token_secret = fp.readline().rstrip('\n')
			fp.close()
	return token,token_secret

def main():
	print " --> Authentication..."
	token,token_secret = read_token()
	if token == "notfound" :
		print " --> Auth Token not found, please re-login "
		return
	flickr = flickrapi.FlickrAPI(api_key=FLICKR_KEY,secret=SECRET) 
	flickr.authenticate_console("read")
	print " ---> Requesting photos..."
	photos = flickr.walk_set(photoset_id=SET_ID)
	for photo in photos:
		url, filename = make_url(photo.__dict__['attrib'])
		path = '/home/jenny/Pictures/flickrtest/%s' % filename
		try:
			image_file = open(path)
			print " ---> Already have %s" % url
		except IOError:
			print " ---> Downloading %s" % url
			r = requests.get(url)      
			image_file = open(path, 'w')
			image_file.write(r.content)
			image_file.close()

if __name__ == '__main__':
	main()
