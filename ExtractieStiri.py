from bs4 import BeautifulSoup
import re
import threading
import time
import datetime
import os
import requests

class Site(threading.Thread):
	continut = ''
	lista_href = []
	lista_text = []
	
	def __init__ (self, nume, path, lock):
		self.nume = nume
		self.path = path
		self.lock = lock
		
	def mod_extractie(self,storyid,tag1,tag2,tag3):
		page = requests.get(storyid)
		soup = BeautifulSoup(page.text)
		continut = soup.find(tag1,{tag2: tag3}) # exemplu: continut = soup.find('div',{'itemprop':'articleBody'})
		self.continut = continut
		return continut

	def extractie_href(self):
		self.lista_href = []
		if self.nume == 'Bloomberg':
			x = self.mod_extractie('http://www.bloomberg.com/news/markets/','ul', 'section_name', 'markets')
		elif self.nume == 'Fxstreet':
			x = self.mod_extractie('http://www.fxstreet.com/news/forex-news/','div', 'class', 'listing-content section')
		for link in x.find_all('a'):
			if (link['href'])[0] == '.':
				(link['href']) = (link['href'])[1:]
			elif (link['href'])[:12] == '/news/fxbeat':
				(link['href']) = (link['href'])[12:]
			self.lista_href.append(link.get('href'))
		return set(self.lista_href)
			
	def extractie_text(self):
		self.lista_text = []
		for x in self.extractie_href():
			if self.nume == 'Bloomberg':
				text = str(self.mod_extractie('http://www.bloomberg.com'+x,'div','itemprop','articleBody'))
				ora = str(self.mod_extractie('http://www.bloomberg.com'+x, 'span', 'class', 'date'))
				titlu = str(self.mod_extractie('http://www.bloomberg.com'+x, 'h1', 'class', 'article_title buffer'))
				if ora != 'None':
					ora = re.sub('<.*?>', '', ora)
					ora2 = datetime.datetime.strptime(ora, ' %Y-%m-%dT%H:%M:%SZ ').strftime('%Y-%m-%d %H-%M-%S')
					titlu = re.sub('<.*?>', '', titlu)
					text = ora2 + 'Bloomberg' + '\n' + titlu + '\n' + text
			elif self.nume == 'Fxstreet':
				text = str(self.mod_extractie('http://www.fxstreet.com/news/forex-news'+x,'div','itemprop','articleBody'))
				ora = str(self.mod_extractie('http://www.fxstreet.com/news/forex-news'+x,'span','itemprop','datePublished'))
				try:
					ora = re.sub('<.*?>', '', ora)[:-4]
					sec = sum([ord(char) - 96 for char in text[76:78].lower()])
					ora = ora + ':' + '%02d' % sec
					ora = datetime.datetime.strptime(ora, '%a, %b %d %Y, %H:%M:%S').strftime('%Y-%m-%d %H-%M-%S')
					text = ora + 'Fxstreet' + '\n' + text
				except ValueError:
					pass
			if '<figure' in text:
				text1 = text[:text.index('<figure')]
				text2 = text[text.index('</figure>'):]
				text = text1 + text2
			text = re.sub(r'<.*?>', '', text)
			text = re.sub('FITITOL-->', '\n', text)
			if 'To contact' in text:
				text = text[:text.index('To contact')]
			self.lista_text.append(text)
			self.lista_text = sorted(self.lista_text)[::-1]
		return self.lista_text

	def scriere_pe_fisier(self):
		self.path = path_options
		verificare_titlu = 'verificare_stire'
		while True:
			lista = []			
			for x in self.extractie_text():
				try:
					titlu_fisier = x[:x.index('\n\n')]
					titlu_fisier = re.sub('[\n?/]', '', titlu_fisier)
					conditie_fisier = x[x.index('\n\n'):x.index('\n\n\n')]
					#conditie_fisier = re.sub('[\n?/]', '', conditie_fisier)
					if verificare_titlu == titlu_fisier:
						break
					lista.append(titlu_fisier)											
					self.lock.acquire()
					fisier = open(self.path+'\\'+titlu_fisier+str(len(conditie_fisier))+'.txt','w')
					fisier.write(x)
					fisier.close()
					self.lock.release()
				except (ValueError,UnboundLocalError):
					pass			
			if lista:
				verificare_titlu = max(lista)
			time.sleep(15)			

options = '[1] Bloomberg\n\n[2] Fxstreet '
user_options = raw_input('\nSelect options:\n\n' + options + '\n') # 1 2 / 1 / 2
path_options = raw_input('Save file to a specific path for every option: \n')
user_dict = {'1':'Bloomberg', '2':'Fxstreet'}

def main():
	thread_list = []
	lock = threading.Lock()
	
	for x in map(int, str(user_options)):
		obiect = Site(user_dict[str(x)], path_options,lock)
		thread_list.append(obiect)
	
	for t in thread_list:
		threading.Thread(target=t.scriere_pe_fisier).start()
if __name__ == "__main__":
    main()