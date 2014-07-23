from twython import TwythonStreamer
import datetime
import threading
from Queue import Queue

APP_KEY = 'eRkLvy8ZrplK0BJxpkLbT5pYO'
APP_SECRET = 'lihgnO8ZnBsPoBYQAy4oI2iUQY3iSuFvf867RElWHgj8CF0DVy'
ACCESS_TOKEN = '2574597132-wNsBwJtHd1VZPFoP2iucrXNzzscROzpMEUpUJkt'
ACCESS_TOKEN_SECRET = 'oaQypcrlTlQT9BMEVLG4s8YbVo30cQcfbbuPuX1AfGkt5'
path_options = raw_input('Save file to a specific path:\n')
word_to_track = 'RT,and,tweet' # pentru a cauta mai multe cuvinte: ex: 'Forex,dubai,obama,$USD....'

class Tweeter(TwythonStreamer):
	queue = Queue(maxsize = 0)	
	start_date = datetime.date.today()
	file = open(path_options+str(datetime.date.today())+'Tweets.txt', 'a')
	
	def process_tweets(self):
		if (datetime.date.today() > self.start_date):
			self.file = open(path_options+str(datetime.date.today())+'Tweets.txt', 'a')
			self.start_date = datetime.date.today()
		buffer = ""		
		while not self.queue.empty():
			buffer = buffer + self.queue.get() + '\n'				
			self.queue.task_done()			
		print buffer
		self.file.write(buffer)		
	
	def on_success(self, data):	
		self.queue.put(str(data) + '\n')
		if (self.queue.qsize() > 100):
			print self.queue.qsize()
			self.process_tweets()
			print self.queue.qsize()
			
	def on_error(self, status_code, data):
		print status_code
		
	def disconnect(self):
		super(Tweeter, self).disconnect()
		self.process_tweets()
		self.queue.join()
		self.file.close()
			
def exitf(stream):	
	while 1:
		exit = raw_input("Type E for exit...")
		if exit == "E":
			stream.disconnect()
			break
			
def main():
	stream = Tweeter(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)		
	threading.Thread(target = exitf, args=(stream,)).start()	
	threading.Thread(target=lambda: stream.statuses.filter(track=word_to_track)).start()

if __name__ == "__main__":
	main()