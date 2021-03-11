import json
import os.path
import re
from nltk.corpus import stopwords

#import nltk
#nltk.download('stopwords')

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

stop_words = set(stopwords.words('english'))
stop_words.add("min")
stop_words.add("max")

def transform(line, file):
    result = []
    tmp = []
    idx = 1
    line = line.strip("\n")
    line = re.sub(r"\s", "_", line)
    line = line.lower()
    line = line.split("--")

    for part in line:
        if (len(tmp) == 0 or len(tmp) == 1):
            tmp.append(part)
        elif (len(tmp) % 2 == 0):
            if tmp[0] in stop_words:
                tmp[0] = result[-1:][0][0]
                result = result[:-1]
            tmp.append(part)
            result.append(tmp)
            tmp = [part]

    for r in result:
        if len(r) == 3:
            file.write("\t".join(r))
            file.write("\n")
    file.write("\n")
    return result

#################################################### Clean path (remove stop words from path)
my_path = os.path.abspath(os.path.dirname(__file__))

path = os.path.join(my_path, "data\\path")
file = open(path, "r")
relation = file.readlines()
file.close()

#################################################### Transform line and save to clean_path file
cleanpath = os.path.join(my_path, "data\\clean_path")
file = open(cleanpath, "w")
for line in relation:
    rows = transform(line, file)
file.close()

#################################################### Read triple score file (from knowledge graph embedding tuple score)
score_dict = {}
triplescore = os.path.join(my_path, "data\\triple_score")
file = open(triplescore, "r")
while True:
    line = file.readline()
    if not line:
        break
    else:
        line = line.strip()
        lines = line.split("\t")
        score_dict[" ".join(lines[:3])] = float(lines[3])
file.close()

file = open(cleanpath, "r")
final_score = {}
tmp = []
score = 1
while True:
    line = file.readline()
    if not line:
        break
    else:
        line = line.strip()
        if line == "":
            final_score["--".join(tmp)] = score
            score = 1
            tmp = []
        else:
            lines = line.split("\t")
            label = []
            tmp1 = lines[0] + " " + lines[1] + " " + lines[2]

            if tmp1 in score_dict:
                score *= score_dict[tmp1]

            if not tmp == []:
                tmp.extend(lines[1:])
            else:
                tmp = lines
file.close()

scorejson = os.path.join(my_path, "data\\scorejson")
with open(scorejson, 'w') as fp:
    json.dump(final_score, fp)