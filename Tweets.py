from twython import Twython

APP_KEY = 'eRkLvy8ZrplK0BJxpkLbT5pYO'
APP_SECRET = 'lihgnO8ZnBsPoBYQAy4oI2iUQY3iSuFvf867RElWHgj8CF0DVy'
ACCESS_TOKEN = '2574597132-wNsBwJtHd1VZPFoP2iucrXNzzscROzpMEUpUJkt'
ACCESS_TOKEN_SECRET = 'oaQypcrlTlQT9BMEVLG4s8YbVo30cQcfbbuPuX1AfGkt5'
twitter = Twython(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

keywords_options = raw_input('Type the keywords you\'re looking for in a tweet, separated with space:\n')
path_options = raw_input('Save file to a specific path:\n')
list_of_keywords = keywords_options.split()
for keywords in list_of_keywords:
	tw = twitter.search(q = keywords, count = 100)
	with open(path_options+keywords+'.txt', 'w') as fisier:
		for tweets in tw['statuses']:
			if tweets['lang'] == 'en':
				try:
					fisier.write(tweets['text']+'\n\n')
				except UnicodeEncodeError:
					pass
		