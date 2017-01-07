from __future__ import division
import os, re, glob, string
from collections import Counter
#from nltk.corpus import stopwords


# http://stackoverflow.com/questions/8703017/remove-sub-string-by-using-python
tagFilter = "<.*?>" 
# http://emailregex.com/
emailIdFilter = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" #2

ipFilter = "[0-9]+(?:\.[0-9]+){3}" #3

punctuationFilter = re.escape(string.punctuation)
# http://stackoverflow.com/questions/5197959/how-do-i-remove-hex-values-in-a-python-string-with-regular-expressions
hexFilter = "^\x20-\x7a"

# http://stackoverflow.com/questions/10340615/matching-multiple-kinds-of-dates-timestamps-using-regex
full_pattern = r'\w{3,4}\W\s\d{1,2}\s\w{3}\s\d{4}\s\d{2}:\d{2}:\d{2}'
time_pattern = r'\d{1,2}:\d{2}(\s(A|P)M)?'
combo_regex = '(%s)' % ('|'.join([full_pattern, time_pattern]),)

# http://stackoverflow.com/questions/22520932/python-remove-all-non-alphabet-chars-from-string
nonNumeric = "[^a-zA-Z]{3,4}"

cachedStopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', \
'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', \
'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', \
'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', \
'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', \
'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', \
'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', \
'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', \
'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', \
'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', \
'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', \
'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', \
'isnt', 'may', 'mightnt', 'mustnt', 'neednt', 'shant', 'shouldnt', 'wasnt', 'werent', 'wont', 'wouldnt']

stopWords1 = [u'a', u'about', u'above', u'after', u'again', u'against', u'all', u'am', u'an', \
u'and', u'any', u'are', u"aren't", u'as', u'at', u'be', u'because', u'been', u'before', \
u'being', u'below', u'between', u'both', u'but', u'by', u"can't", u'cannot', u'could', \
u"couldn't", u'did', u"didn't", u'do', u'does', u"doesn't", u'doing', u"don't", u'down',\
 u'during', u'each', u'few', u'for', u'from', u'further', u'had', u"hadn't", u'has', u"hasn't",\
  u'have', u"haven't", u'having', u'he', u"he'd", u"he'll", u"he's", u'her', u'here', u"here's", \
  u'hers', u'herself', u'him', u'himself', u'his', u'how', u"how's", u'i', u"i'd", u"i'll", u"i'm", \
  u"i've", u'if', u'in', u'into', u'is', u"isn't", u'it', u"it's", u'its', u'itself', u"let's", u'me', \
  u'more', u'most', u"mustn't", u'my', u'myself', u'no', u'nor', u'not', u'of', u'off', u'on', u'once', \
  u'only', u'or', u'other', u'ought', u'our', u'ours', u'ourselves', u'out', u'over', u'own', u'same', u"shan't", \
  u'she', u"she'd", u"she'll", u"she's", u'should', u"shouldn't", u'so', u'some', u'such', u'than', u'that', \
  u"that's", u'the', u'their', u'theirs', u'them', u'themselves', u'then', u'there', u"there's", u'these', \
  u'they', u"they'd", u"they'll", u"they're", u"they've", u'this', u'those', u'through', u'to', u'too', \
  u'under', u'until', u'up', u'very', u'was', u"wasn't", u'we', u"we'd", u"we'll", u"we're", u"we've", u'were', \
  u"weren't", u'what', u"what's", u'when', u"when's", u'where', u"where's", u'which', u'while', u'who', u"who's", \
  u'whom', u'why', u"why's", u'with', u"won't", u'would', u"wouldn", 'you' \
  u'your', u'yours', u'yourself', u'yourselves']

uglyWords = ["also","value", "a","abbr","acronym","address","area","b","base","bdo","big","blockquote","body","br","button",\
"caption","cite","code","col","colgroup","dd","del","dfn","div","dl","DOCTYPE","dt","em","fieldset","form","h1","h2","h3","h4",\
"h5","h6","head","html","hr","i","img","input","ins","kbd","label","legend","li","link","map","meta","noscript","object","ol",\
"optgroup","option","you","your","p","param","pre","q","samp","script","select","small","span","strong","style","sub","sup","table","tbody",\
"td","textarea","tfoot","th","thead","title","tr","tt","ul","var","mon","tue","wed","thu","fri","sat","sun",\
"jan","feb","mar","apr","may","jun","july","aug","sep","oct","nov","dec"]

USStates = ['washington', 'wisconsin', 'virginia', 'florida', 'wyoming', 'hampshire', 'jersey', 'mexico', 'national', 'carolina', \
'dakota', 'nebraska', 'york', 'rhode island', 'nevada', 'guam', 'colorado', 'california', 'georgia', 'connecticut', 'oklahoma', \
'ohio', 'kansas', 'kentucky', 'oregon',  'delaware', 'columbia', 'hawaii', 'puerto rico', 'texas', 'louisiana', 'tennessee', 'pennsylvania', 'virginia', 'virgin islands', 'alaska', 'alabama', 'american samoa', 'arkansas', 'vermont', 'illinois', 'indiana', 'iowa', 'arizona', 'idaho', 'maine', 'maryland', 'massachusetts', 'utah', 'missouri', 'minnesota', 'michigan', 'montana', 'northern mariana islands', 'mississippi']

directions = ['north', 'south', 'east', 'west']

technicalWords = ['example','version','emails','daemon','index','ascii','sites','site','msmail','mailto', 'groups'	\
'outlook','yahoo','hotmail','com', 'org','net', 'type', 'radio', 'name', 'smtp', 'localhost', 'redhat', 'sender'\
'mime','mail','email','align','mailing','linux','imap','center', 'received', 'admin','users','header','mailman','yahoogroups']

days = ["mon","tue","wed","thu","fri","sat","sun"]
months = ["jan","feb","mar","apr","may","jun","july","aug","sep","oct","nov","dec"]



# @staticmethod
def vowelToLenRatio(word):
	ratio= sum(map(word.count, "aeiou")) / len(word)
	return True if ratio >0.3 and ratio<0.7 else False

# @staticmethod
def cleanLine(line):
	junk = line.lower()
	f0 = re.sub(combo_regex,'',junk)
	f1 = re.sub(tagFilter,'',f0)
	f2 = re.sub(emailIdFilter,'',f1)
	f3 = re.sub(ipFilter,'',f2)
	f4 = re.sub('[0-9]',' ',f3)
	f5 = re.sub(nonNumeric,'',f4)
	refined_line  = re.findall("\w+",f5)
	more_refined_line = []
	for x in refined_line:
		if x not in cachedStopWords and len(x) > 3 and len(x) < 12 and x not in uglyWords and x not in USStates:
			if vowelToLenRatio(x) and x not in directions and x not in technicalWords:
				more_refined_line.append(x)
	moreCleanedLine = [x for x in more_refined_line if x != []]
	return moreCleanedLine
 
# fileName = "train/spam/0008.9562918b57e044abfbce260cc875acde"
# spamDirPath = "train/spam/*.*"
# notSpamDirPath = "train/notspam/*.*"
'''
def getCount(dirPath):
	listOfFiles = glob.glob(dirPath)
	total = []
	print "# of files : ",len(listOfFiles)
	for fileName in listOfFiles:		
		with open(fileName,"r") as f:
			cleanedLine = [cleanLine(line) for line in f if line.strip()]
			moreCleanedLine = [x for x in cleanedLine if x != []]
			for e in moreCleanedLine:
				#total.update(e)
				for i in e:
					total.append(i)

	c = Counter(total)
	big_list = Counter(el for el in c.elements() if c[el] > 1)
	big_list = big_list.most_common(1000)
	return big_list
	'''
		#print total
	# w = open("train/wc_"+str(len(listOfFiles))+"_count.out","w")
	# # sorted(big_list, key=big_list.get, reverse=True)

	# for item in big_list:
	# 	w.write(str(item)+"\n")
	# w.close()
	# return len(big_list)

# print "No. of words in spam dir ", getCount(spamDirPath)
# print "No. of words in notspam dir ", getCount(notSpamDirPath)
