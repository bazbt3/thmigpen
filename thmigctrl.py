#!/usr/bin/env python3

# thmigctrl
# v0.1.0 for Python 3.5

# Runs modules based on a matching hashtag

# Setup tag and channel parameters, a list of valid command options: 
tag = 'tmctrl'
retrievecount = 20
channelid = 962

# Import @33MHz and @thrrgilag's library for interacting with pnut.io:
import pnutpy

# Import time, used to delay posting to avoid rate limits:
import time

# Setup pnut.io authorisation:
tokenfile = open("pnut_app_token.txt", "r")
token = tokenfile.read()
token = token.strip()
pnutpy.api.add_authorization_token(token)

# Get hashtag content from pnut.io:
d = pnutpy.api.posts_with_hashtag(tag, count = retrievecount)

# Extract posts, strip out unnecessary words, check for matches to poll options, and construct a summary message:
# Open the previous post numbers file:
f=open('pollctrl.txt','r')
y = f.readlines()
f.close()
f=open('pollctrl.txt','w')
posttext = ''
number = retrievecount
# hashtag = ''
while number >= 0:
	try:
		if not 'is_deleted' in d[0][number]:
			user = str(d[0][number]["user"]["username"])
			querypost = d[0][number]["content"]["text"]
			postnum = str(d[0][number]["id"])
			# If postnum does not appear in the file it's not been seen, so process it to see if a command was made:
			success = False
			if (not (postnum + '\n') in y):
				if 'help' in querypost:
					posttext = '''
*Checks only every 15 minutes.
*Precede all commands with a hash
tmctrl help:
	this!
tmask #hashtag:
	Suggest a hashtag
tmpoll #hashtag:
	Vote for a hashtag
'''
					success = True
				elif ('ask' in querypost):
					posttext = ' ask'
					success = True
				elif ('poll' in querypost):
					posttext = ' poll'
					success = True
				elif success == False:
					posttext = ' Oops, I don\'t understand; please try again. Try #help for more.'
				posttext = '@' + user + posttext + ' (' + postnum + ')'
				if posttext:
					pnutpy.api.create_post(data={'reply_to': postnum, 'text': posttext})
					# Delay to avoid rate limits:
					time.sleep(3.2)
			f.write(str(postnum) + '\n')
			posttext = ''
	except IndexError:
		pass
	number -= 1
f.close()
