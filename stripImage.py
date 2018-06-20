'''
This script uses Pillow to create a new version of images
with their metadata stripped, which not only helps with
security but also may significantly reduce their size. 
Either a single image can be provided on the command line
or a directory of images with a -d flag. Stripped images
get placed in a directory called Exif_Stripped.
'''
from os import path, listdir, makedirs
from sys import argv
from PIL import Image
from pathlib import Path


def verifyAndOpenImage(imageName=''):
    '''
    Attempts to open and return a file and returns None if unsuccessful.
    '''
    try:
        img = Image.open(imageName)
        return img
    except IOError:
        return None


def stripImage(imageName=''):
    '''
    Attempts to strip a file and returns None if unsuccessful.
    '''
    directory, fileName = path.split(imageName)
    
    img = verifyAndOpenImage(imageName)
    if img == None:
        return None

    data = img.getdata()

    strippedImage = Image.new(img.mode, img.size)
    strippedImage.putdata(data)

    p = Path(directory)
    p = p / 'Exif_Stripped' / ('Exif_Stripped_' + fileName)
    print(str(p))
    strippedImage.save(str(p))

    return strippedImage


def processArgs():
    '''
    Currently only checks for -d flag and the source.
    There may be more added in the future.
    '''
    args = {
        'isDirectory': False,
        'source': ''
    }
    
    for arg in argv:
        if arg == '-d':
            args['isDirectory'] = True

    args['source'] = argv[len(argv) - 1]

    return args


if __name__ == '__main__':
    args = processArgs()
    makedirs('Exif_Stripped', 0o777, True) #Wont crash if directory already exists

    if args['isDirectory'] == True:
        files = listdir(args['source'])
        for f in files:
            if path.isfile(f):
                stripImage(f)
    else:
        stripImage(args['source'])   
