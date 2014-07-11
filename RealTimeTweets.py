from bs4 import BeautifulSoup
import requests
import threading
import re
import datetime
import time

tag1,tag2,tag3 = 'div','class','content'
keywords_options = raw_input('Type the keywords you\'re looking for in a tweet, separated with space:\n')
path_options = raw_input('Save file to a specific path:\n')
list_of_keywords = keywords_options.split()
list_of_tweets = []

def tweets_in_list():
	for key_w in list_of_keywords:
		page = requests.get('https://twitter.com/search?f=realtime&q='+key_w+'&src=typd')
		soup = BeautifulSoup(page.text)
		content = soup.findAll(tag1,{tag2: tag3})
		for tags in content:
			for result in tags.find_all('p'):
				if result.text.encode('utf-8') not in list_of_tweets:
					print 'not in'
					list_of_tweets.append(result.text.encode('utf-8'))
					
def tweets_in_fisier():
	with open(path_options+'tweets.txt', 'a') as fisier:
		print len(list_of_tweets)
		if len(list_of_tweets) >= 110:
			for tw in list_of_tweets[:100]:
				fisier.write(tw+'\n')
			list_of_tweets[:100] = []
			
def last_tweets():
	with open(path_options+'tweets.txt', 'a') as fisier:
		for tw in list_of_tweets:
			fisier.write(tw+'\n')
		list_of_tweets[:] = []
		
def main():
	while True:
		st = datetime.datetime.now().strftime('%H:%M:%S')
		threading.Thread(target=tweets_in_list()).start()
		threading.Thread(target=tweets_in_fisier()).start()
		if st >= '23:59:40':
			threading.Thread(target=last_tweets()).start()
			break
main()
