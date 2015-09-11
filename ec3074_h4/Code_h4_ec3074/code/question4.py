from subprocess import PIPE
import sys, subprocess
from collections import defaultdict

v = defaultdict(float)

#read the initial weights from tag.model into 'v'
def initializeWeights(tag_model):
  for line in open(tag_model):
    words = line.strip().split(" ")
    value = words[1]
    index = words[0].strip().split(":")
    v[(index[1], index[2])] = float(value)

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
      
fp = open("output/tag_dev.out", "w")


#based on feature weights get the decoder history and write the decoding result into " tag_dev.out"
def ComputeFeatures(enum_histories, sentence):
  hist=""
  history_list = enum_histories.split("\n")
  word_list = sentence.split("\n")

  for item in history_list:
    elements = item.strip().split()

    if(len(elements) == 3):  
      weight1 = float(v[(elements[1], elements[2])]) #compute weight for each history
      weight2 = float(v[(word_list[int(elements[0])-1], elements[2])]) #compute weight for each history
      weight = weight1 + weight2
      hist=hist+item+" "+str(weight)+"\n"

  decoder_histories = call(decoder_server, hist.strip())

  decoder_list = decoder_histories.split("\n")
  sentence_list = sentence.split("\n")
  for item_d, item_s in zip(decoder_list, sentence_list):
    elements_d = item_d.strip().split()
    elements_s = item_s.strip().split()
    if len(elements_s):
      fp.write(("%s %s\n")%(elements_s[0], elements_d[2]))
  fp.write("\n")

if __name__ == '__main__':
  initializeWeights("tag.model")
  getHistory("tag_dev.dat")

  

