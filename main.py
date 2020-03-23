from __future__ import print_function
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import numpy as np
import math
import scipy
import scipy.misc
import scipy.cluster
import os
import glob
import re
import binascii
import struct

user = os.getlogin()

osuDir = os.path.join('C:/Users', user,'AppData/Local/osu!/Songs')
fileExts = ('png', 'jpg')
trueRanks = ('XH', 'X', 'SH', 'S', 'A', 'B', 'C', 'D')
imgSize = (1280, 720)
fontSizeUserName = 32
fontSizeTitle = 21
fontSizeStats = 24
blockOutline = 10

#question booleans
idQuestion = None
oneMap = None
rankQuestion = None
colourGrabbing = None

#uses the id to search for the song background
while idQuestion is None:
    try:
        songId = int(input("Enter the beatmap id of the song you wish to be made a thumbnail for: "))
        idQuestion = True
    except ValueError:
        print("You didn't enter a correct value.")

#gets the path to the image in the beatmap folder
for songDir in glob.glob(osuDir + '/*'):
    if str(songId) in songDir:
        while oneMap is None:
            titleDir = songDir
            songDirFiles = os.listdir(songDir)
            #print(songDirFiles)
            oneMap = True
            for i in range(len(songDirFiles)):
                if songDirFiles[i - 1].endswith(fileExts):
                    bgName = songDirFiles[i - 1]
                    bgDirFull = os.path.join(songDir, bgName)
                else:
                    pass
    else:
        pass

#asks for rank of play
while rankQuestion is None:
    playRank = input("Enter the rank of the play (XH, X, SH, S, A, B, C, D): ")
    if playRank in trueRanks:
        rankQuestion = True
    else:
        print("You entered an incorrect rank.")
        
#extra details for thumbnail
userName = input("Enter the user that for that play: ")
mapDiff = input("Enter the difficulty name of the map: ")
modsUsed = input("Enter string of mods used (HDDT, HDHR, etc.): ")
ppCount = int(input("Enter the pp from that play: "))
accCount = float(input("Enter the play accuracy: "))
starCount = float(input("Enter the play star count: "))

#creates strings
userNameLength = (len(userName)) * fontSizeUserName
userNameOffset = userNameLength/2
userNameBlockOffset = userNameOffset + 50

splitDir = titleDir.split(" ")
splitDir.pop(0)
fileName = " ".join(splitDir)
finalTitle = " ".join(splitDir)
finalTitle = finalTitle + ((" [{0}] + {1}").format(mapDiff, modsUsed))
print(finalTitle)

titleLength = (len(finalTitle)) * fontSizeTitle
titleOffset = titleLength/2
titleBlockOffset = titleOffset + 50

stats = "{0}pp | {1}% | {2}*".format(ppCount, accCount, starCount)
statsLength = (len(stats)) * fontSizeStats
statsOffset = statsLength/2
statsBlockOffset = statsOffset + 50

print(userNameLength, titleLength, stats)

bg = Image.open(bgDirFull)
bg = bg.filter(ImageFilter.GaussianBlur(15))
bg = bg.resize(imgSize)
#bg.show()


#finds the most common colours in the image by splitting them up into sectors
clusterCount1 = 1
clusterCount2 = 3

image = Image.open(bgDirFull)
image = image.resize((150, 150))
ar = np.asarray(image)
shape = ar.shape
ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

codes, dist = scipy.cluster.vq.kmeans(ar, clusterCount1)
codes2, dist2 = scipy.cluster.vq.kmeans(ar, clusterCount2)
vecs, dist = scipy.cluster.vq.vq(ar, codes) 
vecs2, dist2 = scipy.cluster.vq.vq(ar, codes2) 
counts, bins = scipy.histogram(vecs, len(codes))    
counts2, bins2 = scipy.histogram(vecs2, len(codes2)) 
index_max = scipy.argmax(counts) 
index_max2 = scipy.argmax(counts2)
peak1 = codes[index_max]
peak2 = codes2[index_max2]
colour1 = binascii.hexlify(bytearray(int(c) for c in peak1)).decode('ascii')
colour2 = binascii.hexlify(bytearray(int(c) for c in peak2)).decode('ascii')

#adds hashtag to hex values
colour1, colour2 = ("#"+ colour1), ("#"+ colour2)

#creates mask for later composition
textBlocks = Image.new(mode="RGBA", size=(1280, 720))
x, y = textBlocks.size
draw = ImageDraw.Draw(textBlocks)

#draws the blocks to where the text will be on

#1st 3 blocks are the glowy/blurred backgrounds, NOTE: had to use 3 shapes to create a curved square
draw.ellipse(((x/2-userNameBlockOffset-blockOutline), (y/2-300), (x/2-userNameBlockOffset+120), (y/2-170)), fill=("#ffffff"))
draw.rectangle(((x/2-userNameBlockOffset-(blockOutline/2)+75), (y/2-300), (x/2+userNameBlockOffset-(blockOutline/2)-60), (y/2-170)), fill=("#ffffff"))
draw.ellipse(((x/2+userNameBlockOffset-(blockOutline)-100), (y/2-300), (x/2+userNameBlockOffset-(blockOutline)+20), (y/2-170)), fill=("#ffffff"))

draw.ellipse(((x/2-titleBlockOffset-blockOutline), (y/2-65), (x/2-titleBlockOffset+120), (y/2+65)), fill=("#ffffff"))
draw.rectangle(((x/2-titleBlockOffset-(blockOutline/2)+75), (y/2-65), (x/2+titleBlockOffset-(blockOutline/2)-60), (y/2+65)), fill=("#ffffff"))
draw.ellipse(((x/2+titleBlockOffset-(blockOutline)-100), (y/2-65), (x/2+titleBlockOffset-(blockOutline)+20), (y/2+65)), fill=("#ffffff"))

draw.ellipse(((x/2-statsBlockOffset-blockOutline), (y/2+170), (x/2-statsBlockOffset+120), (y/2+300)), fill=("#ffffff"))
draw.rectangle(((x/2-statsBlockOffset-(blockOutline/2)+75), (y/2+170), (x/2+statsBlockOffset-(blockOutline/2)-60), (y/2+300)), fill=("#ffffff"))
draw.ellipse(((x/2+statsBlockOffset-(blockOutline)-100), (y/2+170), (x/2+statsBlockOffset-(blockOutline)+20), (y/2+300)), fill=("#ffffff"))

textBlocks = textBlocks.filter(ImageFilter.GaussianBlur(8))
#textBlocks.show()
smallBlocks = Image.new(mode="RGBA", size=(1280, 720))
x, y = smallBlocks.size
draw = ImageDraw.Draw(smallBlocks)

#these 3 blocks are the main coloured backgrounds
draw.ellipse(((x/2-userNameBlockOffset+blockOutline), (y/2-285), (x/2-userNameBlockOffset+120), (y/2-185)), fill=("#ffffff"))
draw.rectangle(((x/2-userNameBlockOffset+75), (y/2-285), (x/2+userNameBlockOffset-60), (y/2-185)), fill=("#ffffff"))
draw.ellipse(((x/2+userNameBlockOffset-120), (y/2-285), (x/2+userNameBlockOffset-blockOutline), (y/2-185)), fill=("#ffffff"))

draw.ellipse(((x/2-titleBlockOffset+blockOutline), (y/2-50), (x/2-titleBlockOffset+120), (y/2+50)), fill=("#ffffff"))
draw.rectangle(((x/2-titleBlockOffset+75), (y/2-50), (x/2+titleBlockOffset-60), (y/2+50)), fill=("#ffffff"))
draw.ellipse(((x/2+titleBlockOffset-120), (y/2-50), (x/2+titleBlockOffset-blockOutline), (y/2+50)), fill=("#ffffff"))

draw.ellipse(((x/2-statsBlockOffset+blockOutline), (y/2+185), (x/2-statsBlockOffset+120), (y/2+285)), fill=("#ffffff"))
draw.rectangle(((x/2-statsBlockOffset+75), (y/2+185), (x/2+statsBlockOffset-60), (y/2+285)), fill=("#ffffff"))
draw.ellipse(((x/2+statsBlockOffset-120), (y/2+185), (x/2+statsBlockOffset-blockOutline), (y/2+285)), fill=("#ffffff"))
#smallBlocks.show()

#textBlocks.show()
textBlocks.convert('RGBA')
bg.paste(textBlocks, (0, 0), textBlocks)
#bg.show()

gradient = Image.new('RGB', imgSize) 

innerColor = peak1 #color at the center
outerColor = peak2 #color at the corners

#creates a gradient with the average bg colour
for y in range(imgSize[1]):
    for x in range(imgSize[0]):
        #distance to the center
        distanceToCenter = math.sqrt((x - imgSize[0]/2) ** 2 + (y - imgSize[1]/2) ** 2)

        #convert to scale between 0 and 1
        distanceToCenter = float(distanceToCenter) / (math.sqrt(2) * imgSize[0]/2)

        #calculates rgb values
        r = outerColor[0] * distanceToCenter + innerColor[0] * (1 - distanceToCenter)
        g = outerColor[1] * distanceToCenter + innerColor[1] * (1 - distanceToCenter)
        b = outerColor[2] * distanceToCenter + innerColor[2] * (1 - distanceToCenter)

        #place the pixel        
        gradient.putpixel((x, y), (int(r), int(g), int(b)))

#gradient.show()
finalImage = Image.new("RGB", imgSize)

#composites all the images so it creates a finished product, not finished yet
finalImage = Image.composite(gradient, bg, smallBlocks)
#finalImage.show()

#different font sizes for different blocks to stop unneccesary text/block overflow
vagRoundUserName = ImageFont.truetype("vag-rounded.ttf", 60)
vagRoundTitle = ImageFont.truetype("vag-rounded.ttf", 45)
vagRoundStats = ImageFont.truetype("vag-rounded.ttf", 55)

if userNameLength < 100:
    extraOffset = -6
else:
    extraOffset = 5

#places text to image
textDraw = ImageDraw.Draw(finalImage)
textDraw.text(((x/2 - userNameOffset + extraOffset), 85), userName, fill="#000000", font=vagRoundUserName, stroke_width=2, stroke_fill="#ffffff")
textDraw.text(((x/2 - titleOffset + extraOffset), 330), finalTitle, fill="#000000", font=vagRoundTitle, stroke_width=2, stroke_fill="#ffffff")
textDraw.text(((x/2 - statsOffset + extraOffset), 560), stats, fill="#000000", font=vagRoundStats, stroke_width=2, stroke_fill="#ffffff")

#adds rank to image
rankImage = Image.open("ranks/{}.png".format(playRank))
finalImage.paste(rankImage, (25, 25), rankImage)

finalImage.show()

finalImage.save("thumbnails/"+fileName+".png")
end = input("Done!")
