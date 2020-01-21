import requests
import math
import sys
import re
import os
import numpy as np
import PIL.Image

def joinImagesHorizontal(list_im, nameOut, goodImages):
	imgs    = [ PIL.Image.open(i).convert('RGB') for i in list_im ]
	min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs], reverse=True)[0][1] # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
	imgs_comb = np.hstack( list((np.asarray( i.resize(min_shape, PIL.Image.BILINEAR) ) for i in imgs )) )
	# save that beautiful picture
	imgs_comb = PIL.Image.fromarray( imgs_comb)
	imgs_comb.save( "auxi/"+nameOut+'.jpg' )    

def joinImagesVertical(list_im, nameOut):
	imgs    = [ PIL.Image.open(i).convert('RGB') for i in list_im ]
	# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
	min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs],  reverse=True)[0][1]
	imgs_comb = np.vstack( list((np.asarray( i.resize(min_shape) ) for i in imgs )) )
	imgs_comb = PIL.Image.fromarray( imgs_comb)
	print("Generating " +nameOut+'fi.jpg')
	imgs_comb.save( nameOut+'fi.jpg' )
	
def generateCompleteImage(imgPile, nameOut):
	allImages = len(imgPile)
	numCol=10
	numRows=allImages%numCol
	i = 0
	imgJoin = []
	while i < (numRows-1):
		start=(i*numCol)
		final=(i*numCol+numCol)
		if(final>=allImages):
			diferencia=final-allImages
			j=0
			while j < diferencia:
				imgPile.append("auxi/back.jpg")
				j +=1
		if(start<allImages):
			joinImagesHorizontal(imgPile[start:final], str(i), allImages)
			imgJoin.append("auxi/"+str(i)+'.jpg')
		i += 1
	joinImagesVertical(imgJoin, nameOut)

	
if(len(sys.argv) < 2):
	print("python.exe .\downloadJaeke.py 'link'")
else:
	os.makedirs("auxi/", exist_ok=True)
	os.makedirs("img/", exist_ok=True)
	numImage=0
	imgPile = []
	regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	reverseCardUrl="http://cloud-3.steamusercontent.com/ugc/804367798108512107/91DF58F3EE3DC17AFA6A23A87DA7472FFB8CE5F5/"
	reverseName="auxi/back.jpg"
	f = open(reverseName,'wb')
	f.write(requests.get(reverseCardUrl).content)
	f.close()
	for link in sys.argv[1:]:
		if(re.match(regex,link)):
			fUrl = requests.get(link)
			text = fUrl.text
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
			urls = list( dict.fromkeys(urls) )  
			for url in urls:
				if(url.find("d12h0em1d7ppg.cloudfront.net/items/") != -1):
					urlBona=url
					extension=urlBona[-3:]
					nameImg="img/"+str(numImage)+'.'+extension
					f = open(nameImg,'wb')
					imgPile.append(nameImg)
					f.write(requests.get(urlBona).content)
					f.close()
					numImage += 1
					
					
				if(url.find("thumb_") != -1):
					urlBona=url.replace('thumb_','')
					extension=urlBona[-3:]
					nameImg="img/"+str(numImage)+'.'+extension
					f = open(nameImg,'wb')
					imgPile.append(nameImg)
					f.write(requests.get(urlBona).content)
					f.close()
					numImage += 1
				
				if(url.find("thumbnaildb?") != -1):
					urlBona=url.replace('thumbnaildb?image=','markdb?id=')
					extension="jpg"
					nameImg="img/"+str(numImage)+'.'+extension
					f = open(nameImg,'wb')
					imgPile.append(nameImg)
					print(urlBona)
					print(nameImg)
					f.write(requests.get(urlBona).content)
					f.close()
					
					imageTMP=PIL.Image.open(nameImg).convert('RGB')
					coordinate = x, y = 20, 100
					c = imageTMP.getpixel( coordinate )
					if(c == (255, 255, 255)):
						imageTMP=imageTMP.crop((35,35,780,1075))
					imageTMP.save(nameImg)
					
					numImage += 1
				
	numImages=69
	lenPileImages=len(imgPile)
	allImagesTotals = math.trunc(lenPileImages / numImages)
	i=0
	while i <= allImagesTotals:
		start=(i*numImages)
		final=(i*numImages+numImages)
		if(final>=lenPileImages):
			#final=lenPileImages-1
			diferencia=final-lenPileImages
			j=0
			while j < diferencia:
				imgPile.append("auxi/back.jpg")
				j +=1
		generateCompleteImage(imgPile[start:final], str(i))
		i += 1
	