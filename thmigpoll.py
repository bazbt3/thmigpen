#!/usr/bin/env python3

# thmigpoll
# A very alpha attempt to list respondents to a pnut.io poll, using an RSS feed of the poll's hashtag
# v0.1 for Python 3.5.

# Based on rssupdatepnut v0.3.2 and thmigpen v0.0.

# Setup tag and channel parameters, and a list of valid poll options: 
tag = 'tmpoll'
channelid = '962'
polloptions = [
	'#test',
	'#test1',
	'#test2'
	]

# Import RSS feed parser:
import feedparser

# Import @33MHz and @thrrgilag's library for interacting with pnut.io:
import pnutpy

# Setup pnut.io authorisation:
tokenfile = open("pnut_app_token.txt", "r")
token = tokenfile.read()
token = token.strip()
pnutpy.api.add_authorization_token(token)

# Get hashtag RSS feed from pnut.io:
feed_title = 'https://api.pnut.io/v0/feed/rss/posts/tags/' + tag
d = feedparser.parse(feed_title)

# Extract posts, strip out unnecessary words, check for matches to poll options, and construct a summary message:
n = 0
posttext = ''
for post in d:
	try:
		p_title = d.entries[n].title
		words = p_title.split()
		for word in words:
			if ('@' in word):
				word = word.strip('@')
				word = word.strip(':')
				user = word
				# print(word)
			if ('#' in word):
				if word != ('#' + tag):
					hashtag = word
					if not (hashtag in polloptions):
						hashtag += '. Rejected'
					# print(hashtag)
					# print('^^^^^^')
		# p_link = d.entries[n].link
		# p_post = p_link
		# postnum = p_post.strip('https://posts.pnut.io/')
		# postnum = postnum.split('#')
		# print(postnum[0])
		# p_publish = d.entries[n].published
		n += 1
		posttext += '• @' + user + ' voted for ' + hashtag + ' in #' + tag + '.\n'
		# print(posttext)
		# postcontent = pnutpy.api.create_post(data={'text': posttext})
	except IndexError:
		pass

# If there's text to post:
if posttext:
	
	# Create message in channel 962, using ONLY the text from pnut_message:
	messagecontent = pnutpy.api.create_message(channelid, data={'text': posttext})
	
	# Create a public post:
	pollalert = 'Another vote in the TEST ' + tag + ' poll.'
	channelurl = "https://patter.chat/room/" + channelid
	# Removed hash before tag:
	channelurlmd = '[' + tag + ' <=>](' + channelurl + ")"
	pollalert += "\n" + channelurlmd
	postcontent = pnutpy.api.create_post(data={'text': pollalert})
