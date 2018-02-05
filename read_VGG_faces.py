from scipy import misc
import numpy as np
from skimage import io
import time
import os
import socket
from urllib2 import urlopen
global f
def main():
  socket.setdefaulttimeout(60)
  prefix = '/Users/debraji/Downloads/vgg_face_dataset/'
  datasetDescriptor = prefix+'files'
  textFileNames = sorted(os.listdir(datasetDescriptor))
  person = 0
 
  for textFileName in textFileNames:
    if textFileName.endswith('.txt'):
      person += 1
      with open(os.path.join(datasetDescriptor, textFileName), 'rt') as f:
        lines = f.readlines()
      lastLine = int(lines[-1].split(' ')[0])
      print lastLine
      dirName = textFileName.split('.txt')[0]
      classPath = os.path.join(datasetDescriptor, dirName)
      if not os.path.exists(classPath):
        os.makedirs(classPath)
        lastfile = 0
      else:
        files = sorted(os.listdir(classPath))
        lastfile = int(files[-1].split('.png')[0])
 
        if lastLine == lastfile:
          print person, dirName, lastfile, "Done!"
          continue
 
      for line in lines:
        x = line.split(' ')
        fileName = x[0]
        url = x[1]
        errorLine = ''
 
        if lastfile < int(fileName):
          box = np.rint(np.array(map(float, x[2:6])))
          imagePath = os.path.join(datasetDescriptor, dirName, fileName+'.png')
 
          if not os.path.exists(imagePath):
            try:
              img = io.imread(urlopen(url,timeout = 40))
            except Exception as e:
              errorMessage = '{}: {}'.format(url, e)
              errorLine = line
            else:
              try:
                if img.ndim == 2:
                  img = toRgb(img)
                if img.ndim != 3:
                  raise Exception('Wrong number of image dimensions')
                hist = np.histogram(img, 255, density=True)
                if hist[0][0] > 0.9 and hist[0][254] > 0.9:
                  raise Exception('Image is mainly black or white')
                else:
                  errorMessage = 'ok!'
                  imgCropped = img[int(box[1]):int(box[3]),int(box[0]):int(box[2]),:]
                  imgResized = misc.imresize(imgCropped, (256,256))
                  misc.imsave(imagePath, imgResized)
              except Exception as e:
                errorMessage = '{}: {}'.format(url, e)
                errorLine = line
            print person,dirName,fileName,errorMessage
        with open(prefix+"fix/"+dirName+".txt","a") as fix:
          if line != errorLine:
            fix.write(line)
      print dirName + " Done!"
 
 
def toRgb(img):
  w, h = img.shape
  ret = np.empty((w, h, 3), dtype=np.uint8)
  ret[:, :, 0] = ret[:, :, 1] = ret[:, :, 2] = img
  return ret
 
if __name__ == '__main__':
  main()
