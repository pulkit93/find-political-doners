#!/usr/bin/python

import os
import argparse
from datetime import datetime

def is_date(string):
    try:
        datetime.strptime(string, '%m%d%Y')
        return True
    except ValueError:
        return False

def clean_input(line):
    fields = line.split('|')
    fields = [fields[i] for i in [0, 10, 13, 14, 15]]
    if fields[0] == '' or fields[3] == '':
        return 0,0
    fields[1] = fields[1][:5]
    if fields[4] != '':
        return 0,0

    by_zip = fields
    by_date = fields
    if len(fields[1]) < 5:  ## or (not fields[1].isdigit()):
        by_zip = 0

    if not is_date(fields[2]):
        by_date = 0

    return by_zip, by_date

## more efficient
# def out_by_zip(line):
#     line[3] = float(line[3])
#     if medianvals_by_zip[(line[0],line[1])]:
#         value = medianvals_by_zip[(line[0], line[1])]
#         value[1] += 1
#         value[2] += line[3]
#         value[0] = int(round(value[2]/value[1]))
#         value[2] = int(round(value[2]))
#     else:
#         line[3] = int(round(line[3]))
#         value = (line[3], 1, line[3])
#     medianvals_by_zip[(line[0], line[1])] = value
def median(lst):
    n = len(lst)
    if n < 1:
            return None
    if n % 2 == 1:
            return sorted(lst)[n//2]
    else:
            return sum(sorted(lst)[n//2-1:n//2+1])/2.0

def out_by_zip(file, line, medianvals_by_zip):
    ##int or float??
    line[3] = int(line[3])
    if (line[0], line[1]) in medianvals_by_zip:
        medianvals_by_zip[(line[0], line[1])].append(line[3])
    else:
        medianvals_by_zip[(line[0], line[1])] = [line[3]]
    vals = medianvals_by_zip[(line[0], line[1])]
    file.write("|".join([line[0],line[1],str(int(round(median(vals)))),str(len(vals)),str(sum(vals))]))
    file.write('\n')

def out_by_date(line, medianvals_by_date):
    ##int or float??
    line[3] = int(line[3])
    line[2] = datetime.strptime(line[2], '%m%d%Y')
    if (line[0], line[2]) in medianvals_by_date:
        medianvals_by_date[(line[0], line[2])].append(line[3])
    else:
        medianvals_by_date[(line[0], line[2])] = [line[3]]

def main():
    input_file = open(FLAGS.input_data, 'r')
    out_zip_file = open(FLAGS.output_zip_data,'a')
    out_date_file = open(FLAGS.output_date_data,'a')
    medianvals_by_zip = {}
    medianvals_by_date = {}
    for line in input_file:
        clean_by_zip, clean_by_date = clean_input(line)
        if clean_by_zip:
            out_by_zip(out_zip_file, clean_by_zip, medianvals_by_zip)
        if clean_by_date:
            out_by_date(clean_by_date, medianvals_by_date)
    values = sorted(medianvals_by_date)
    for val in values:
        vals = medianvals_by_date[(val[0], val[1])]
        out_date_file.write("|".join([val[0], val[1].strftime('%m%d%Y'), str(int(round(median(vals)))), str(len(vals)), str(sum(vals))]))
        out_date_file.write('\n')
    out_zip_file.close()
    out_date_file.close()
    input_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_data',
        nargs='?',
        type=str,
        default=os.path.join('../input/itcont.txt'),
        help='Path of input data')
    parser.add_argument(
        'output_zip_data',
        nargs='?',
        type=str,
        default=os.path.join('../output/medianvals_by_zip.txt'),
        help='Path of output data for median values by zip')
    parser.add_argument(
        'output_date_data',
        nargs='?',
        type=str,
        default=os.path.join('../output/medianvals_by_date.txt'),
        help='Path of output data for median values by date')

    ##'../input/itcont.txt'
    ##'../output/medianvals_by_zip.txt'
    ##'../output/medianvals_by_date.txt'
    FLAGS, unparsed = parser.parse_known_args()
    main()