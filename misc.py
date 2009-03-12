#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

import re
import md5

REWORDS=re.compile("([a-zA-Z]{3,})")
SCRIPTS=re.compile("(<script[^>]*>([^<]|<[^s]|<s[^c]|<sc[^r]|<scr[^i]|<scri[^p])*</script>)",re.I)
TAG=re.compile("<[^>]*>")

def getResponseWords (resp):   ### Divide una response en las palabras que la componen
	words={}
	str=resp.getContent()

		

	for i,j in SCRIPTS.findall(str):
		str=str.replace(i,"")
	str=TAG.sub("",str)

	for j in REWORDS.findall(str):
		if len(j)>3:
			words[j]=True
	words=words.keys()
	words.sort()

	return words

def distance(words1,words2):
	if not len(words1):
		words1.append('')

#	print words1
#	print "-------============-----------"
#	print words2

	if len(words2)>len(words1):
		tmp=words1
		words1=words2
		words2=tmp

	words3=[]
	for i in words2:
		if i in words1:
			words3.append(i)

	return len(words3)*100/len(words1)

def getRESPONSEMd5 (resp):      ### Obtiene el MD5 de una response
	return md5.new(" ".join(getResponseWords(resp))).hexdigest()
