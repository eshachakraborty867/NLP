from subprocess import PIPE
import sys, subprocess
from collections import defaultdict

v = defaultdict(float)

def initializeWeights(tag_model, suffix_model):
  
  for line in open(tag_model):
    words = line.strip().split(" ")
    value = words[1]
    index = words[0].strip().split(":")
    v[(index[1], index[2])] = float(value)
  for line in open(suffix_model):
    words = line.strip().split(" ")
    value = words[1]
    index = words[0].strip().split(":")
    v[(index[0], index[1])] = float(value)
  


def process(args):
  "Create a 'server' to send commands to."
  return subprocess.Popen(args, stdin=PIPE, stdout=PIPE)

def call(process, stdin):
  "Send command to a server and get stdout."
  output = process.stdin.write(stdin + "\n\n")
  line = ""
  while 1: 
    l = process.stdout.readline()
    if not l.strip(): break
    line += l
  return line

enum_server = process(
  ["python", "tagger_history_generator.py",  "ENUM"])
decoder_server = process(
  ["python", "tagger_decoder.py", "HISTORY"])

def getHistory(dev_file):
  fdev=open(dev_file)
  devlines = fdev.readlines()
  sentence=""
  for line in devlines:
    if line != "\n":
      sentence=sentence+line
    else:
      enum_histories = call(enum_server, sentence.strip())
      ComputeFeatures(enum_histories, sentence)
      sentence=""
      
fp = open("output/tag_dev6_3.out", "w")

def ComputeFeatures(enum_histories, sentence):
  #g=defaultdict(float)
  weight=defaultdict(float)
  hist=""
  history_list = enum_histories.split("\n")
  word_list = sentence.split("\n")

  for item in history_list:
    elements = item.strip().split()

    if(len(elements) == 3):  

      if int(elements[0])-2 < 0:
        tempweight1 = 0
      else:
        tempweight1 = v[(word_list[int(elements[0])-2].strip().split()[0], elements[2])]

      #current tag - current word - next word
      if int(elements[0]) >= len(word_list)-1:
        tempweight2 = 0
      else:
        tempweight2 = v[(word_list[int(elements[0])-1].strip().split()[0], word_list[int(elements[0])].strip().split()[0], elements[2])]

      #current tag - previous two words
      if int(elements[0])-3<0:
        tempweight3=0
      else:
        tempweight3 = v[(word_list[int(elements[0])-3].strip().split()[0], word_list[int(elements[0])-2].strip().split()[0], elements[2])]


      weight1 = float(v[(elements[1], elements[2])])  #compute weight for each history
      weight2 = float(v[(word_list[int(elements[0])-1], elements[2])]) #compute weight for each history

      if len(word_list[int(elements[0])-1]) == 1:
        weight3 = float(v[(word_list[int(elements[0])-1][-1:], elements[2])])

      elif len(word_list[int(elements[0])-1]) == 2:
        weight3 = float(v[(word_list[int(elements[0])-1][-1:], elements[2])]) + float(v[(word_list[int(elements[0])-1][-2:], elements[2])])

      else:
        weight3 = float(v[(word_list[int(elements[0])-1][-1:], elements[2])]) + float(v[(word_list[int(elements[0])-1][-2:], elements[2])]) + float(v[(word_list[int(elements[0])-1][-3:], elements[2])])
      
      weight[(elements[0], elements[1], elements[2])] = weight1 + weight2 + weight3 + tempweight1 +tempweight3 +tempweight2

      hist=hist+item+" "+str(weight[(elements[0], elements[1], elements[2])])+"\n"

  decoder_histories = call(decoder_server, hist.strip())
  #print decoder_histories

  decoder_list = decoder_histories.split("\n")
  sentence_list = sentence.split("\n")
  for item_d, item_s in zip(decoder_list, sentence_list):
    elements_d = item_d.strip().split()
    elements_s = item_s.strip().split()
    if len(elements_s):
      fp.write(("%s %s\n")%(elements_s[0], elements_d[2]))
  fp.write("\n")

if __name__ == '__main__':
  initializeWeights("tag.model", "output/suffix_tagger6_3.model")
  getHistory("tag_dev.dat")

  

