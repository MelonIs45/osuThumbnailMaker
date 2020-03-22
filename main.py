from __future__ import print_function
import PIL, json, os, glob, re, binascii, struct
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import numpy as np
import math
import scipy
import scipy.misc
import scipy.cluster

user = os.getlogin()

osuDir = os.path.join('C:/Users', user,'AppData/Local/osu!/Songs')
fileExts = ('png', 'jpg')
trueRanks = ('XH', 'X', 'SH', 'S', 'A', 'B', 'C', 'D', 'F')
imgSize = (1280, 720)

#question booleans
idQuestion = None
oneMap = None
rankQuestion = None
colourGrabbing = None

while idQuestion is None:
    try:
        songId = int(input("Enter the beatmap id of the song you wish to be made a thumbnail for: "))
        idQuestion = True
    except:
        print("You didn't enter a correct value.")

#gets the path to the image in the beatmap folder
for songDir in glob.glob(osuDir + '/*'):
    if str(songId) in songDir:
        while oneMap is None:
            #print(songDir)
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
    playRank = input("Enter the rank of the play (XH, X, SH, S, A, B, C, D, F): ")
    if playRank in trueRanks:
        rankQuestion = True
    else:
        print("You entered an incorrect rank.")
        
#extra details for thumbnail
userName = input("Enter the user that for that play: ")
modsUsed = input("Enter string of mods used (HDDT, HDHR, etc.): ")
ppCount = int(input("Enter the pp from that play: "))
accCount = float(input("Enter the play accuracy: "))
starCount = float(input("Enter the play star count: "))

bg = Image.open(bgDirFull)
bg = bg.filter(ImageFilter.GaussianBlur(15))
bg = bg.resize(imgSize)
bg.show()


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
draw.ellipse(((x/2-285), (y/2-295), (x/2-165), (y/2-175)), fill=("#ffffff"))
draw.rectangle(((x/2-230), (y/2-295), (x/2+230), (y/2-175)), fill=("#ffffff"))
draw.ellipse(((x/2+165), (y/2-295), (x/2+285), (y/2-175)), fill=("#ffffff"))

draw.ellipse(((x/2-285), (y/2-60), (x/2-165), (y/2+60)), fill=("#ffffff"))
draw.rectangle(((x/2-230), (y/2-60), (x/2+230), (y/2+60)), fill=("#ffffff"))
draw.ellipse(((x/2+165), (y/2-60), (x/2+285), (y/2+60)), fill=("#ffffff"))

draw.ellipse(((x/2-285), (y/2+175), (x/2-165), (y/2+295)), fill=("#ffffff"))
draw.rectangle(((x/2-230), (y/2+175), (x/2+230), (y/2+295)), fill=("#ffffff"))
draw.ellipse(((x/2+165), (y/2+175), (x/2+285), (y/2+295)), fill=("#ffffff"))

textBlocks = textBlocks.filter(ImageFilter.GaussianBlur(8))
textBlocks.show()
smallBlocks = Image.new(mode="RGBA", size=(1280, 720))
x, y = smallBlocks.size
draw = ImageDraw.Draw(smallBlocks)

draw.ellipse(((x/2-275), (y/2-285), (x/2-175), (y/2-185)), fill=("#ffffff"))
draw.rectangle(((x/2-225), (y/2-285), (x/2+225), (y/2-185)), fill=("#ffffff"))
draw.ellipse(((x/2+175), (y/2-285), (x/2+275), (y/2-185)), fill=("#ffffff"))

draw.ellipse(((x/2-275), (y/2-50), (x/2-175), (y/2+50)), fill=("#ffffff"))
draw.rectangle(((x/2-225), (y/2-50), (x/2+225), (y/2+50)), fill=("#ffffff"))
draw.ellipse(((x/2+175), (y/2-50), (x/2+275), (y/2+50)), fill=("#ffffff"))

draw.ellipse(((x/2-275), (y/2+185), (x/2-175), (y/2+285)), fill=("#ffffff"))
draw.rectangle(((x/2-225), (y/2+185), (x/2+225), (y/2+285)), fill=("#ffffff"))
draw.ellipse(((x/2+175), (y/2+185), (x/2+275), (y/2+285)), fill=("#ffffff"))
smallBlocks.show()

textBlocks.show()
textBlocks.convert('RGBA')
bg.paste(textBlocks, (0, 0), textBlocks)
bg.show()



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

gradient.show()
finalImage = Image.new("RGB", imgSize)

#composites all the images so it creates a finished product, not finished yet
finalImage = Image.composite(gradient, bg, smallBlocks)
finalImage.show()

vagRound = ImageFont.truetype("vag-rounded.ttf", 16)

textDraw = ImageDraw.Draw(finalImage, "RGBA")
textDraw.text((12, 70), str(userName), vagRound, stroke_width=2)

finalImage.show()

input()