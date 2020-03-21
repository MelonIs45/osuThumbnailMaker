import PIL, json, os, glob, re
from PIL import Image
user = os.getlogin()
osuDir = os.path.join('C:/Users', user,'AppData/Local/osu!/Songs')
fileExts = ('png', 'jpg')
trueRanks = ('XH', 'X', 'SH', 'S', 'A', 'B', 'C', 'D', 'F')

#question booleans
idQuestion = False
oneMap = False
rankQuestion = False

while idQuestion == False:
    try:
        songId = int(input("Enter the beatmap id of the song you wish to be made a thumbnail for: "))
        idQuestion = True
    except:
        print("You didn't enter a correct value.")


#gets the path to the image in the beatmap folder
for songDir in glob.glob(osuDir + '/*'):
    if str(songId) in songDir:
        while oneMap == False:
            print(songDir)
            songDirFiles = os.listdir(songDir)
            print(songDirFiles)
            oneMap = True
            for i in range(len(songDirFiles)):
                if songDirFiles[i - 1].endswith(fileExts):
                    bgName = songDirFiles[i - 1]
                    bgDirFull = os.path.join(songDir, bgName)
                else:
                    pass
    else:
        pass

while rankQuestion == False:
    playRank = input("Enter the rank of the play (XH, X, SH, S, A, B, C, D, F): ")
    if playRank in trueRanks:
        rankQuestion = True
    else:
        print("You entered an incorrect rank.")
        
userName = input("Enter the user that for that play: ")
modsUsed = input("Enter string of mods used (HDDT, HDHR, etc.): ")
ppCount = int(input("Enter the pp from that play: "))
accCount = float(input("Enter the play accuracy: "))
starCount = float(input("Enter the play star count: "))

bg = Image.open(bgDirFull)
bg.show()
input()