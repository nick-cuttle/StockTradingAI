import os
import sys

#Get all 50,000 label files..... -> []

out_file = open(sys.argv[1], 'w')


test_label_path = "./test_labels/"

label_filenames = os.listdir(test_label_path) # ["file1.txt", "file2.txt"]

for label_filename in label_filenames:
    label_file = open(test_label_path + label_filename, 'r')
    fname = label_file.name.replace("./test_labels/", "")
    new_line = fname + " "
    for line in label_file:
        line = line.strip()
        if len(line) == 0:
            continue
        split_line = line.split(" ")
        label_str = split_line[0] + split_line[1]
        new_line += label_str + " "
    label_file.close()
    out_file.write(new_line + "\n")

out_file.close()






#split(" ")
#filename.txt DIRECTION:DOWN SYMBOL:IBM
#[filename.txt, DIRECTION:DOWN, SYMBOL:IBM]
#               # split(":")
    #["DIRECTION", "DOWN"]
#