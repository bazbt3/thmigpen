#!/usr/bin/env python3

# thmigpoll
# A very alpha attempt to list respondents to a pnut.io poll, using an RSS feed of the poll's hashtag
# v0.1 for Python 3.5

# Based on rssupdatepnut and thmigpen.

# Setup tag and channel parameters, a list of valid poll options, amd an empty list to store votes: 
tag = 'tmpoll'
channelid = '962'
polloptions = {
	'#test': 0,
	'#test1': 0,
	'#test2': 0
	}
votes = []

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

print(d,'\n')

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
			if ('#' in word):
				if word != ('#' + tag):
					hashtag = word
					votes.append(hashtag)
					if not (hashtag in polloptions):
						hashtag += '. Rejected'
		n += 1
		posttext += '• @' + user + ' voted for ' + hashtag + ' in #' + tag + '.\n'
	except IndexError:
		pass

# Total votes:
posttext += '\nLeaderboard:\n'
for vote in votes:
	if vote in polloptions:
		polloptions[vote] += 1
for vote in polloptions:
	posttext += str(polloptions[vote]) + ' ' + vote + '\n'	

# Uncomment both lines to prevent posts & messages whilst testing:
print(posttext)
posttext = ''

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
