#!/usr/bin/env python3

# thmigpoll v0.1.12 for Python 3.5

# A quite alpha attempt to list respondents to a pnut.io poll, using the poll's hashtag.
# Based on rssupdatepnut and thmigpen.

# Setup tag and channel parameters, a list of valid poll options, and an empty list for votes: 
tag = 'tmpoll'
retrievecount = 50
channelid = '962'
polloptions = {
	'#test': 0,
	'#test1': 0,
	'#test2': 0
	}
votes = []

# Import @33MHz and @thrrgilag's library for interacting with pnut.io:
import pnutpy

# Import module to work out the maximum votes within the dict:
import operator

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

# Get hashtag content from pnut.io:
d = pnutpy.api.posts_with_hashtag(tag, count = retrievecount)

# Extract posts, strip out unnecessary words, check for matches to poll options, and construct a summary message:
votesmade = False
# Open the previous post numbers file:
f=open('pollpostnumbers.txt','w')
posttext += 'The votes so far:\n'
number = retrievecount
hashtag = ''
while number >= 0:
	try:
		if not "is_deleted" in d[0][number]:
			user = str(d[0][number]["user"]["username"])
			p_title = d[0][number]["content"]["text"]
			postnum = str(d[0][number]["id"])
			words = p_title.split()
			# If '<=>' does not appears in a post it's not a notification, so process it:
			if not ('<=>' in p_title):
				for word in words:
					if not ('#' in word):
						hashtag = 'nothing (no hashtag included, oops!) Please try again.'
					if ('#' in word):
						if word != ('#' + tag):
							votesmade = True
							hashtag = word
							votes.append(hashtag)
							if not (hashtag in polloptions): 
								hashtag += ', which is not a candidate. Please try again.'
		if votesmade:
			# Save the post number to a file:
			if not (postnum in y):
				f.write(str(postnum) + '\n')
			# Create a poll entry:
			posttext += '• @' + user + ' voted for ' + hashtag + '\n'
	except IndexError:
		pass
	number -= 1
f.close()

# Tidy the message if no-one voted yet:
if not votesmade:
	posttext += '• No-one has voted yet. Why not be first?! Simply create a public post using #' + tag + ' and your choice, not forgetting the hash.\n'

# Total votes:
if votesmade:
	posttext += '\nTotal votes for each option:\n'
	for vote in votes:
		if vote in polloptions:
			polloptions[vote] += 1
	for vote in polloptions:
		posttext += '• ' + str(polloptions[vote]) + ' ' + vote + '\n'	

# Summarise the intermediate result:
if votesmade:
	winner = (max(polloptions.items(), key=operator.itemgetter(1))[0])
	winnervotes = (max(polloptions.items(), key=operator.itemgetter(1))[1])
	posttext += '\nIf the poll was closed now, ' + winner + ' would win with ' + str(winnervotes) + ' votes!'

# FOR TESTING, uncomment the lines in this section to prevent the creation of posts & messages:
# print(posttext)
# posttext = ''

# If there's text to post:
if posttext:
	# Create message in channel 962, using ONLY the text from pnut_message:
	messagecontent = pnutpy.api.create_message(channelid, data={'text': posttext})
	
	# Create a public post:
	pollalert = 'To see the current votes in the TEST #' + tag + ' poll go to the Patter room link below. (Report not run automatically.)'
	channelurl = "https://patter.chat/room/" + channelid
	# Removed hash before tag:
	channelurlmd = '[' + tag + ' <=>](' + channelurl + ")"
	pollalert += "\n" + channelurlmd
	postcontent = pnutpy.api.create_post(data={'text': pollalert})
