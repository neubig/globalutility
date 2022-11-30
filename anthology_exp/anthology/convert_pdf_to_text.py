import pdftotext
import os
import sys


inputfile = sys.argv[1]
outputfile = sys.argv[2]

with open(inputfile, "rb") as f:
    pdf = pdftotext.PDF(f)

with open(outputfile, "w") as op:
    op.write("\n\n".join(pdf))
