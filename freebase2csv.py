#!/usr/bin/env python
import gzip
import argparse
import sys
import re

#argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--begin', type=int, help="line number to start")
parser.add_argument('--end', type=int, help="line number to end (not included)")
parser.add_argument('-plain', action='store_true', default=False,
                    help="if input is plain text")
parser.add_argument('--output', type=str, help="output file name")
parser.add_argument("input", metavar='FB_FILE',
                    type=str, help="freebase gz file")
args = parser.parse_args()


def output(line, output):
    #escape commas
    line = line.replace(",", "\,")
    #remove null values
    line = line.replace("\x00", "")
    line = re.sub(r'@[^ @"]*$', "", line)
    triples = line.split("\t")[0:3]
    f = lambda x: x if x[0] == '"' and x[-1] == '"' else "".join(('"', x, '"'))
    line = ",".join(map(f, triples))
    output.write(line + "\n")


def main():
    if args.plain:
        f = open(args.input, "r")
    else:
        f = gzip.GzipFile(args.input, "rb")

    if args.output:
        out = open(args.output, "w")
    else:
        out = sys.stdout
    num = 0
    for line in f:
        num += 1
        if args.begin and num < args.begin:
            continue
        if args.end and num >= args.end:
            break
        output(line, out)
    out.close()

if __name__ == '__main__':
    main()
