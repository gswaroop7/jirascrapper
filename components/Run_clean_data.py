from clean_data import CleanData

o = CleanData()

import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# the file to be converted to
# json format
filename = os.path.join(ROOT_DIR, '<filename.txt>')
file = open(filename, 'r')
Lines = file.readlines()

output =  os.path.join(ROOT_DIR, '<output.txt>')
write_file = open(output, 'a')

for line in Lines:
    data_list = line.split(',')
    data_list[1] = o.remove_stop_words(data_list[1])  # summary of the ticket
    data_list[2] = o.remove_stop_words(data_list[2])  # Description of the ticket
    data_list[3] = o.remove_stop_words(data_list[3])  # Solution of the ticket

    try:
        write_file.write(','.join(data_list))
        write_file.write("\n")
    except Exception as e:
        print (f"Failed with Error {e}")
