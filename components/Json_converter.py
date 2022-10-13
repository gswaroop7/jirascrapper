# Python program to convert text
# file to JSON

import json
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# the file to be converted to
# json format
filename = os.path.join(ROOT_DIR, '<filenaMe.txt>')

#outputfile to store the json format
output_file = os.path.join(ROOT_DIR, '<outputfile.json>')

# dictionary where the lines from
# text will be stored
sub_data = []
qas = {}
answer = []
final_data=[]

# creating dictionary
with open(filename) as fh:
    for line in fh:
        data = {}
        # reads each line and trims of extra the spaces
        # and gives only the valid words
        sub_data = line.strip().split(',')
        answer = [{ "text":sub_data[3], "answer_start": 0, }]
        qas = { "id":sub_data[0], "is_impossible":False, "question":sub_data[1], "answers":answer}
        data["context"] = sub_data[2]
        data["qas"] = [qas]
        final_data.append(data)

#adding to the file
out_file = open(output_file, "w")
json.dump(final_data, out_file, indent=4, sort_keys=False)
out_file.close()
