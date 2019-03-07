import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Downloading and reading a genome
def getGenome(filename):
    """
    Read fasta file
    """
    genome = ''
    with open(filename, 'r') as f:
        for line in f:
            if not line[0] =='>':
                #remove trailing white space from line
                genome += line.rstrip()
    return genome

genome = getGenome('lambda_virus.fa')
# print 1st 100 bases of virus genome
genome[:100]

counts = {'A': 0, 'T':0, 'G':0, 'C':0}
# raw form
for base in genome:
    counts[base] += 1
#print(counts)

# use collections module to achieve the same result
import collections

new_counts = collections.Counter(genome)

#print(new_counts)


# Working with sequencing reads
# fastq comes in sets of 4
# 1st line = Name to indicate which read it is
# 2nd line = String of DNA bases
# 3rd line = +
# 4th line = quality sequence from read (each quality score is Phred33 encoded
#converted to ASCII character and that is what is on the line)

def readFastq(filename):
    """
    Download and parse FASTQ file
    """
    sequences = []
    qualities = []
    with open(filename) as f:
        while True:
            #dont need line 1
            f.readline()
            #get seq from line 2
            seq = f.readline().rstrip()
            #dont need line 3
            f.readline()
            #get qual from line 4
            qual = f.readline().rstrip()
            # check if we are at end of file, seq will be 0
            if len(seq) == 0:
                break
            #add reads and their qual scores to respective lists
            sequences.append(seq)
            qualities.append(qual)
    return sequences, qualities

seqs, quals = readFastq('SRR835775_1.first1000.fastq')

#print(seqs[:5])
#print(quals[:5])

"""
Usual ASCII encoding is Phred+33, take Qm rounded to integer, add 33, convert to character
"""

def QtoPhred33(Q):
    """Turn Q into Phred+33 ASCII-encoded quality"""
    return chr(Q + 33)

def phred33ToQ(qual):
    """Turn Phred+33 ASCII-encoded quality into Q"""
    return ord(qual)-33

#print(phred33ToQ('#')) # is 2, which is very low
#print(phred33ToQ('J')) J is 41, which is very high, < 1/10,000 base call is incorrect

def createHist(qualities):
    hist = [0] * 50
    for qual in qualities:
        for phred in qual:
            q = phred33ToQ(phred)
            hist[q] += 1
    return hist

h = createHist(quals)
#print(h)

# plot as bar chart
# x vals are length of hist, y vals are histogram itself
plt.bar(range(len(h)), h)
plt.show()

# End of reads have a low quality value, due to improper base calls likely to happen at end of sequence

### ANALYZING READS BY POSITION ###
"""
def findGCByPos(reads):
    # number of GC bases seen at each position in reads
    # all reads are of length 100bp
    gc = [0] * 100
    # total bases
    totals = [0] * 100

    for read in reads;
        for i in range(len(read)):
            if read[i] == 'C' or read[i] == 'G':
                gc[i] += 1
            totals[i] += 1
    for i in range(len(gc))"""
