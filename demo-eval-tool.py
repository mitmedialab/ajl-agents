import operator
import os
import urllib

from clarifai.rest import Image as ClImage
from clarifai.rest import ClarifaiApp

app = ClarifaiApp("5Jw6Ivz58UgkcahDmrLH1jwYYV1XbFu7_l5fe9gO",
                  "5GP2z4eLRz4ahYkuNsxQk97nOdJXHxX2FKN7sf2T")


def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
  '''From:
    http://code.activestate.com/recipes/473878-timeout-function-using-threading/'''
  import threading

  class InterruptableThread(threading.Thread):

    def __init__(self):
      threading.Thread.__init__(self)
      self.result = None

    def run(self):
      try:
        self.result = func(*args, **kwargs)
      except:
        self.result = default

  it = InterruptableThread()
  it.start()
  it.join(timeout_duration)
  if it.isAlive():
    return False
  else:
    return it.result


testfile = urllib.URLopener()


def formatter(act):
  '''
	act -- a list of actor and actress names

	NOTE: you need to make an uncropped folder in local directory first in order for this to work
	'''
  filenames = []
  act_dict = {}
  for a in act:
    name = a.lower()
    i = 0
    links = []
    for line in open("facescrub_actors.txt"):
      if i < 10:
        if a in line:
          #will download file and give you the name of the file
          filename = name + str(i) + '.' + line.split()[4].split('.')[-1]
          timeout(testfile.retrieve, (line.split()[4], "uncropped/" + filename), {}, 30)
          if not os.path.isfile("uncropped/" + filename):
            continue
          links.append(line.split()[4])
          filenames.append(filename)
          i += 1

    for line in open("facescrub_actresses.txt"):
      if i < 10:
        if a in line:
          #will download file and give you the name of the file
          filename = name + str(i) + '.' + line.split()[4].split('.')[-1]
          timeout(testfile.retrieve, (line.split()[4], "uncropped/" + filename), {}, 30)
          if not os.path.isfile("uncropped/" + filename):
            continue
          links.append(line.split()[4])
          filenames.append(filename)
          i += 1

    act_dict[a] = links

  return act_dict, filenames


def demo_predict(filename):
  '''
	argument could be one of the following options:

	filename -- a filename of the folder on the local computer for each image, in my case, in an uncropped folder on my desktop ( safer option since you know images will download)
	link -- a url link to the image ( a bit less safe, as some URLs are currupt and will result in a bad request to API call)


	'''
  prediction = []
  #uncomment for link input option
  #image = ClImage(url=link)
  #file input option, personlized for my unique filepath - change '/Users/debraji/Desktop/uncropped' to be whatever the path to the folder in which your images are saved
  image = ClImage(file_obj=open('/Users/debraji/Desktop/uncropped/' + filename, 'rb'))

  #NOTE: this code is only useful if you have ONE face per image - to get all the faces, iterate through the total number of outputs (TO DO)
  model = app.models.get('demographics')
  labels = model.predict([image])[u"outputs"][0][u'data'][u'regions'][0]
  labels[u'region_info'][u'bounding_box']
  age_guesses = labels[u'data'][u'face'][u'age_appearance'][u'concepts']
  ages = {}

  for num in age_guesses:
    age = str.strip(str(num[u'name']))
    value = str.strip(str(num[u'value']))
    ages[age] = value

  print(ages)  #ages is a dict of age predictions and thier probabilties
  #return age with max probability
  prediction.append(max(ages.iterkeys(), key=lambda k: ages[k]))

  gender_guesses = labels[u'data'][u'face'][u'gender_appearance'][u'concepts']
  genders = {}

  for gen in gender_guesses:
    gender = str.strip(str(gen[u'name']))
    value = str.strip(str(gen[u'value']))
    genders[gender] = value

  print(genders)  #genders is a dict of gender predictions and thier probabilties
  prediction.append(max(genders.iterkeys(), key=lambda k: genders[k]))

  race_guesses = labels[u'data'][u'face'][u'multicultural_appearance'][u'concepts']
  races = {}

  for r in race_guesses:
    race = str.strip(str(r[u'name']))
    value = str.strip(str(r[u'value']))
    races[race] = value

  print(races)
  prediction.append(max(races.iterkeys(), key=lambda k: races[k]))
  return prediction


#TESTING
'''
Using a subset of the Facescrub dataset, which uses celebrity images in order to generate large, clean sets of data used in many open source face recognition projects. Images were retrieved from the Internet and are taken under real-world situations (uncontrolled). name and gender annotations are present. 

Although there seems to be a deliberate 50/50 gender appearance split, an issue with Facescrub is the lack of ethnic diversity in the dataset, which is highlighted in the results below. The lack of diversity in the subjects of the dataset can then becaome a source of introducing bias into several open source projects, reducing program performance for users of underrepresented multicultural appearance.  

To learn more about the dataset, and access the whole thing, you can look here : http://vintage.winklerbros.net/facescrub.html

Fill out this form to get download instructions :  http://form.jotform.me/form/43268445913460.    
Released under the creative commons liscence. 

'''

people = []
for line in open("facescrub_actors.txt"):
  l = line.split()
  if (len(l) == 7) and (l[1] not in people):
    name = l[1]
    people.append(name)

for line in open("facescrub_actresses.txt"):
  l = line.split()
  if (len(l) == 7) and (l[1] not in people):
    name = l[1]
    people.append(name)

#using filenames of images saved on local computer

act_dict, filenames = formatter(people)

results = []
for file in filenames:
  try:
    #print(demo_predict(file))
    results += demo_predict(file)
  except:
    pass

set_res = sorted(set(results))
tot_items = len(results) / 3
output = {}

for item in set_res:
  num = results.count(item)
  output[item] = 100 * (float(num) / tot_items)

out = list(reversed(sorted(output.items(), key=operator.itemgetter(1))))

print(out)
