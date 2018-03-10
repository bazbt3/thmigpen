#!/usr/bin/env python3

# thmigpen
# v0.1 for Python 3.5

# Basis of the recurring repeat modified from: https://stackoverflow.com/questions/2295765/generating-recurring-dates-using-python

# Import date modules:
import dateutil.rrule as dr
import dateutil.parser as dp
import dateutil.relativedelta as drel
import datetime

# Import @33MHz and @thrrgilag's library for interacting with pnut.io:
import pnutpy

start=dp.parse("01/01/2018")   # First Monday in January 2018

# Setup a list of dates, adjust count to something larger, in multiples of 12 (momths):
rr = dr.rrule(dr.MONTHLY,byweekday=drel.MO(1),dtstart=start, count=12)

# What's today's date?:
t = datetime.date.today()
t = t.strftime('%d/%m/%Y')

x = ([d.strftime('%d/%m/%Y') for d in rr[::1]])

# If today is a week to go until #ThemeMonday:
pnut_message = ''
n = 0
while n <= 11:
	tmprev = (x[n])
	if tmprev == t:
		pnut_message = 'There\'s a week to go until #ThemeMonday. Let\'s suggest themes and start a poll before the weekend!'
	n += 1

# If a message gas been created:
if pnut_message != '':
	# Setup pnut.io authorisation:
	tokenfile = open("pnut_app_token.txt", "r")
	token = tokenfile.read()
	token = token.strip()
	pnutpy.api.add_authorization_token(token)

	# Create a public post using the text from pnut_message, add an x-post footer then create the post:
	posttext = pnut_message
	channelurl = "https://patter.chat/room/779"
	channelurlmd = "[#ThemeMonday <=>](" + channelurl + ")"
	posttext += "\n\n" + channelurlmd
	postcontent = pnutpy.api.create_post(data={'text': posttext})
	
	# Create message in channel 779, using ONLY the text from pnut_message:
	channelid = 779
	postcontent = pnutpy.api.create_message(channelid, data={'text': pnut_message})
