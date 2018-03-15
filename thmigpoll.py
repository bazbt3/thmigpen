#!/usr/bin/env python3

# thmigpoll
# A very alpha attempt to list respondents to a pnut.io poll, using an RSS feed of the poll's hashtag
# v0.1.thmigpoll.7 for Python 3.5

# Based on rssupdatepnut and thmigpen.

# Setup tag and channel parameters, a list of valid poll options, and an empty list for votes: 
tag = 'tm201804'
channelid = '962'
polloptions = {
	'#ketchup': 0,
	'#mustard': 0,
	'#ketchupnmustard': 0
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

# Open vote post numbers file:
y = open('pollpostnumbers.txt', 'r')
y = y.readlines()

# List the poll options:
posttext = 'The choices in #' +  tag + ' are:\n'
for option in polloptions:
	posttext += '• ' + option + '\n'
posttext += '\n'

# Get hashtag RSS feed from pnut.io:
feed_title = 'https://api.pnut.io/v0/feed/rss/posts/tags/' + tag
d = feedparser.parse(feed_title)

# Extract posts, strip out unnecessary words, check for matches to poll options, and construct a summary message:
n = 0
votesmade = False
# Save the list to file:
f=open('pollpostnumbers.txt','w')
posttext += 'The votes so far:\n\n'
for post in d:
	try:
		p_title = d.entries[n].title
		# Extract words from post:
		words = p_title.split()
		for word in words:
			if ('@' in word):
				word = word.strip('@')
				word = word.strip(':')
				user = word
				votesmade = True
			if not ('#' in word):
				hashtag = 'nothing (no hashtag included, oops!) Please try again'
			if ('#' in word):
				if word != ('#' + tag):
					hashtag = word
					votes.append(hashtag)
					if not (hashtag in polloptions):
						hashtag += ', but it\'s not a candidate. Please try again'
		if votesmade:
			# Extract post number from link:
			p_link = d.entries[n].link
			postnum = p_link.strip('https://posts.pnut.io/')
			postnum = postnum.split('#')[0]
			# Save the post number to a file:
			if not (postnum in y):
				f.write(str(postnum) + '\n')
			# Create a poll entry:
			posttext += '@' + user + ' voted for ' + hashtag + '. (Post ' + str(postnum) + '.)\n\n'
		n += 1
	except IndexError:
		pass
f.close()

# Tidy the message if no-one voted yet:
if not votesmade:
	posttext += '• No-one voted yet. Why not be first?!\n'

# Total votes:
if votesmade:
	posttext += 'Total votes for each option:\n'
	for vote in votes:
		if vote in polloptions:
			polloptions[vote] += 1
	for vote in polloptions:
		posttext += '• ' + str(polloptions[vote]) + ' ' + vote + '\n'	

# FOR TESTING, uncomment the lines in this section to prevent the creation of posts & messages:
# print(posttext)
# posttext = ''

# If there's text to post:
if posttext:
	# Create message in channel 962, using ONLY the text from pnut_message:
	messagecontent = pnutpy.api.create_message(channelid, data={'text': posttext})
	
	# Create a public post:
	pollalert = 'The current state of the votes in the TEST #' + tag + ' poll. (Not run automatically.)'
	channelurl = "https://patter.chat/room/" + channelid
	# Removed hash before tag:
	channelurlmd = '[' + tag + ' <=>](' + channelurl + ")"
	pollalert += "\n" + channelurlmd
	postcontent = pnutpy.api.create_post(data={'text': pollalert})
