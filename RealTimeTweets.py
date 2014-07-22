from twython import TwythonStreamer
import datetime

APP_KEY = '...'
APP_SECRET = '...'
ACCESS_TOKEN = '...'
ACCESS_TOKEN_SECRET = '...'
path_options = raw_input('Save file to a specific path:\n')
word_to_track = 'Forex,$usd' # pentru a cauta mai multe cuvinte: ex: 'Forex,dubai,obama,$USD....'
keys_from_dict = 'text'
list_of_tweets = []

class Tweeter(TwythonStreamer):
	def on_success(self, data):
		endtime = datetime.datetime.now().strftime('%H:%M:%S')
		today = datetime.date.today()
		list_of_tweets.append(data[keys_from_dict].encode('utf-8')+'\n')	
		with open(path_options+str(today)+'Tweets.txt', 'a+') as fisier:
			if endtime >= '23:59:30':
				for tw in list_of_tweets:
					fisier.write(tw+'\n')
				list_of_tweets[:] = []			
				self.disconnect()
			if len(list_of_tweets) >= 110:
				for tw in list_of_tweets[:100]:
					fisier.write(tw+'\n')
				list_of_tweets[:100] = []			
			
	def on_error(self, status_code, data):
		print status_code
		
def main():
	stream = Tweeter(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	stream.statuses.filter(track=word_to_track)

if __name__ == "__main__":
	main()