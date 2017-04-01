#coding:utf-8
import urllib2
import urllib
import json
import sys
import os
import time
import re
import Queue 
import thread
import threading
# import jieba
# import chardet
from bs4 import BeautifulSoup
import httplib
from lxml import etree
import json
import requests
import lxml.html
import lxml.etree
from decimal import Decimal

import socket
socket.setdefaulttimeout(10.0) 

reload(sys)
sys.setdefaultencoding('utf-8') 

sess = requests.session()

CorpusSize = 20 # the number of pages will be extract from baidu search

def getWordsUrl(item):
	url = 'http://www.baidu.com/s?wd=' + item + '&rn=' + str(CorpusSize)
	r = sess.get(url)

	xpath =  u"///h3/a/@href"
	html = r.text.decode('utf8')
	html_map = lxml.etree.HTML(html.decode('utf8'))
	node = html_map.xpath(xpath)
	seen = set()
	a = [str(x) for x in node if x not in seen and not seen.add(x)]
	return a



# titleKeyWords = titleTag.contents[0]
# cutWords(titleKeyWords)

def saveHtmls(links, localpath):
	print("save htmls in dir " + localpath)
 	if not os.path.exists(localpath):
 		os.mkdir(localpath)
 	counter = len(os.listdir(localpath))
 	print("目录下已有" + str(counter) + "个文档")
 	f = open(localpath + "/urls.txt", "w")
	for link in links:
		try:
			downloadPage(link, counter, localpath)
			f.write(link +"\n")
		except Exception,e:  
			continue  
		finally:
			counter += 1
			print("小黄图+1,已有" + str(counter) + "张小黄图")	
	f.close()		
	return

def downloadPage(link, counter, localpath):
	req = urllib2.urlopen(link, timeout=5)
	html = req.read()
	soup = BeautifulSoup(html, "lxml")
	for script in soup.findAll('script'):
		script.extract()
	for style in soup.findAll('style'):
		style.extract() 
	soup.prettify()
	reg1 = re.compile("<[^>]*>")
	content = reg1.sub('',soup.prettify())	
	# print(content)

	f = open(localpath + "/" + str(counter + 1)+".txt", "w")
	f.write(content) 
	f.close()

	return

def getTagCorpus(url, tagLocalpath):
	req = urllib2.urlopen(url)
	page = req.read()
	cont = json.loads(page)
	counter = 0

	f = open(tagLocalpath + "/map.txt", "w")

	# parse json
	for item in cont['results']:
	    counter += 1
	    f.write(str(counter)+"\t" + item +"\n")
	    print(item)
	    localpath = tagLocalpath + "/" + str(counter)
	    if not os.path.exists(localpath):
	    	os.mkdir(localpath)
	    time.sleep(1)
	    links = getWordsUrl(item)
	    saveHtmls(links, localpath)
	
	f.close
	print("Number of titles in this Tag: ", counter)

	return




# main
# done: music, product, video, restaurant, 
# to do: movie, news, question, travel

KeyMaps = {"product":["title", "description", "price", "salesVolume", "score", "freight","promotionalInfo", "tags"],\
"restaurant":["title", "description", "price", "score", "salesVolume", "freight", "tel", "address", "openTime", "longitude", "latitude"],\
"video":["title", "description", "uploader", "uploadTime", "videoTime", "playCount", "commentCount", "comments", "tags"],\
"movie":["title", "description","score", "director", "star", "language", "countries", "movieType", "evaluateCount", "comments", "releaseTime", "movieTime", "tags"],\
"music":["title", "singer", "lyricist", "composer", "lyric", "musicTime", "album", "tags", "releaseTime", "commentCount", "comments"],\
"news":["title", "writer", "description", "press", "publishedDate"],\
"question":["questionTime", "answerWriter", "answerContent", "answerTime"],\
"travel":["title", "city", "address", "description", "trafficInfo"]\
}
size = 100

api = "http://60.205.139.71:8080/MobileSearch/api/dataset!get.action?"

corpusName = "corpus-" + str(CorpusSize) + "PagesPerItem"

if not os.path.exists(corpusName):
	os.mkdir(corpusName)

for typeName in KeyMaps:
	fieldNameList = KeyMaps[typeName]
	for fieldName in fieldNameList:
		tagLocalpath = corpusName + "/" + typeName + "-" + fieldName + "-" + str(size)		
		if not os.path.exists(tagLocalpath):
			os.mkdir(tagLocalpath)
			url= api + "typeName="+ typeName + "&fieldName=" + fieldName + "&size=" + str(size)
			print(url)
			getTagCorpus(url, tagLocalpath)


		