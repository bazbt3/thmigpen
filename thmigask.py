#!/usr/bin/env python3

# thmigask v0.1.0 for Python 3.5

# A quite alpha attempt to list suggestions for a pnut.io poll, using the poll's suggestion hashtag.
# Based on thmigpoll.

# Setup tag and channel parameters, a list of valid poll options, and an empty list for votes: 
tag = 'tmask'
suggestionmade = False
retrievecount = 50
channelid = '962'

# Import @33MHz and @thrrgilag's library for interacting with pnut.io:
import pnutpy

# Setup pnut.io authorisation:
tokenfile = open("pnut_app_token.txt", "r")
token = tokenfile.read()
token = token.strip()
pnutpy.api.add_authorization_token(token)

# Get hashtag content from pnut.io:
d = pnutpy.api.posts_with_hashtag(tag, count = retrievecount)

# Extract posts, strip out unnecessary words, and construct a summary message:
posttext = 'The suggestions for the #' + tag + ' poll so far:\n'
number = retrievecount
hashtag = ''
while number >= 0:
	try:
		if not "is_deleted" in d[0][number]:
			user = str(d[0][number]["user"]["username"])
			suggestion = d[0][number]["content"]["text"]
			postnum = str(d[0][number]["id"])
			words = suggestion.split()
			# If '<=>' does not appear in a post it's not a notification, so process it:
			if not ('<=>' in suggestion):
				for word in words:
					if not ('#' in word):
						hashtag = 'nothing (no hashtag included, oops!) Please try again.'
					if ('#' in word):
						if word != ('#' + tag):
							suggestionmade = True
							hashtag = word
		if suggestionmade:
			# Create a suggestion entry:
			posttext += '• @' + user + ' suggested ' + hashtag + '\n'
	except IndexError:
		pass
	number -= 1

# Tidy the message if no-one voted yet:
if not suggestionmade:
	posttext += '• No-one has suggested a theme yet. Why not be first?! Simply create a public post using #' + tag + ' and your choice, not forgetting the hash.\n'

# FOR TESTING, uncomment the lines in this section to prevent the creation of posts & messages:
# print(posttext)
# posttext = ''

# If there's text to post:
if posttext:
	# Create message in channel 962, using ONLY the text from pnut_message:
	messagecontent = pnutpy.api.create_message(channelid, data={'text': posttext})
	
	# Create a public post:
	pollalert = 'To see the current suggestions for the TEST #' + tag + ' poll go to the Patter room link below. (Report not run automatically.)'
	channelurl = "https://patter.chat/room/" + channelid
	# Removed hash before tag:
	channelurlmd = '[' + tag + ' <=>](' + channelurl + ")"
	pollalert += "\n" + channelurlmd
	postcontent = pnutpy.api.create_post(data={'text': pollalert})
