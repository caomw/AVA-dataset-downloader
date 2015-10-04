#
# Use 'AVA.txt' provided by database author to download all images from 'dpchallenge.com'.
#    This script should be placed under AVA_dataset/script/ and images are saved at
#    AVA_dataset/image/ folder.
#
# Author: Wei Zhen @ IIE, CAS & Yingcai, UESTC
# Finish on 2015-10-04
#
# Usage:
#    python downloadImage.py beginIndex stopIndex
# So you can download in multi-process.
#
# Note: few images were deleted from the website, please use checkWholeness.py to check
#    missed images and manually delete their items from AVA.txt

import time
import os
import urllib
import sys
from HTMLParser import HTMLParser

##
# Heritate from HTMLParser to parse main image's url
#
class dpchallengeImageParser(HTMLParser):
    def __init__(self):
	HTMLParser.__init__(self)
	self.name = None

    # fetch url and loop out when both image's width and height exceed 200 pix.
    def handle_starttag(self, tag, attrs):
	if self.name is not None:
	    return
	if tag == 'img':
            tmpWidth = 0
	    tmpHeight = 0
	    for key,value in attrs:
		if key == 'src':
		    tmpName = value
		    tmpWidth = 0
		    tmpHeight = 0
		elif key == 'width':
		    tmpWidth = float(value)
		elif key == 'height':
		    tmpHeight = float(value)
		
		# extract main (big) image only
		if (tmpWidth > 150) and (tmpHeight > 150):
		    self.name = tmpName
		    break

savePath = r'../image'
URLprefix = r'http://www.dpchallenge.com/image.php?IMAGE_ID='
AVAtxt = r'../AVA.txt'

# arg check
if len(sys.argv) < 3:
    print 'arg failer! # python downloadImage.py beginIndex stopIndex'
    exit()

# must >= 1
beginIndex = int(sys.argv[1])
# must >= 255530
stopIndex = int(sys.argv[2])

f = open(AVAtxt)
for line in f:
    line = line.strip().split(' ')
    imageIndex = line[0]

    # use begin and stop index constrain 
    if int(imageIndex) < beginIndex:
	continue
    elif int(imageIndex) >= stopIndex:
	break

    # skip exiting images
    if os.path.isfile(os.path.join(savePath, imageIndex + '.jpg')) == True:
	continue;

    # get display webpage url
    imageID = line[1]
    URL = URLprefix + imageID

    # url request and write image
    tic = time.time()
    # get 'dpchallenge' display page
    urlopen=urllib.URLopener() 
    fp = urlopen.open(URL) 
    data = fp.read()
    fp.close()
    # parse out image url in 'self.name'
    urlParser = dpchallengeImageParser()
    # ignore illegal characters (almost impossible appear in image's url)
    data = data.decode('ascii', 'ignore')
    urlParser.feed(data)

    # some main images are even smaller than advertisements
    #    or have been deleted from website
    #    they need manual downloading
    if urlParser.name is None:
	continue
    
    # get iamge
    fimg = urlopen.open(urlParser.name)
    data = fimg.read()
    fimg.close()
    # write image
    fout = open(os.path.join(savePath, imageIndex + '.jpg'), 'w+b')
    fout.write(data)
    fout.close()
    toc = time.time()

    # display progress
    print 'Processing image: {}\ttime elapse: {}\tstop at: {}'.format(int(imageIndex), toc - tic, stopIndex)

