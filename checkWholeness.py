#
# While downloading AVA images, you may need to check the un-downloaded images. This sript will
#    display information of missing images in console.
#
# Author: Wei Zhen @ IIE, CAS & Yingcai, UESTC
# Finish on 2015-10-04
#
# Note: This script should be placed under AVA_dataset/script/ and images are saved at
#    AVA_dataset/image/ folder.

import os
import sys

savePath = r'../image'
AVAtxt = r'../AVA.txt'

# arg check
if len(sys.argv) < 3:
    print 'arg failer! # python checkWholeness.py beginIndex stopIndex'
    exit()

# must >= 1
beginIndex = int(sys.argv[1])
# must >= 255530
stopIndex = int(sys.argv[2])

f = open(AVAtxt)
for line in f:
    line = line.strip().split(' ')
    imageIndex = line[0]
    imageID = line[1]

    # use begin and stop index constrain 
    if int(imageIndex) < beginIndex:
	continue
    elif int(imageIndex) >= stopIndex:
	break

    # if the image does not exist, display its 'index ID' pair
    if os.path.isfile(os.path.join(savePath, imageIndex + '.jpg')) == False:
	print imageIndex, imageID
