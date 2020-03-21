import PIL, json, os, glob, re

user = os.getlogin()
osuDir = os.path.join('C:\\Users', user,'AppData/Local/osu!/Songs')
fileExt = ['png', 'jpg']

songString = input("Enter the beatmap id of the song you wish to be made a thumbnail for: ")
#songString = "402887"

for songDir in glob.glob(osuDir + '/*'):
    if songString in songDir:
        print(songDir)
        print(os.listdir(songDir))
    else:
        pass



input()