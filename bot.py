#! /usr/bin/python

import asyncio
import discord, aiohttp, os
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime

# Enviroment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
ANCHOR_EMAIL = os.getenv('ANCHOR_EMAIL')
ANCHOR_PASSWORD = os.getenv('ANCHOR_PASSWORD')
WEEKLY_TIME = os.getenv('WEEKLY_TIME')
PRINT_MESSAGES_TO_CONSOLE = os.getenv('PRINT_MESSAGES_TO_CONSOLE') and os.getenv('PRINT_MESSAGES_TO_CONSOLE').lower() in {'true', '1'}
SEND_MESSAGES_TO_DISCORD = os.getenv('SEND_MESSAGES_TO_DISCORD') and os.getenv('SEND_MESSAGES_TO_DISCORD').lower() in {'true', '1'}

# Simple constants
BASE_URL = 'https://anchor.fm/api/'
ANALYTICS_URL = BASE_URL + 'proxy/v3/analytics/station/webStationId:{}/{}'
HOURS_IN_A_WEEK = 168
SECONDS_IN_A_WEEK = 604800

# Objects for connections
bot = commands.Bot(command_prefix='.')
cookies = aiohttp.CookieJar()


# HTTP request functions

async def get(session, url):
	async with session.get(url) as res:
		status = None
		body = None
		status = res.status
		if status == 200 and await res.text():
			body = await res.json()
		return status, body

async def post(session, url, body):
	async with session.post(url, json=body) as res:
		status = None
		body = None
		status = res.status
		if status == 200 and await res.text():
			body = await res.json()
		return status, body


# Debugging function

async def error(status, channel, message):
	message = 'Error ' + message[0].lower() + message[1:]
	print(message)
	await channel.send(message)
	if status == 403:
		print('403 Forbidden')
		print('Incorrect token, cookie, or body')
	elif status == 401:
		print('401 Unauthorized')
		print('Incorrect email or password')
	elif status == 429:
		print('429 Too many requests')
	elif status == 500:
		print('500 Server error')
	else:
		print(status)


# Simple string functions

def stringPercent(fraction):
	return str(round(fraction * 100)).rjust(2) + ' %'

def stringDate(timestamp):
	return datetime.fromtimestamp(timestamp).strftime('%a, %b %d').replace('0', '')

def stringTitle(string):
	title = string[0].upper()
	for c in string[1:]:
		if c >= 'A' and c <= 'Z':
			title += ' '
		title += c
	return title


# Data parsing & processing functions

def stringOfPercentages(stats):
	string = ''
	longestTitleLength = 0
	for group in stats:
		title = group[0]
		fraction = group[1]
		length = len(title)
		if fraction and length > longestTitleLength:
			longestTitleLength = length
	for group in stats:
		title = group[0]
		fraction = group[1]
		if fraction:
			title = (title + ':').ljust(longestTitleLength + 2)
			percentage = stringPercent(fraction)
			if string:
				string += '\n'
			string += title + percentage
	return string

def stringOfPlays(stats):
	string = ''
	longestNumber = 0
	for group in stats:
		length = len(str(group[1]))
		if length > longestNumber:
			longestNumber = length
	for group in stats:
		timestamp = group[0]
		number = str(group[1]).rjust(longestNumber)
		date = stringDate(timestamp)
		date = (date + ':').ljust(13)
		if string:
			string += '\n'
		string += date + number
	return string

def stringOfTopEpisodes(stats):
	string = ''
	longestTitle = 0
	longestPlays = 0
	for group in stats:
		title = group[0]
		plays = str(group[1])
		length = len(title)
		if length > longestTitle:
			longestTitle = length
		length = len(plays)
		if length > longestPlays:
			longestPlays = length
	for group in stats:
		title = group[0]
		plays = str(group[1]).rjust(longestPlays)
		title = (title + ':').ljust(longestTitle + 2)
		if string:
			string += '\n'
		string += title + plays
	return string


# Bot functions

@bot.event
async def on_ready():
	get_analytics.start()

@tasks.loop(hours=HOURS_IN_A_WEEK)
async def get_analytics():

	# Set up connection with Discord

	channel = bot.get_channel(DISCORD_CHANNEL_ID)
	if not channel:
		print('Error with Discord channel id')
		print(DISCORD_CHANNEL_ID)
		return

	async with aiohttp.ClientSession(cookie_jar=cookies) as session:


		# Set up connection with Anchor

		analytics = {}

		task = 'Getting token'
		status, body = await get(session, BASE_URL + 'csrf')
		if status != 200:
			await error(status, channel, task)
			return
		anchorToken = body['csrfToken']

		task = 'Logging in'
		body = {
			'email': ANCHOR_EMAIL,
			'password': ANCHOR_PASSWORD,
			'_csrf': anchorToken,
		}
		status, body = await post(session, BASE_URL + 'login', body)
		if status != 200:
			await error(status, channel, task)
			return

		task = 'Getting station id & user id'
		status, body = await get(session, BASE_URL + 'currentuser')
		if status != 200:
			await error(status, channel, task)
			return
		anchorUserId = str(body['user']['userId'])
		anchorWebStationId = str(body['user']['currentWebStationId'])


		# Get statistics

		analytic = 'uniqueListeners'
		task = 'Getting analytic: {}'.format(analytic)
		status, body = await get(session, ANALYTICS_URL.format(anchorWebStationId, analytic))
		if status != 200:
			await error(status, channel, task)
			return
		string = str(body['data']['rows'][0])
		analytics[analytic] = string

		analytic = 'audienceSize'
		task = 'Getting analytic: {}'.format(analytic)
		status, body = await get(session, ANALYTICS_URL.format(anchorWebStationId, analytic))
		if status != 200:
			await error(status, channel, task)
			return
		string = str(body['data']['rows'][0])
		analytics[analytic] = string

		analytic = 'totalPlays'
		task = 'Getting analytic: {}'.format(analytic)
		status, body = await get(session, ANALYTICS_URL.format(anchorWebStationId, analytic))
		if status != 200:
			await error(status, channel, task)
			return
		string = str(body['data']['rows'][0])
		analytics[analytic] = string

		analytic = 'playsByGender'
		task = 'Getting analytic: {}'.format(analytic)
		status, body = await get(session, ANALYTICS_URL.format(anchorWebStationId, analytic))
		if status != 200:
			await error(status, channel, task)
			return
		string = stringOfPercentages(body['data']['rows'])
		analytics[analytic] = string

		analytic = 'playsByAgeRange'
		task = 'Getting analytic: {}'.format(analytic)
		status, body = await get(session, ANALYTICS_URL.format(anchorWebStationId, analytic))
		if status != 200:
			await error(status, channel, task)
			return
		string = stringOfPercentages(body['data']['rows'])
		analytics[analytic] = string

		analytic = 'playsByApp'
		task = 'Getting analytic: {}'.format(analytic)
		status, body = await get(session, ANALYTICS_URL.format(anchorWebStationId, analytic))
		if status != 200:
			await error(status, channel, task)
			return
		string = stringOfPercentages(body['data']['rows'])
		analytics[analytic] = string

		analytic = 'playsByGeo'
		task = 'Getting analytic: {}'.format(analytic)
		status, body = await get(session, ANALYTICS_URL.format(anchorWebStationId, analytic) + '?limit=200&resultGeo=geo2')
		if status != 200:
			await error(status, channel, task)
			return
		string = stringOfPercentages(body['data']['rows'])
		analytics[analytic] = string

		analytic = 'plays'
		task = 'Getting analytic: {}'.format(analytic)
		status, body = await get(session, ANALYTICS_URL.format(anchorWebStationId, analytic))
		if status != 200:
			await error(status, channel, task)
			return
		string = stringOfPlays(body['data']['rows'])
		analytics[analytic] = string

		analytic = 'topEpisodes'
		task = 'Getting analytic: {}'.format(analytic)
		status, body = await get(session, ANALYTICS_URL.format(anchorWebStationId, analytic) + '?limit=10')
		if status != 200:
			await error(status, channel, task)
			return
		string = stringOfTopEpisodes(body['data']['rows'])
		analytics[analytic] = string


		# Send analytics

		if PRINT_MESSAGES_TO_CONSOLE:
			analyticsString = ''
			for key, string in analytics.items():
				title = stringTitle(key)
				if analyticsString:
					analyticsString += '\n\n'
				analyticsString += title + '\n'
				analyticsString += string
			print(analyticsString)

		if SEND_MESSAGES_TO_DISCORD:
			for key, string in analytics.items():
				title = stringTitle(key)
				message = '{}```\n{}```'.format(title, string)
				await channel.send(message)

@get_analytics.before_loop
async def before_get_analytics():
	for _ in range(SECONDS_IN_A_WEEK):
		if datetime.utcnow().strftime('%H:%M UTC %a') == WEEKLY_TIME:
			return

		await asyncio.sleep(30)

bot.run(DISCORD_BOT_TOKEN)
