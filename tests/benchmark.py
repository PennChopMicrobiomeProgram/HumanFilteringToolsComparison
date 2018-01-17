import json
from subprocess import call
import sys, os

#define abs path
path = os.path.abspath(os.path.dirname(sys.argv[0]))
data_path = path + "/data"

# create directories for summary files and output files if they don't exist
log_path = data_path + "/log"
if not os.path.exists(log_path):
    os.mkdir(log_path)

output_path = data_path + "/output"
if not os.path.exists(output_path):
    os.mkdir(output_path)

# for pct between 0.0 and 1.0
for p in map(lambda x: x/10.0,range(0,11)):
    #for frac between 0.0 and 1.0
    for f in map(lambda x: x/10.0,range(0,11)):
        # print pct and frac
        print("pct: " + str(p) + " frac: " + str(f))
        # name summary files
        hum_sum_file = "{}/humanseqs_{}_{}.json".format(log_path, p, f)
        nonhum_sum_file = "{}/nonhumanseqs_{}_{}.json".format(log_path, p, f)
        # run decontam over human seqs
        call(["decontaminate.py", "--forward-reads", data_path + "/humanseqs.fastq", "--organism", "human", "--pct", str(p), "--frac", str(f), "--output-dir", output_path, "--summary-file", hum_sum_file])
        # run decontam over nonhuman seqs
        call(["decontaminate.py", "--forward-reads", data_path + "/nonhumanseqs.fastq", "--organism", "human", "--pct", str(p), "--frac", str(f), "--output-dir", output_path, "--summary-file", nonhum_sum_file])
        # from human seqs summary file, read and print number of true positive ("true" in data) and false negatives ("false" in data)  
        # from nonhuman seqs summary file, read and print number of false positives ("true" in data) and true negatives ("false" in data)
        message = ["tru", "fal", "tru"]
        for i, file in enumerate([hum_sum_file, nonhum_sum_file]):
            with open(file) as f:
                data = json.loads(f.read())["data"]
                mess = "{} pos: ".format(message[i])
                if "true" in data:
                    print("{}{}".format(mess, data["true"]))
                else:
                    print("{}0".format(mess))    
                mess = "{} neg: ".format(message[i+1])
                if "false" in data:
                    print("{}{}".format(mess, data["false"]))
                else:
                    print("{}0".format(mess))
