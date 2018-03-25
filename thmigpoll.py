#!/usr/bin/env python3

# thmigpoll v0.1.19 for Python 3.5

# A very beta attempt to list respondents to a pnut.io poll, using the poll's hashtag.
# Based on rssupdatepnut and thmigpen.

# Setup tag and channel parameters, a list of valid poll options, and an empty list for votes: 
tag = 'dst2018'
# description is displayed in braces:
tagdescribe = 'Have you changed clocks to summer time yet?'
retrievecount = 50
channelid = '962'
polloptions = {
	'#no': 0,
	'#yes': 0,
	'#noneedto': 0,
	'#2weeksago': 0,
	'#notagain': 0
	}
votes = []

# Import @33MHz and @thrrgilag's library for interacting with pnut.io:
import pnutpy

# Import module to work out the maximum votes within the dict:
import operator

# Import time, used to delay posting to avoid rate limits:
import time

# Setup pnut.io authorisation:
tokenfile = open("pnut_app_token.txt", "r")
token = tokenfile.read()
token = token.strip()
pnutpy.api.add_authorization_token(token)

# Open vote post numbers file:
f = open('pollpostnumbers.txt', 'r')
y = f.readlines()
f.close()

# List the poll options:
posttext = 'The choices in #' +  tag + ' (' + tagdescribe + ') are:\n'
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
	newvote = False
	try:
		validvote = False
		if not "is_deleted" in d[0][number]:
			user = str(d[0][number]["user"]["username"])
			votepost = d[0][number]["content"]["text"]
			postnum = str(d[0][number]["id"])
			words = votepost.split()
			# If '<=>' does not appears in a post it's not a notification, so process it:
			if not ('<=>' in votepost):
				for word in words:
					if ('#' in word):
						if word != ('#' + tag):
							votesmade = True
							hashtag = word
							if (hashtag in polloptions):
								validvote = True
								votes.append(hashtag)
							if not (hashtag in polloptions):
								validvote = False
		if votesmade and (not ('<=>' in votepost)):
			# Save the post number to a file:
			if not postnum in y:
				f.write(str(postnum) + '\n')
				# Reply if the vote is valid:
				if validvote and (not (postnum + '\n') in y):
					newvote = True
					thankstext = '@' + user + ' Thanks for your vote! (' + postnum + ')\n'
					
					channelurl = "https://patter.chat/room/" + channelid
					channelurlmd = '[See here for the current poll. <=>](' + channelurl + ')'
					thankstext += channelurlmd
					pnutpy.api.create_post(data={'reply_to': postnum, 'text': thankstext})
					# Delay to avoid rate limits:
					time.sleep(3.2)
				
				if (not validvote) and (not (postnum + '\n') in y):
					thankstext = '@' + user + ' Sorry, your vote seems to be invalid. Can you please try again? (' + postnum + ')'
					pnutpy.api.create_post(data={'reply_to': postnum, 'text': thankstext})
					# Delay to avoid rate limits:
					time.sleep(3.2)

			# Create a poll entry if the vote is valid:
			if validvote:
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
	posttext += '\nIf the poll was closed now, ' + winner + ' would win with ' + str(winnervotes) + ' votes!)'

# FOR TESTING, uncomment the lines in this section to prevent the creation of posts & messages:
# print(posttext)
# newvote = False

# If there's text to post:
if newvote:
	# Create message in the chosen channel, using ONLY the text from pnut_message:
	messagecontent = pnutpy.api.create_message(channelid, data={'text': posttext})
	
	# Create a public post:
	pollalert = 'To see the current votes in the TEST #' + tag + '(' + tagdescribe + ') poll go to the Patter room link below. (' + postnum + ')'
	channelurl = "https://patter.chat/room/" + channelid
	# Removed hash before tag:
	channelurlmd = '[' + tag + ' <=>](' + channelurl + ")"
	pollalert += "\n" + channelurlmd
	postcontent = pnutpy.api.create_post(data={'text': pollalert})
