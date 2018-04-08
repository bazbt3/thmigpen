#!/usr/bin/env python3

# thmigask v0.1.5 for Python 3.5

# A very beta attempt to list suggestions for a pnut.io poll.
# Based on thmigpoll.

# Setup tag and channel parameters, and an empty list for suggestions: 
tag = 'tmask1805'
# description is displayed in braces:
tagdescribe = 'Suggest a theme for May 14'
roomname = '#ThemeMonday'
retrievecount = 50
channelid = '779'
suggestions = []

# Import @33MHz and @thrrgilag's library for interacting with pnut.io:
import pnutpy

# Import time, used to delay posting to avoid rate limits:
import time

# Setup pnut.io authorisation:
tokenfile = open("pnut_app_token.txt", "r")
token = tokenfile.read()
token = token.strip()
pnutpy.api.add_authorization_token(token)

# Open vote post numbers file:
f = open('pollsuggestions.txt', 'r')
y = f.readlines()
f.close()

# Get hashtag content from pnut.io:
d = pnutpy.api.posts_with_hashtag(tag, count = retrievecount)

# Extract posts, strip out unnecessary words, check for matches to poll options, and construct a summary message:
suggestionsmade = False
# Open the previous post numbers file:
f=open('pollsuggestions.txt','w')
posttext = 'The suggestions for #' + tag + ' (' + tagdescribe + ') so far:\n'
number = retrievecount
hashtag = ''
while number >= 0:
	newsuggestion = False
	try:
		validsuggestion = False
		if not "is_deleted" in d[0][number]:
			user = str(d[0][number]["user"]["username"])
			suggestionpost = d[0][number]["content"]["text"]
			postnum = str(d[0][number]["id"])
			words = suggestionpost.split()
			# If '<=>' does not appears in a post it's not a notification, so process it:
			if not ('<=>' in suggestionpost):
				for word in words:
					if ('#' in word):
						if word != ('#' + tag)or word != '#ThemeMonday':
							suggestionsmade = True
							validsuggestion = True
							hashtag = word
							suggestions.append(hashtag)
		if suggestionsmade and (not ('<=>' in suggestionpost)):
			# Save the post number to a file:
			if not postnum in y:
				f.write(str(postnum) + '\n')
				# Reply if the vote is valid:
				if validsuggestion and (not (postnum + '\n') in y):
					newsuggestion = True
					thankstext = '@' + user + ' Thanks for your suggestion! (' + postnum + ')\n'
					
					channelurl = "https://patter.chat/room/" + channelid
					channelurlmd = '[See here for other suggestions. <=>](' + channelurl + ')'
					thankstext += channelurlmd
					pnutpy.api.create_post(data={'reply_to': postnum, 'text': thankstext})
					# Delay to avoid rate limits:
					time.sleep(3.2)
				
				if (not validsuggestion) and (not (postnum + '\n') in y):
					thankstext = '@' + user + ' Sorry, your suggestion seems invalid. Can you please try again? (' + postnum + ')'
					pnutpy.api.create_post(data={'reply_to': postnum, 'text': thankstext})
					# Delay to avoid rate limits:
					time.sleep(3.2)

			# Create a poll entry if the vote is valid:
			if validsuggestion:
				posttext += '• @' + user + ' suggested ' + hashtag + '\n'			
	except IndexError:
		pass
	number -= 1
f.close()

# Tidy the message if no-one suggested yet:
if (not suggestionsmade):
	newsuggestion = True
	postnum = 0
	posttext += '• No-one responded yet; why not be first?! Simply create a public post using #' + tag + ' with your suggestion, not forgetting the hash.\n'

# FOR TESTING, uncomment the lines in this section to prevent the creation of posts & messages:
# print(posttext)
# newsuggestion = False

# If there's text to post:
if newsuggestion:
	# Create message in the chosen channel, using ONLY the text from pnut_message:
	messagecontent = pnutpy.api.create_message(channelid, data={'text': posttext})
	
	# Create a public post:
	suggestionalert = 'To see suggestions for #' + tag + ' (' + tagdescribe + ') see the chatroom link below. Please suggest in public, not the channel.\n'
	channelurl = "https://patter.chat/room/" + channelid
	# Removed hash before tag:
	channelurlmd = '[' + roomname + ' <=>](' + channelurl + ")"
	suggestionalert += channelurlmd + '\n(' + str(postnum) + ')'
	postcontent = pnutpy.api.create_post(data={'text': suggestionalert})
