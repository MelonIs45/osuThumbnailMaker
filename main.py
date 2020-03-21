import PIL, json, os, glob, re
from PIL import Image
user = os.getlogin()
osuDir = os.path.join('C:\\Users', user,'AppData/Local/osu!/Songs')
fileExt = ('png', 'jpg')

songString = input("Enter the beatmap id of the song you wish to be made a thumbnail for: ")

for songDir in glob.glob(osuDir + '/*'):
    if songString in songDir:
        print(songDir)
        songDirFiles = os.listdir(songDir)
        print(songDirFiles)
        for i in range(len(songDirFiles)):
            if songDirFiles[i - 1].endswith(fileExt):
                bgDir = songDirFiles[i - 1]
                bgDirFull = os.path.join(songDir, bgDir)
            else:
                pass
    else:
        pass

bg = Image.open(bgDirFull)
bg.show()
input()